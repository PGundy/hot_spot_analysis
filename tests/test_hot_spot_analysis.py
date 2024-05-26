import pandas as pd
import pytest
import seaborn as sns  # Only imported to load some common datasets

from hot_spot_analysis.hot_spot_analysis import HotSpotAnalysis


class test_hsa:
    """
    This class just holds some of the
    """

    def create_df_tips(self):

        df_tips_temp = demo.data_stacker(
            df=sns.load_dataset("tips"),
            stack_count=50,  # stack the data X times
        )
        df_tips_temp["tip_perc"] = df_tips_temp["tip"] / df_tips_temp["total_bill"]

        return df_tips_temp

    def calc_tip_stats(self, data: pd.DataFrame) -> pd.DataFrame:
        """fake"""
        tmp = data.agg(
            #!count_tips=pd.NamedAgg("tip", "count"),
            avg_tips=pd.NamedAgg("tip", "mean"),
            avg_tip_perc=pd.NamedAgg("tip_perc", "mean"),
        ).round(2)

        return tmp


from hot_spot_analysis import hot_spot_analysis

HSA = hot_spot_analysis.HotSpotAnalysis(
    data=test_hsa.create_df_tips(),
    # data=df_tips_plus.groupby("sex", observed=True),
    target_cols=["day", "smoker", "size"],
    time_period=["timestamp"],
    interaction_limit=3,
    objective_function=test_hsa.calc_tip_stats,
)

# HSA.prep_analysis()
# HSA.test_objective_function(verbose=False)
HSA.run_hsa()
hsa_data = HSA.export_hsa_output_df()
print(hsa_data.head())
