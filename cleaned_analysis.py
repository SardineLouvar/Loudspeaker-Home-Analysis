import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import fftconvolve


from functions.utility_funcs import check_folders
from functions.analysis_funcs import find_sweep_start_in_recording, get_magnitude_freq_data, smooth_octave
from functions.plotting import plot_spectrum_db_octaves_multi, save_figure


if __name__=="__main__":
    check_folders()

    OUTPUT_FILES = [
        ("audio/30cm_normal.wav", "30cm Normal"),
        ("audio/50cm_normal.wav", "50cm Normal"),
        ("audio/30cm_loud.wav", "30cm Loud"),
    ]

    sample_rate, input_sweep = wavfile.read("audio/input_sweep.wav")

    spectra = []

    for path, label in OUTPUT_FILES:
        sample_rate, signal = wavfile.read(path)

        # Get accurate time range for sweep in recording
        true_start = find_sweep_start_in_recording(sample_rate,input_sweep,signal,4,16)
        output_sweep = signal[true_start: true_start + len(input_sweep)]

        frequencies, magnitude_spectrum = get_magnitude_freq_data(input_sweep, output_sweep, sample_rate)
        magnitude_smoothed = smooth_octave(frequencies, magnitude_spectrum, fraction=3)

        spectra.append((frequencies, magnitude_smoothed, label))

    fig, ax = plt.subplots(figsize=(10, 6))
    plot_spectrum_db_octaves_multi(ax, spectra, "Magnitude Frequency Response for All Recordings")
    fig.tight_layout()

    save_figure(fig, "Magnitude_Frequency_Response_Comparison")

