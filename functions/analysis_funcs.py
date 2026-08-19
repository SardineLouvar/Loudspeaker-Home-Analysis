import numpy as np
from scipy.signal import fftconvolve

from functions.utility_funcs import seconds_to_samples

def find_offset(signal, reference):
    corr = fftconvolve(signal, reference[::-1], mode='valid')
    offset = np.argmax(np.abs(corr))
    return offset


def get_freq_data(signal, sample_rate):
    magnitude_spectrum = np.abs(np.fft.rfft(signal))
    frequencies = np.fft.rfftfreq(len(signal), 1 / sample_rate)
    return frequencies, magnitude_spectrum


def find_sweep_start_in_recording(sample_rate_input,input_sweep,output_signal,lb=4,ub=16):
    search_start = seconds_to_samples(sample_rate_input, lb)
    search_end = seconds_to_samples(sample_rate_input, ub)
    search_region = output_signal[search_start:search_end]

    offset = find_offset(search_region, input_sweep)
    #print(offset / sample_rate_input)
    return search_start + offset


def get_magnitude_freq_data(input, output, sample_rate):
    input_fft = np.fft.rfft(input)
    output_fft = np.fft.rfft(output)

    frequencies = np.fft.rfftfreq(len(input),1/sample_rate)

    # Wiener deconvolution:
    # Prevents noise from blowing up when sweep has little energy, ...
    # and prevents noise spikes from dividing by small numbers.
    reg_fraction = 0.01
    epsilon = reg_fraction * np.max(np.abs(input_fft))
    transfer_function = (output_fft * np.conj(input_fft)) / (np.abs(input_fft)**2 + epsilon**2)

    magnitude_spectrum = np.abs(transfer_function)

    return frequencies,magnitude_spectrum


def smooth_octave(frequencies, magnitude, fraction=3):
    # 1/fraction octave smoothing in linear space
    smoothed = np.copy(magnitude)
    for i, f in enumerate(frequencies):
        if f <= 0:
            continue       

        # Can do as frequencies is ordered list
        low = np.searchsorted(frequencies, f / 2**(1/(2*fraction)), side='left') 
        high = np.searchsorted(frequencies, f * 2**(1/(2*fraction)), side='right') 
        smoothed[i] = np.mean(magnitude[low:high])
    return smoothed