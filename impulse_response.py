import os

import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from librosa import amplitude_to_db

from functions.utility_funcs import check_folders, seconds_to_samples
from functions.analysis_funcs import find_sweep_start_in_recording
from functions.plotting import save_figure, plot_impulse_response


def get_impulse_response(input,output):
    input_fft = np.fft.rfft(input)
    output_fft = np.fft.rfft(output)

    reg_fraction = 0.01
    epsilon = reg_fraction * np.max(np.abs(input_fft))
    transfer_function = (output_fft * np.conj(input_fft)) / (np.abs(input_fft)**2 + epsilon**2)

    impulse_response = np.fft.irfft(transfer_function)
    return impulse_response


def impulse_to_wav(label,ir, sample_length):

    # normalise to compress to audible level
    ir_normalised = ir / np.max(np.abs(ir))

    sample_length = seconds_to_samples(sample_rate,sample_length)
    ir_trimmed = ir_normalised[:sample_length]

    wavfile.write(f"audio/generated/{label.replace(" ","_")}_impulse.wav", sample_rate, ir_trimmed.astype(np.float32))


if __name__=="__main__":
    check_folders()
    os.makedirs("audio/generated", exist_ok=True)

    FILES = [
        ("audio/30cm_normal.wav", "30cm Normal"),
        ("audio/50cm_normal.wav", "50cm Normal"),
        ("audio/30cm_loud.wav", "30cm Loud"),
    ]

    sample_rate, input_sweep = wavfile.read("audio/input_sweep.wav")

    time = np.linspace(0,10,seconds_to_samples(sample_rate,10))

    fig, ax = plt.subplots(1, len(FILES), figsize=(6 * len(FILES), 4))

    for i, (path, label) in enumerate(FILES):
        sample_rate, signal = wavfile.read(path)

        # Get accurate time range for sweep in recording
        true_start = find_sweep_start_in_recording(sample_rate,input_sweep,signal,4,16)
        output_sweep = signal[true_start : true_start + input_sweep.shape[0]]

        impulse_response = get_impulse_response(input_sweep,output_sweep)

        ir_db = amplitude_to_db(impulse_response)
        search_region = ir_db[:len(ir_db)//2]
        last_value_pos = np.where(search_region > min(ir_db))[0][-1]
        time_pos = last_value_pos / sample_rate

        plot_impulse_response(ax[i], time, impulse_response, time_pos)
        ax[i].set_title(label)

        # Generate wav from impulse response
        impulse_to_wav(label, impulse_response, time_pos)

    fig.suptitle("Impulse Response from Sweep Start to End")
    fig.tight_layout()


    save_figure(fig, "Impulse_response")