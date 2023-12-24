# %%

import pandas as pd
import seaborn as sns
import seaborn as sb

# from utils import

# %%

df = sb.load_dataset("tips")

df.head()

# %%

# list = [1,2,3,4]
# list + ['a']

# %%

from utils import combos, list_funcs

df = sb.load_dataset("tips")

df.head()
# %%


list1 = [2, 1]
# list1.sort()
list2 = [1, 2]

list_funcs._make_list_unique(input_list=list1)  # = list2

# %%
