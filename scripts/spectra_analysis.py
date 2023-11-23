# %%
## Import modules
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from utils import normalize_binary_series, compute_power_spectrum, compute_average_power_spectrum
import pandas as pd

## Path and global variables
HERE = Path(__file__).absolute().parent.parent
DATA = HERE / 'data'

# Length of each segment
segment_length = 64

# Overlap between segments
overlap = 32

# %%
## Read data
random_df = pd.read_csv(DATA/'study1_random_df.csv')
compare_df = pd.read_csv(DATA/'study1_compare_df.csv')

# %%
df = random_df.reset_index().pivot_table( index = ['id', 'age', 'sex', 'condition', 'condition_vis', 'file_name'], columns = ['ids'] )
seq = df['key'].values.tolist()
seq = [ np.array(x)[~np.isnan(x)].astype(int) for x in seq ]
invisible = list(df.reset_index().condition_vis)
invisible_list = [ item for n, item in enumerate(seq) if invisible[n] == 'invisible' ]
visible_list = [ item for n, item in enumerate(seq) if invisible[n] == 'visible' ]
# %%
## Average power spectra over participants

## Normalize series.
invisible_series = [ normalize_binary_series(item) for item in invisible_list if sum(item) > 10 ]
visible_series = [ normalize_binary_series(item) for item in visible_list if sum(item) > 10 ]

## Compute power spectra for all participants
invisible_spectrum = [ compute_average_power_spectrum(series, segment_length = segment_length, overlap = overlap) for series in invisible_series if len(series) > 100 ]
visible_spectrum = [ compute_average_power_spectrum(series, segment_length = segment_length, overlap = overlap) for series in visible_series if len(series) > 100 ]

## Average power spectra over participants
invisible_spectrum_average = pd.DataFrame(invisible_spectrum).mean(axis = 0)
visible_spectrum_average = pd.DataFrame(visible_spectrum).mean(axis = 0)

# %%
## Compute and plot average power spectrum for all participants
plt.figure(figsize=(10, 6))
freq_values = np.fft.fftfreq(len(invisible_spectrum_average))
plt.plot(np.log10(freq_values), np.log10(invisible_spectrum_average), marker = 'o', linestyle='-', label='Invisible')
plt.plot(np.log10(freq_values), np.log10(visible_spectrum_average), marker = 'o', linestyle='-', label='Visible')
plt.title('Average Spectral Density of Binary Series (log10 scale)')
plt.xlabel('Frequency (log10)')
plt.ylabel('Average Power (log10)')
plt.legend()
plt.grid(True)
plt.show()
# %%
