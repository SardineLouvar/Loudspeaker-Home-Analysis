import numpy as np
import matplotlib.pyplot as plt
import librosa

# Preferred octave frequency bands according to the ISO standard
# All About Audio Equalization: Solutions and Frontiers - Scientific Figure on ResearchGate.
# Available from: https://www.researchgate.net/figure/Preferred-octave-frequency-bands-according-to-the-ISO-standard-61_tbl1_302067841 [accessed 17 Aug 2026]
XTICKS = [31.5, 63, 125, 250, 500, 1000, 2000, 4000, 8000, 16000]
XTICK_LABELS = ["31.5", "63", "125", "250", "500", "1k", "2k", "4k", "8k", "16k"]

def save_figure(fig, filename):
    fig.savefig("graphs/" + filename + ".png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def plot_amplitude_time(ax, signal, sp, ep, bnep, sample_rate, title):
    time = np.linspace(0, len(signal) / sample_rate, len(signal))

    if bnep is not None:
        ax.plot(time[0:sp], signal[0:sp], 'r', label="Background noise")
        ax.plot(time[sp:ep], signal[sp:ep], 'b', label="Frequency sweep")
        ax.plot(time[ep:bnep], signal[ep:bnep], 'r')
        ax.set_xlim(0, time[-1])
        ax.legend()
    else:
        # For Input Sweep only
        ax.plot(time, signal, 'b', label="Frequency sweep")
        ax.set_xlim(0, time[-1])

    ax.set_ylim(min(signal), max(signal))
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Amplitude (digital)")
    ax.set_title(title)


def plot_spectrum_db_octaves(ax, frequencies, magnitude_spectrum, title):

    # make relative to frequency with highest magnitude
    normalised_spectrum = magnitude_spectrum / np.amax(magnitude_spectrum)
    db = librosa.amplitude_to_db(normalised_spectrum)

    ax.semilogx(frequencies, db)
    ax.set_xlim(20, frequencies.max())
    ax.set_ylim(db.min(), db.max())

    ax.set_title(title)
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Relative Magnitude (dB)")

    ax.set_xticks(XTICKS)
    ax.set_xticklabels(XTICK_LABELS)

    ax.grid(True)


def plot_spectrum_db_octaves_multi(ax, spectra, title):
    all_db = []
    processed = []

    for frequencies, magnitude_spectrum, label in spectra:
        normalised_spectrum = magnitude_spectrum / np.amax(magnitude_spectrum)
        db = librosa.amplitude_to_db(normalised_spectrum)
        processed.append((frequencies, db, label))
        all_db.append(db)

    for frequencies, db, label in processed:
        ax.semilogx(frequencies, db, label=label)

    freq_max = max(f.max() for f, _, _ in processed)
    db_min = min(d.min() for d in all_db)
    db_max = max(d.max() for d in all_db)

    ax.set_xlim(20, freq_max)
    ax.set_ylim(db_min, db_max)

    ax.set_title(title)
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Relative Magnitude (dB)")

    ax.set_xticks(XTICKS)
    ax.set_xticklabels(XTICK_LABELS)

    ax.grid(True)
    ax.legend()


def plot_impulse_response(ax, sample_rate, time, impulse_response):
    ir_db = librosa.amplitude_to_db(impulse_response)

    ax.plot(time, ir_db, 'r')

    ax.grid(True)

    # Set x lim to last value-floor transition
    search_region = ir_db[:len(ir_db)//2]
    last_value_pos = np.where(search_region > min(ir_db))[0][-1]
    time_pos = last_value_pos / sample_rate
    ax.set_xlim(0, time_pos)

    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Impulse response (dB)")
    