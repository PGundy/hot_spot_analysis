#%%

from __future__ import annotations

import numpy as np
import pandas as pd
import seaborn as sns

from hot_spot_analysis.hot_spot_analysis import HotSpotAnalysis

""" Create an instance of the HotSpotAnalysis class"""
HSA = HotSpotAnalysis()


# ! ---------------------------------------------------------------------------------
#%%

## Load data from seaborn
df = sns.load_dataset("diamonds")

## Funtionally get categorical variables: ['cut', 'color', 'clarity']
df_key_vars = list(df.select_dtypes(include=["category"]).columns)

## Let's create a fake cohort variable; 'retailer'
df["retailer"] = df.reset_index()["index"]
df["retailer"] = (df["retailer"] % 3) + 1  ## create 3 groups
dict_retailer = {1: "Tiffany", 2: "DeBeers", 3: "Cartier"}
df["retailer"] = df["retailer"].map(dict_retailer)

## Pre-define any coumns required in the exampleFunction
df["price_per_carat"] = df["price"] / df["carat"]

df.head()


#%%
#! Define a HSA object!
# HSA = HotSpotAnalysis()
HSA.data_cuts = df_key_vars
HSA.depth_limit = 4
HSA.data = df
# HSA.data = df.groupby(["retailer"])


#! Here we have a function that calculates out key metrics
def exampleFunction(data):

    data = data.agg(
        count=pd.NamedAgg("price", "count"),
        size=pd.NamedAgg("price", "size"),
        avg_price=pd.NamedAgg("price", np.mean),
        med_price=pd.NamedAgg("price", np.median),
        price_per_carat=pd.NamedAgg("price_per_carat", np.mean),
    ).round(2)

    return data


#! Is our function going to work for the full HSA?
HSA.test_user_function(exampleFunction)

#%%
#! Run the HSA
HSA.run_hsa(user_function=exampleFunction)

#! View the output data
HSAdata = HSA.get_hsa_data()
HSAdata.head()

#%%
#! Explore the data - part 1
print("HSA.get_data_cuts().head()")
HSA.get_data_cuts().head()

#%%
#! Explore the data - part 2
TEMP = pd.DataFrame()

# NOTE: This is using a hidden method to demonostrate functionality and avoid a warning message.
if HSA._is_data_grouped():
    ## If grouped on 'Retailer' then...
    TEMP = HSA.get_data_content(data_cut=["retailer", "clarity"]).head()
else:
    print('HSA.get_data_content("clarity").head()')
    TEMP = HSA.get_data_content("clarity").head()

TEMP.head()


#%%

#! Search across the data
HSA.filter_hsa_data(
    target_var="data_cut_content",
    search_terms="color: G",
    search_type="broad",
).head()

# %%
#! Chain filtering!
### Now lets use the above filter & get every 'cut: Very Good'
### THUS we now have 'color: G' & 'cut: Very Good' at depth 2 &
### all level 3 interactions contain BOTH 'color: G' & 'cut: Very Good'

df_chain_filtering = HSA.filter_hsa_data(
    target_var="data_cut_content",
    search_terms="color: G",
    search_type="broad",
)

HSA.filter_hsa_data(
    target_var="data_cut_content",
    search_terms="cut: Very Good",
    search_type="broad",
    depth_filter=[2, 3, 4],
    data=df_chain_filtering,
).head()


# %%
print("everything ran as expected.")
