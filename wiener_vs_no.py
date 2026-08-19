import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

from functions.utility_funcs import check_folders
from functions.analysis_funcs import find_sweep_start_in_recording, get_magnitude_freq_data, smooth_octave
from functions.plotting import plot_spectrum_db_octaves_multi, save_figure


def get_magnitude_freq_data_naive(input, output, sample_rate):
    input_fft = np.fft.rfft(input)
    output_fft = np.fft.rfft(output)

    frequencies = np.fft.rfftfreq(len(input),1/sample_rate)

    transfer_function = output_fft / input_fft

    magnitude_spectrum = np.abs(transfer_function)

    return frequencies,magnitude_spectrum


if __name__ == "__main__":
    check_folders()

    sample_rate, input_sweep = wavfile.read("audio/input_sweep.wav")

    path = "audio/30cm_loud.wav"

    sample_rate, signal = wavfile.read(path)

    # Get accurate time range for sweep in recording
    true_start = find_sweep_start_in_recording(sample_rate,input_sweep,signal,4,16)
    output_sweep = signal[true_start:true_start + len(input_sweep)]

    # Naive
    frequencies_naive, magnitude_naive = get_magnitude_freq_data_naive(input_sweep, output_sweep, sample_rate)
    magnitude_naive_smoothed = smooth_octave(frequencies_naive, magnitude_naive, fraction=3)

    # Wiener deconvolution
    frequencies_normal, magnitude_normal = get_magnitude_freq_data(input_sweep, output_sweep, sample_rate)
    magnitude_normal_smoothed = smooth_octave(frequencies_normal, magnitude_normal, fraction=3)


    # put both on one graph
    spectra = [(frequencies_naive, magnitude_naive_smoothed, "Naive"),
        (frequencies_normal, magnitude_normal_smoothed, "Normal")]

    fig, ax = plt.subplots(figsize=(10, 6))

    plot_spectrum_db_octaves_multi(ax,spectra, "30cm Loud - Naive vs Normal")

    fig.tight_layout()

    save_figure(fig, "30cm_Loud_Naive_vs_Normal")

