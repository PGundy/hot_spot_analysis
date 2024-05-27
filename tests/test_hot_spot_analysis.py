import pandas as pd
import pytest
import seaborn as sns  # Only imported to load some common datasets

from hot_spot_analysis.hot_spot_analysis import HotSpotAnalysis
from hot_spot_analysis.utils import demo


class test_hsa:
    """
    TODO: add explination for this
    """

    @staticmethod
    def create_df_tips(stack_count=50):
        df_tips_temp = demo.data_stacker(
            df=sns.load_dataset("tips"),
            stack_count=stack_count,  # stack the data X times
        )
        df_tips_temp["tip_perc"] = df_tips_temp["tip"] / df_tips_temp["total_bill"]

        return df_tips_temp

    @staticmethod
    def calc_tip_stats(data: pd.DataFrame) -> pd.DataFrame:
        """fake"""
        tmp = data.agg(
            #!count_tips=pd.NamedAgg("tip", "count"),
            avg_tips=pd.NamedAgg("tip", "mean"),
            avg_tip_perc=pd.NamedAgg("tip_perc", "mean"),
        ).round(2)

        return tmp


HSA = HotSpotAnalysis(
    data=test_hsa.create_df_tips(),
    target_cols=["day", "smoker", "size"],
    # time_period=["timestamp"],
    interaction_limit=3,
    objective_function=test_hsa.calc_tip_stats,
)

HSA.run_hsa()
hsa_data = HSA.export_hsa_output_df()
print(hsa_data.head(10))

search_results = HSA.search_hsa_output(search_terms="Sat", search_across="values")
print("\n\nBelow we have the HSA results for the top 'avg_tip_perc' on Saturday.")
print(search_results.sort_values(["avg_tip_perc"], ascending=False).head(10))
