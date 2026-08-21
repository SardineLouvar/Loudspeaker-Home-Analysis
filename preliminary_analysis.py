import matplotlib.pyplot as plt
from scipy.io import wavfile

from functions.utility_funcs import check_folders,seconds_to_samples
from functions.analysis_funcs import get_freq_data, find_sweep_start_in_recording
from functions.plotting import plot_amplitude_time, plot_spectrum_db_octaves, save_figure


if __name__=="__main__":
    check_folders()

    FILES = [
        ("audio/input_sweep.wav", "Input Sweep"),
        ("audio/30cm_normal.wav", "30cm Normal"),
        ("audio/50cm_normal.wav", "50cm Normal"),
        ("audio/30cm_loud.wav", "30cm Loud"),
    ]

    sample_rate, input_sweep = wavfile.read("audio/input_sweep.wav")

    fig_time, axes_time = plt.subplots(1, len(FILES), figsize=(6 * len(FILES), 4))
    fig_freq, axes_freq = plt.subplots(1, len(FILES), figsize=(6 * len(FILES), 4))

    for i, (path, label) in enumerate(FILES):
        sample_rate, signal = wavfile.read(path)

        sp = seconds_to_samples(sample_rate, 5)
        ep = seconds_to_samples(sample_rate, 15)

        if label == "Input Sweep":
            target_signal = signal
            # No background noise region for pure signal
            bnep = None  
        else:
            bnep = seconds_to_samples(sample_rate, 20)

            # Get accurate time range for sweep in recording
            true_start = find_sweep_start_in_recording(sample_rate,input_sweep,signal,4,16)
            target_signal = signal[true_start : true_start + len(input_sweep)]

        plot_amplitude_time(axes_time[i], signal, sp, ep, bnep, sample_rate, label)

        frequencies, magnitude_spectrum = get_freq_data(target_signal, sample_rate)
        plot_spectrum_db_octaves(axes_freq[i], frequencies, magnitude_spectrum, label)

    fig_time.suptitle("Amplitude vs Time")
    fig_freq.suptitle("Magnitude Spectrum")

    fig_time.tight_layout()
    fig_freq.tight_layout()

    save_figure(fig_time, "Amplitude_Time_Comparison")
    save_figure(fig_freq, "Magnitude_Spectrum_Comparison")