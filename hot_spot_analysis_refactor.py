# %%
from dataclasses import dataclass
from typing import Callable

import numpy as np
import pandas as pd
import seaborn as sns

from utils2 import combos, general, grouped_df, lists


# %%
@dataclass
class HotSpotAnalysis:
    """
    _summary_ TODO
    fdsfsd
    """

    data: pd.DataFrame
    target_cols: list[str]
    interaction_limit: int
    objective_function: Callable

    def __init__(
        self,  # Default values
        data: pd.DataFrame = pd.DataFrame(None),  # HSA.data.empty -> True
        target_cols: list = [None],  # []
        interaction_limit: int = 3,  # 3
        objective_function=None,
    ):
        self.data_input = data
        self.target_cols = lists.unique(target_cols, drop_none=True)
        self.interaction_limit = interaction_limit
        self.objective_function = objective_function

        # Set defaults for variables set via functions
        self.pre_grouped_vars: list[str] = None
        self.data_prep: pd.DataFrame = pd.DataFrame(None)
        self.combinations: list[list[str]] = None
        self.obj_func_tested: bool = False
        self.hsa_raw_output_dicts: list[dict] = None
        self.hsa_output_df: pd.DataFrame = pd.DataFrame(None)

    def prep_class(self):
        """Extract any groups & the dataframe from the init"""
        self.data_prep = grouped_df.return_data(self.data_input)

        if grouped_df.is_grouped(self.data_input):
            self.pre_grouped_vars = grouped_df.get_groups(self.data_input)

    def _build_combos(self):
        """fake doc string"""
        if self.data_prep.empty:
            self.prep_class()

        combinations = combos.create_combos(
            target_cols=self.target_cols, interaction_max=self.interaction_limit
        )

        if self.pre_grouped_vars is not None:
            # If the input data is grouped we add the groups!
            combinations = grouped_df.add_groups_to_combos(
                group_vars=self.pre_grouped_vars, combos=combinations
            )

        self.combinations = combinations

        print(
            f"Combinations have been generated. There are {len(combinations)} across the target variables: {','.join(self.target_cols)}"
        )

    def _build_data(self):
        """fake doc string"""
        if self.data_prep.empty:
            self.prep_class()

        # TODO Add validation checks here for 'target_cols' in 'self.data_input', etc.

        self.data_prep["Overall"] = "Overall"
        print("Data passed checks, and is ready for analysis.")

    def test_objective_function(
        self,
        row_limit: int = 100,
        verbose: bool = True,
    ):
        """check if the objective function even works"""
        if self.data_prep.empty:
            self._build_data()

        if verbose:
            print(f"Using random sample of {row_limit} rows")

        test_df = self.data_prep.sample(row_limit, replace=True)

        try:
            output = self.objective_function(test_df.groupby("Overall"))
        except:
            raise ValueError(
                "The function supplied to 'objective_function' is not compatible\n\nThe function must be able to run on a grouped data frame."
            )

        self.obj_func_tested = True
        if verbose:
            return output

    def prep_analysis(self):
        """fake doc string"""
        self._build_data()
        self._build_combos()
        if not self.obj_func_tested:
            self.test_objective_function(verbose=False)

    def run_obj_func_iterations(self):
        self.prep_analysis()

        if self.hsa_raw_output_dicts is not None:
            print("The objective function has already been run.")

        combination_outputs = []
        print("\n")
        for step_i, combo in enumerate(self.combinations):
            print(f"\tstep: {step_i} group by {combo}")
            df_grp_by_combo = self.data_prep.groupby(combo, observed=True)
            df_combo_output = self.objective_function(df_grp_by_combo)

            df_grp_nrows = df_grp_by_combo.size().reset_index(name="n_rows")

            combination_output_df = df_grp_nrows.merge(df_combo_output, on=combo)

            combination_output = {
                "combination": combo,
                "interaction_count": len(combo),
                "df": combination_output_df.reset_index(),
            }
            combination_outputs.append(combination_output)
        print("\n")
        self.hsa_raw_output_dicts = combination_outputs

    def process_hsa_raw_output_dicts(self):
        if not self.hsa_output_df.empty:
            print("The HSA data output already exsists.")
            return

        if self.hsa_raw_output_dicts is None:
            self.run_obj_func_iterations()

        combo_dfs = []
        for row_i, _ in enumerate(self.hsa_raw_output_dicts):
            combo_i_dict = self.hsa_raw_output_dicts[row_i]

            combo_i_combination = combo_i_dict["combination"]
            combo_i_interaction_count = combo_i_dict["interaction_count"]
            combo_i_df = combo_i_dict["df"]
            combo_i_df_rows = len(combo_i_df)

            combo_i_df_obj_func_calcs = lists.find_items(
                combo_i_df.columns,
                combo_i_combination,
                return_matching=False,
            )

            #! Below we transform the keys & values into a dict
            combo_i_df["combo_keys"] = pd.Series(
                [combo_i_combination] * combo_i_df_rows
            )
            combo_i_df["combo_values"] = combo_i_df[combo_i_combination].apply(
                lambda row: list(row.values.astype(str)), axis=1
            )

            combo_i_df["combo_dict"] = lists.lists_to_zipped_dict(
                combo_i_df["combo_keys"],
                combo_i_df["combo_values"],
            )

            combo_i_df.drop(
                columns=["combo_keys", "combo_values"],
                inplace=True,
            )

            combo_i_df["interaction_count"] = combo_i_interaction_count

            hsa_columns = list(
                # Dynamically grab the HSA columns using sets
                # NOTE: This preserves the column order
                set(combo_i_df.columns)
                - set(combo_i_df_obj_func_calcs)
                - set(combo_i_combination)
            )

            column_order = hsa_columns + combo_i_df_obj_func_calcs

            combo_i_df_final = combo_i_df[column_order]
            combo_dfs.append(combo_i_df_final)

        hsa_df = pd.concat(combo_dfs).reset_index(drop=True)
        self.hsa_output_df = hsa_df

    def pop_pre_grouped_vars(self):
        #!! move into process_hsa_raw_output_dicts() at end
        # TODO: once moved add a condition that the following var is not None

        if self.pre_grouped_vars is None:
            # no changes if input data is not grouped
            return

        group_by_dicts: list[dict] = []
        for _, combo_dict_i in enumerate(self.hsa_output_df["combo_dict"]):
            group_by_dict = general.pop_keys(combo_dict_i, self.pre_grouped_vars)
            group_by_dicts.append(group_by_dict)

        self.hsa_output_df["group_by_dict"] = group_by_dicts

        # Now reorder the columns so our grouped
        all_columns_with_dupes = ["group_by_dict"] + list(self.hsa_output_df.columns)
        all_columns_ordered = lists.unique(all_columns_with_dupes)
        self.hsa_output_df = self.hsa_output_df[all_columns_ordered]

    def run_hsa(self):
        self.process_hsa_raw_output_dicts()
        self.pop_pre_grouped_vars()
        print("HSA has been run & the output has been processed.")

    def export_hsa_output_df(self):
        if self.hsa_output_df.empty:
            raise ValueError(
                "hsa_output_df is not defined. Try: running run_hsa() then use this command."
            )
        return self.hsa_output_df

    def search_hsa_output(
        self,
        hsa_df: pd.DataFrame = pd.DataFrame(None),
        search_across: str = "keys",
        search_terms: str | list[str] = None,
        search_type: str = "any",
        interactions: int | list[int] = [0],  # default defined below
        n_row_minimum: int = 0,
    ):
        # TODO: add check to see if 'self.hsa_output_df' is defined.
        if hsa_df.empty:
            hsa_df = self.hsa_output_df.copy()

        if isinstance(interactions, int):
            interactions = [interactions]
        if interactions == [0]:
            # default to all possible interactions
            interactions = list(np.arange(self.interaction_limit) + 1)

        df = hsa_df[
            (hsa_df["interaction_count"].isin(interactions))
            & (hsa_df["n_rows"] >= n_row_minimum)
        ].copy()
        df.reset_index(inplace=True, drop=True)

        is_grouped_hsa = "group_by_dict" in df.columns
        if is_grouped_hsa:
            # If grouped we union our output dict column
            df["hsa_dict"] = lists.zip_lists_of_dicts(
                df["group_by_dict"], df["combo_dict"]
            )
        else:
            df["hsa_dict"] = hsa_df["combo_dict"]

        if isinstance(search_terms, str):
            search_terms = [search_terms]
        search_terms = sorted(search_terms)

        #! START - TODO: migrate the following into a util func
        search_types = ["any", "all"]
        if search_type not in search_types:
            raise ValueError(f"'search_type' must be either: {search_types}")
        #! END

        search_across_types = ["keys", "values"]
        search_vector = []
        if search_across not in search_across_types:
            raise ValueError(f"'type' must be equal to either {search_across_types}")
        elif search_across == "keys":
            search_vector = [list(x.keys()) for x in df["hsa_dict"]]
        elif search_across == "values":
            search_vector = [list(x.values()) for x in df["hsa_dict"]]

        if search_type == "all":
            search_results_bool = [search_terms == sorted(x) for x in search_vector]
        else:
            search_results_interim = [
                lists.find_items(search_terms, x, return_bools=True)
                for x in search_vector
            ]
            search_results_bool = [any(x) for x in search_results_interim]

        search_results = df[search_results_bool]

        # If we have valid results return them else
        if len(search_results) > 0:
            return search_results.drop(columns="hsa_dict")
        else:
            if is_grouped_hsa:
                extra_msg_search_across = " & group_by_dict"
            else:
                extra_msg_search_across = ""

            msg_search_terms = ",".join(["'" + x + "'" for x in search_terms])
            msg_interactions = ",".join(map(str, interactions))
            search_failed_helper = (
                "0 search results with the following parameters:"
                + "\n\n\t"
                + f"search_across: '{search_across}' within 'combo_dict"
                + extra_msg_search_across
                + "'"
                + "\n\t"
                + f"search_terms: {msg_search_terms}"
                + "\n\t"
                + f"search_type: '{search_type}' of the search_terms"
                + "\n\t"
                + f"interactions: {msg_interactions}"
                + "\n\n"
            )
            raise ValueError(search_failed_helper)


