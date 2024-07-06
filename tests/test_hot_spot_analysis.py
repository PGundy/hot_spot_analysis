import pandas as pd
import pytest

from hot_spot_analysis.hot_spot_analysis import HotSpotAnalyzer
from hot_spot_analysis.utils import demo

# Note: it is advisable to use run the following
# pip list #! check which (if any) of hot-spot-analysis is installed
# pip uninstall hot-spot-analysis #! remove any prior installation -- also checks dependents
# pip install hot-spot-analysis #! official release
# pip install -i https://test.pypi.org/simple/ hot-spot-analysis #! install test release
# pip install dist/hot_spot_analysis-X.X.X.tar.gz --force-reinstall #! force install X.X.X


class test_hsa:
    """
    #! This entire section is just meant to run without an error
    """

    @staticmethod
    def create_df_tips(stack_count=50):
        df_tips_temp = demo.data_stacker(
            df=pd.read_csv("data/tips_dataset.csv"),
            stack_count=stack_count,  # stack the data X times
        )
        df_tips_temp["tip_perc"] = df_tips_temp["tip"] / df_tips_temp["total_bill"]

        return df_tips_temp

    @staticmethod
    def calc_tip_stats(data: pd.DataFrame) -> pd.DataFrame:
        """fake"""
        tmp = data.agg(
            avg_tips=pd.NamedAgg("tip", "mean"),
            avg_tip_perc=pd.NamedAgg("tip_perc", "mean"),
        ).round(2)

        return tmp


tips_data_for_hsa = test_hsa.create_df_tips()
print(tips_data_for_hsa.info())

HSA = HotSpotAnalyzer(
    data=tips_data_for_hsa,
    target_cols=["day", "smoker", "size"],
    time_period=["fake_ts"],
    interaction_limit=3,
    objective_function=test_hsa.calc_tip_stats,
)

HSA.run_hsa()
hsa_data = HSA.export_hsa_output_df()
print(hsa_data.head(10))

search_results = HSA.search_hsa_output(search_terms="Sat", search_across="values")
print("\n\nBelow we have the HSA results for the top 'avg_tip_perc' on Saturday.")
print(search_results.sort_values(["avg_tip_perc"], ascending=False).head(10))


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


HSA.search_hsa_output(search_terms=["smoker", "day"], search_across="keys", search_type="any")

HSA.search_hsa_output(search_terms="smoker", search_across="keys", interactions=3)


df_lagged = HSA.lag_hsa_by_time_period(lag_iterations=[1, 3])

HSA.search_hsa_output(
    hsa_df=df_lagged,
    search_across="values",
    search_terms=["10", "Thur"],
    search_type="all",
    interactions=[2],
).head().T
