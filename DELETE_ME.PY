# %%

import pandas as pd
import seaborn as sns

from hot_spot_analysis.hot_spot_analysis import HotSpotAnalysis
from hot_spot_analysis.utils import demo

# %%


df_tips = demo.data_stacker(
    df=sns.load_dataset("tips"),
    stack_count=100,  # stack data to create fake 'timestamp' variable
)
df_tips["tip_perc"] = df_tips["tip"] / df_tips["total_bill"]


def tip_stats(data: pd.DataFrame) -> pd.DataFrame:
    """fake"""
    tmp = data.agg(
        #!count_tips=pd.NamedAgg("tip", "count"),
        avg_tips=pd.NamedAgg("tip", "mean"),
        avg_tip_perc=pd.NamedAgg("tip_perc", "mean"),
    ).round(2)

    return tmp


HSA = HotSpotAnalysis(
    data=df_tips,
    # data=df_tips_plus.groupby("sex", observed=True),
    target_cols=["day", "smoker", "size"],
    time_period=["timestamp"],
    interaction_limit=3,
    objective_function=tip_stats,
)

# HSA.prep_analysis()
# HSA.test_objective_function(verbose=False)
HSA.run_hsa()
hsa_data = HSA.export_hsa_output_df()
hsa_data.head(10)


# %%
HSA.search_hsa_output(
    search_terms="Thur",
    search_across="values",
    search_type="any",
    interactions=[1, 2],
).head()

# %%
HSA.search_hsa_output(
    search_terms="Yes",
    search_across="values",
    search_type="any",
    # interactions=[2,3],
    n_row_minimum=50,
).head(10)

# %%

# HSA.search_hsa_output(search_terms="smoker", search_across="keys", search_type="all")

# HSA.search_hsa_output(search_terms=["smoker", "day"], search_across="keys", search_type="all")

# HSA.search_hsa_output(search_terms="smoker", search_across="keys", interactions=1)

# HSA.search_hsa_output(search_terms=["Male", "Yes"], search_across="values", search_type="all")

# HSA.search_hsa_output(search_terms=["Fri", "Yes"], search_across="values", search_type="all")

# %%


df_lagged = HSA.lag_hsa_by_time_period(lag_iterations=[1, 3])

# %%
HSA.search_hsa_output(
    hsa_df=df_lagged,
    search_across="values",
    search_terms=["Thur"],
    search_type="any",
    interactions=[2],
)


# %%
