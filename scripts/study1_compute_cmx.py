## Import modules and functions
import pandas as pd
import numpy as np
from pybdm import BDM
from pybdm import PartitionIgnore, PartitionRecursive
from pathlib import Path

## Path and global variables
HERE = Path(__file__).absolute().parent.parent
DATA = HERE / 'data'

## BDM class
s = 11
bdm = BDM(ndim=1, shape = (s,), raise_if_zero = False, partition=PartitionIgnore)
bdm_rec = BDM(ndim=1, shape = (12,), raise_if_zero=False, partition=PartitionRecursive)
bdm_short_7 = BDM(ndim = 1, shape = (7,), partition = PartitionRecursive, min_length = 7)

## Function to compute rolling Algorithmic Complexity
def window_bdm(seq, bdm, k = 7, normalized = False, step = 1):
    return np.array([ bdm.bdm(seq[i : (i + k)], normalized = normalized) for i in range(0,len(seq) - k, step) ])

## Read data 
random_df = pd.read_csv(DATA/'study1_random_df.csv')
compare_df = pd.read_csv(DATA/'study1_compare_df.csv')

## Prepare data for algorithmic complexity computation
df = random_df.reset_index().pivot_table( index = ['id', 'age', 'sex', 'condition', 'condition_vis', 'file_name'], columns = ['ids'] )
seq = df['key'].values.tolist()
seq = [ np.array(x)[~np.isnan(x)].astype(int) for x in seq ]
seq_cmx = [ list( item[i:i+s] for i in range(0, len(item), s) ) for item in seq ]
seq_cmx = [ list( item[i:i+s] for i in range(0, len(item), s) if len(item[i:i+s]) > 3 ) for item in seq ]

## Demographic data
data  = pd.DataFrame(df.index.tolist())

## Compute algorithmic complexity
data['cmx'] = [ bdm.nbdm(x) for x in seq ]
data['cmx_mean'] = [ np.mean( list( bdm.nbdm(x) if len(x) > s - 1 else bdm_rec.nbdm(x) for x in item ) ) for item in seq_cmx ]
data['cmx_sd'] = [ np.std( list( bdm.nbdm(x) if len(x) > s - 1 else bdm_rec.nbdm(x) for x in item ) ) for item in seq_cmx ]
data['cmx_rn7'] = [ window_bdm(x, bdm = bdm_short_7, k = 7, normalized = True) for x in seq ]

## Filter out series shorter than 96 elements
data = data[data.cmx_rn7.apply(lambda x: len(x) > 95)]
data['cmx_rn7'] = data.cmx_rn7.apply(lambda x: ','.join(x.astype(str)))

## Write out data to csv
data.to_csv(DATA/'study1_random_cmx.csv')