# %%

df_tips = sns.load_dataset("tips")
numbers = np.arange(10)
df_tips_plus = []
for i, _ in enumerate(numbers):
    scalar = i + 1
    df_tips_temp = pd.concat([df_tips] * scalar).reset_index(drop=True)
    df_tips_temp["tip"] += scalar * 1.0
    df_tips_temp["timestamp"] = pd.Series([scalar] * len(df_tips_temp))
    df_tips_plus.append(df_tips_temp)

df_tips_plus: pd.DataFrame = pd.concat(df_tips_plus)

# %%

#! Feature construction + aggregation function!
df_tips_plus["tip_perc"] = df_tips_plus["tip"] / df_tips_plus["total_bill"]


def tip_stats(data: pd.DataFrame) -> pd.DataFrame:
    """fake"""
    tmp = data.agg(
        count_tips=pd.NamedAgg("tip", "count"),
        avg_tips=pd.NamedAgg("tip", "mean"),
        avg_tip_perc=pd.NamedAgg("tip_perc", "mean"),
    ).round(2)

    return tmp


HSA = HotSpotAnalysis(
    # data=df_tips_plus.groupby(["sex", "timestamp"], observed=True),
    data=df_tips_plus.groupby("timestamp", observed=True),
    # data=df_tips_plus,
    target_cols=["day", "smoker", "size"],
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
    search_terms="Thur", search_across="values", search_type="any", interactions=2
)

