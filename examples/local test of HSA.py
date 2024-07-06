# %%

import pandas as pd

from hot_spot_analysis.hot_spot_analysis import HotSpotAnalyzer
from hot_spot_analysis.utils import demo

df_tips = demo.build_demo_df_from_sns_datasets("tips")
df_tips["tip_perc"] = df_tips["tip"] / df_tips["total_bill"]
df_tips.info()


def calc_tip_stats(data: pd.DataFrame) -> pd.DataFrame:
    """fake"""
    tmp = data.agg(
        avg_tips=pd.NamedAgg("tip", "mean"),
        avg_tip_perc=pd.NamedAgg("tip_perc", "mean"),
    ).round(2)

    return tmp


calc_tip_stats(df_tips).head()


# %%

HSA = HotSpotAnalyzer(
    data=df_tips,
    target_cols=["day", "smoker", "size"],
    time_period=["fake_ts"],
    interaction_limit=3,
    objective_function=calc_tip_stats,
)

HSA.run_hsa()
hsa_data = HSA.export_hsa_output_df()
print(hsa_data.head(10))

# %%

HSA.lag_hsa_by_time_period([1, 3, 6]).head(10)

# %%
