import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

from functions.utility_funcs import check_folders, seconds_to_samples
from functions.analysis_funcs import get_magnitude_freq_data, find_sweep_start_in_recording, smooth_octave
from functions.plotting import save_figure


def get_impulse_response(input,output):
    input_fft = np.fft.rfft(input)
    output_fft = np.fft.rfft(output)

    frequencies = np.fft.rfftfreq(len(input),1/sample_rate)

    reg_fraction = 0.01
    epsilon = reg_fraction * np.max(np.abs(input_fft))
    transfer_function = (output_fft * np.conj(input_fft)) / (np.abs(input_fft)**2 + epsilon**2)
    impulse_response = np.fft.irfft*(transfer_function)
    return impulse_response


if __name__=="__main__":
    check_folders()

    FILES = [
        ("audio/30cm_normal.wav", "30cm Normal"),
        ("audio/50cm_normal.wav", "50cm Normal"),
        ("audio/30cm_loud.wav", "30cm Loud"),
    ]

    sample_rate, input_sweep = wavfile.read("audio/input_sweep.wav")

    time = seconds_to_samples(sample_rate,10)

    fig_time, axes_time = plt.subplots(1, len(FILES), figsize=(6 * len(FILES), 4))
    fig_freq, axes_freq = plt.subplots(1, len(FILES), figsize=(6 * len(FILES), 4))

    for i, (path, label) in enumerate(FILES):
        sample_rate, signal = wavfile.read(path)\
        

        # Get accurate time range for sweep in recording
        true_start = find_sweep_start_in_recording(sample_rate,input_sweep,signal,4,16)
        target_signal = signal[true_start : true_start + len(input_sweep)]

        impulse_response = get_impulse_response(signal,target_signal)

        plt.plot(impulse_response,time)

    plt.show()

    # fig_time.suptitle("Amplitude vs Time")
    # fig_freq.suptitle("Magnitude Spectrum")

    # fig_time.tight_layout()
    # fig_freq.tight_layout()

    # save_figure(fig_time, "Amplitude_Time_Comparison")
    # save_figure(fig_freq, "Magnitude_Spectrum_Comparison")