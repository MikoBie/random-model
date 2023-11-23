
# %%
import numpy as np
from collections import defaultdict
import pandas as pd

# %%
def window_bdm(seq: np.array, bdm, k: int = 7, normalized: bool = False, step: int = 1) -> np.array:
    """
    It takes an array of 0s and 1s and returns an array of rolling 
    algorithmic complexity.

    Args:
        seq (np.array): an array filled with 0s and 1s.
        bdm (function): a function to compute Algorithmic Complexity.
        k (int, optional): the length of the rolling window. Defaults to 7.
        normalized (bool, optional): whether Algorithmic Complexity should be
        normalized. Defaults to False.
        step (int, optional): the length of the step between rolling windows. Defaults to 1.

    Returns:
        np.array : an array with the measures of rolling Algorithmic Complexity.
    """
    return np.array([ bdm.bdm(seq[i : (i + k)], normalized = normalized) for i in range(0,len(seq) - k, step) ])

def occurrences(string, sub) -> int:
    """
    Returns number of occurences of a given substring in a string.

    Args:
        string (str): a string.
        sub (str): a substring to check occurences.

    Returns:
        (int) : number of occurances of substring in string.
    """
    count = start = 0
    while True:
        start = string.find(sub, start) + 1
        if start > 0:
            count+=1
        else:
            return count
        
def freq_5(seq: np.array) -> dict:
    """
    Returns a dictionary with frequencies of u

    Args:
        seq (np.array): _description_

    Returns:
        dict: _description_
    """
    seq_str = ''
    permutations = [ format(item, '#03b') for item in range(2) ]
    permutations += [ format(item, '#04b') for item in range(4) ]
    permutations += [ format(item, '#05b') for item in range(8) ]
    permutations += [ format(item, '#06b') for item in range(16) ]
    permutations += [ format(item, '#07b') for item in range(32) ]
    for item in seq:
        seq_str += str(item)
    output = defaultdict(int)
    for item in permutations:
        temp_i = item[2:]
        output[temp_i] = occurrences(string = seq_str, sub = temp_i)
    return output

def normalize_binary_series(series: np.array) -> np.array:
    """
    Takes a series of 1s and 0s and normalizes them around the mean.

    Args:
        series (_type_): a series of 0s and 1s.

    Returns:
        np.array: a normalized series.
    """
    mean = np.mean(series)
    sd = np.std(series)
    return np.array( [ (item - mean)/sd for item in series ] )

def compute_power_spectrum(segment: np.array) -> np.array:
    """
    Computes a Fourier transformation using a Fast Fourier Transform model. It
    returns a power spectrum of the np.array.

    Args:
        segment (np.array): a series.

    Returns:
        np.array: a power spectrum of the segment (series)
    """
    return np.abs(np.fft.fft(segment))**2

def compute_average_power_spectrum(binary_series: np.array, segment_length: int, overlap: int) -> np.array:
    """
    Computes average power spectrum over rolling window of length of segment_length and overlaping.

    Args:
        binary_series (np.array): a series.
        segment_length (int, optional): length of the segment. Defaults to segment_length.
        overlap (int, optional): overlap between preceding segments. Defaults to overlap.

    Returns:
        np.array: a series with averaged power spectra of length segment_length.
    """
    num_segments = int((len(binary_series) - segment_length) / (segment_length - overlap)) + 1
    spectra = []

    for i in range(num_segments):
        start = i * (segment_length - overlap)
        end = start + segment_length
        segment = binary_series[start:end]
        spectrum = compute_power_spectrum(segment)
        spectra.append(spectrum)

    # Compute the average spectrum
    average_spectrum = pd.DataFrame(spectra).mean(axis = 0)

    return average_spectrum