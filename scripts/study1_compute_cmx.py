# %%
## Import modules and functions
import pandas as pd
import numpy as np
from pybdm import BDM
from pybdm import PartitionIgnore, PartitionRecursive
from pathlib import Path
from collections import defaultdict

## Path and global variables
HERE = Path(__file__).absolute().parent.parent
DATA = HERE / 'data'

## BDM class
s = 11
bdm = BDM(ndim=1, shape = (s,), raise_if_zero = False, partition=PartitionIgnore)
bdm_rec = BDM(ndim=1, shape = (12,), raise_if_zero=False, partition=PartitionRecursive)
bdm_short_7 = BDM(ndim = 1, shape = (7,), partition = PartitionRecursive, min_length = 7)
bdm_short_8 = BDM(ndim = 1, shape = (8,), partition = PartitionRecursive, min_length = 8)
bdm_short_9 = BDM(ndim = 1, shape = (9,), partition = PartitionRecursive, min_length = 9)
bdm_short_5 = BDM(ndim = 1, shape = (5,), partition = PartitionRecursive, min_length = 5)
bdm_short_6 = BDM(ndim = 1, shape = (6,), partition = PartitionRecursive, min_length = 6)

# %%
## Function to compute rolling Algorithmic Complexity
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
    permutations = [ format(item, '#04b') for item in range(4) ]
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

# %%
## Read data 
random_df = pd.read_csv(DATA/'study1_random_df.csv')
compare_df = pd.read_csv(DATA/'study1_compare_df.csv')

# %%
## Prepare data for algorithmic complexity computation
df = random_df.reset_index().pivot_table( index = ['id', 'age', 'sex', 'condition', 'condition_vis', 'file_name'], columns = ['ids'] )
seq = df['key'].values.tolist()
seq = [ np.array(x)[~np.isnan(x)].astype(int) for x in seq ]
seq_cmx = [ list( item[i:i+s] for i in range(0, len(item), s) ) for item in seq ]
seq_cmx = [ list( item[i:i+s] for i in range(0, len(item), s) if len(item[i:i+s]) > 3 ) for item in seq ]
seq_5 = [ freq_5(s) for s in seq ]
# %%
## Demographic data
data  = pd.DataFrame(df.index.tolist())

# %%
## Compute algorithmic complexity
data['cmx'] = [ bdm.nbdm(x) for x in seq ]
data['cmx_mean'] = [ np.mean( list( bdm.nbdm(x) if len(x) > s - 1 else bdm_rec.nbdm(x) for x in item ) ) for item in seq_cmx ]
data['cmx_sd'] = [ np.std( list( bdm.nbdm(x) if len(x) > s - 1 else bdm_rec.nbdm(x) for x in item ) ) for item in seq_cmx ]
data['cmx_rn7'] = [ window_bdm(x, bdm = bdm_short_7, k = 7, normalized = True) for x in seq ]
data['cmx_rn8'] = [ window_bdm(x, bdm = bdm_short_8, k = 8, normalized = True) for x in seq ]
data['cmx_rn9'] = [ window_bdm(x, bdm = bdm_short_9, k = 9, normalized = True) for x in seq ]
data['cmx_rn5'] = [ window_bdm(x, bdm = bdm_short_5, k = 5, normalized = True) for x in seq ]
data['cmx_rn6'] = [ window_bdm(x, bdm = bdm_short_6, k = 6, normalized = True) for x in seq ]
data = pd.concat([data, pd.DataFrame.from_records(seq_5)], axis = 1)
data['alternation_rate'] = data.apply(lambda x: (x['01'] + x['10'])/(x['00'] + x['01'] + x['10'] + x['11']), axis = 1)


# %%
## Filter out series shorter than 96 elements
data = data[data.cmx_rn7.apply(lambda x: len(x) > 95)]
data['cmx_rn7'] = data.cmx_rn7.apply(lambda x: ','.join(x.astype(str)))
data['cmx_rn8'] = data.cmx_rn8.apply(lambda x: ','.join(x.astype(str)))
data['cmx_rn9'] = data.cmx_rn9.apply(lambda x: ','.join(x.astype(str)))
data['cmx_rn5'] = data.cmx_rn5.apply(lambda x: ','.join(x.astype(str)))
data['cmx_rn6'] = data.cmx_rn6.apply(lambda x: ','.join(x.astype(str)))

# %%
## Write out data to csv
data.to_csv(DATA/'study1_random_cmx.csv')
# %%
