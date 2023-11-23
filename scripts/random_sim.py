# %%
import numpy as np
from utils import freq_5
import pandas as pd
from pathlib import Path

# %%
np.random.seed(2137)
HERE = Path(__file__).absolute().parent.parent
DATA = HERE/'data'

# %%
sim_df = [ np.random.randint(low = 0, high = 2, size = 120) for i in range(100) ]
df = [ freq_5(item) for item in sim_df ]
df = pd.DataFrame.from_records(df)

# %%
df.to_csv(DATA/'study1_random_counts.csv')
# %%