# %%
HSA.search_hsa_output(
    search_terms="Yes",
    search_across="values",
    search_type="any",
    n_row_minimum=50,
)

# %%

# HSA.search_hsa_output(search_terms="smoker", search_across="keys", search_type="all")

# HSA.search_hsa_output(search_terms=["smoker", "day"], search_across="keys", search_type="all")

# HSA.search_hsa_output(search_terms="smoker", search_across="keys", interactions=1)

# HSA.search_hsa_output(search_terms=["Male", "Yes"], search_across="values", search_type="all")

# HSA.search_hsa_output(search_terms=["Fri", "Yes"], search_across="values", search_type="all")

# %%


#! Test chain laggin using group_combo

hsa_data.head()

df_combo = HSA.search_hsa_output(
    search_terms=["Fri", "Thur"],
    search_across="values",
    search_type="any",
    interactions=2,
)
df_combo

#!! Below is a way to join lags using groupby as a defacto timeseries
# 1. convert dict to a hashable type (JSON)
# 2. use shift() to shift the data to be lag 1 (using index)
# 3. left join shifted (lagged) data onto original (using index)

import json

df_combo["group_by_dict"] = [json.dumps(x) for x in df_combo["group_by_dict"]]
df_combo["combo_dict"] = [json.dumps(x) for x in df_combo["combo_dict"]]

df_combo_shifted = df_combo.groupby(["combo_dict", "interaction_count"]).shift(1)
df_combo_shifted


# %%
df_combo.merge(
    df_combo_shifted,
    how="left",
    left_index=True,
    right_index=True,
    suffixes=["", "_lag1"],
).head(6)


# df_combo.merge()


# %%
