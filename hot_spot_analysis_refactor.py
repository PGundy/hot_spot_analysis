# %%
from dataclasses import dataclass
from typing import Callable

import numpy as np
import pandas as pd
import seaborn as sns

from utils2 import combos, grouped_df, lists


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
        """If the user's data is grouped we resolve that here."""
        if grouped_df.is_grouped(self.data_input):
            self.pre_grouped_vars = grouped_df.get_groups(self.data_input)
            print(f"Input data is grouped by: {self.pre_grouped_vars}")

        self.data_prep = grouped_df.return_data(self.data_input)

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

        if len(self.data_prep) > row_limit:
            if verbose:
                print(f"Using random sample of {row_limit} rows")
            test_df = self.data_prep.sample(row_limit)
        else:
            test_df = self.data_prep

        try:
            output = self.objective_function(test_df.groupby("Overall"))
        except:
            raise ValueError(
                "The function supplied to 'objective_function' is not compatible\n\nThe function must worked on grouped data frames, and thus all feature engineering must be done in the agg() or subsequently."
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
            pass

        combination_outputs = []
        print("\n")
        for step_i, combo in enumerate(self.combinations):
            print(f"\tstep: {step_i} group by {combo}")
            df_grp_by_combo = self.data_prep.groupby(combo, observed=True)
            df_combo_output = self.objective_function(df_grp_by_combo)
            combination_output = {
                "combination": combo,
                "interaction_count": len(combo),
                "df": df_combo_output,
            }
            combination_outputs.append(combination_output)
        print("\n")
        self.hsa_raw_output_dicts = combination_outputs

    def process_hsa_raw_output_dicts(self):
        if not self.hsa_output_df.empty:
            print("The raw HSA data output has already been processed.")
            pass

        if self.hsa_raw_output_dicts is None:
            self.run_obj_func_iterations()

        hsa_dfs = []
        for row_i, _ in enumerate(self.hsa_raw_output_dicts):
            combo_i_dict = self.hsa_raw_output_dicts[row_i]

            combo_combination = combo_i_dict["combination"]
            combo_interaction_count = combo_i_dict["interaction_count"]
            combo_df = combo_i_dict["df"]
            combo_df_rows = len(combo_df)

            # This method with a for loop should preserve column order b/c sets do NOT preserve ordering!
            combo_df_obj_func_calcs = []
            for col in combo_df.columns:
                if col in combo_combination:
                    pass
                else:
                    combo_df_obj_func_calcs.append(col)
            combo_df_obj_func_calcs

            # return combo_i_dict

            combo_df["interaction_count"] = combo_interaction_count
            combo_df["combo_keys"] = pd.Series([combo_combination] * combo_df_rows)
            combo_df["combo_values"] = combo_df[combo_combination].apply(
                lambda row: list(row.values.astype(str)), axis=1
            )

            combination_dicts = []
            for row in range(combo_df_rows):
                combination_dict = dict(
                    zip(
                        combo_df["combo_keys"][row],
                        combo_df["combo_values"][row],
                    )
                )
                combination_dicts.append(combination_dict)

            combo_df["combo_dict"] = combination_dicts
            combo_df.drop(
                columns=["combo_keys", "combo_values"],
                inplace=True,
            )

            hsa_columns = list(
                # Dynamically grab the HSA columns using sets
                set(combo_df.columns)
                - set(combo_df_obj_func_calcs)
                - set(combo_combination)
            )
            hsa_columns.sort()

            column_order = hsa_columns + combo_df_obj_func_calcs

            combo_df_final = combo_df[column_order]
            hsa_dfs.append(combo_df_final)

        hsa_df = pd.concat(hsa_dfs)
        # hsa_df = hsa_df.reset_index(names=["combo_index"])
        hsa_df = hsa_df.reset_index(drop=True)
        self.hsa_output_df = hsa_df

    def pop_pre_grouped_vars(self):
        grp_vars = self.pre_grouped_vars

        group_combo_dicts: list[dict] = []
        for _, combo_dict_i in enumerate(self.hsa_output_df["combo_dict"]):
            group_combo_dict = {}
            if grp_vars is not None:
                for grp_var in grp_vars:
                    group_combo_dict[grp_var] = combo_dict_i.pop(grp_var)

            group_combo_dicts.append(group_combo_dict)

        self.hsa_output_df["group_combo_dict"] = group_combo_dicts

        # Now reorder the columns so our grouped
        all_columns_with_dupes = ["group_combo_dict"] + list(self.hsa_output_df.columns)
        all_columns_ordered = lists.unique(all_columns_with_dupes)
        self.hsa_output_df = self.hsa_output_df[all_columns_ordered]

    def run_hsa(self):
        self.process_hsa_raw_output_dicts()
        if self.pre_grouped_vars is not None:
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
        interactions: int | list[int] = [0],  # default defined below
        search_type: str = "any",
    ):
        # TODO: add check to see if 'self.hsa_output_df' is defined.
        if hsa_df.empty:
            hsa_df = self.hsa_output_df

        if "group_combo_dict" in hsa_df.columns:
            hsa_dict = []
            for i in range(len(hsa_df)):
                hsa_dict.append(hsa_df.group_combo_dict[i] | hsa_df.combo_dict[i])
            hsa_df["hsa_dict"] = hsa_dict
        else:
            hsa_df["hsa_dict"] = hsa_df["combo_dict"]

        if isinstance(search_terms, str):
            search_terms = [search_terms]
        search_terms = sorted(search_terms)

        if isinstance(interactions, int):
            interactions = [interactions]
        if interactions == [0]:
            interactions = list(np.arange(self.interaction_limit) + 1)

        search_types = ["any", "all"]
        if search_type not in search_types:
            raise ValueError(f"'search_type' must be either: {search_types}")

        hsa_df_subset = hsa_df[hsa_df["interaction_count"].isin(interactions)]

        search_across_types = ["keys", "values"]
        if search_across not in search_across_types:
            search_vector = None
            raise ValueError(f"'type' must be equal to either {search_across_types}")
        elif search_across == "keys":
            search_vector = [list(x.keys()) for x in hsa_df_subset["hsa_dict"]]
        elif search_across == "values":
            search_vector = [list(x.values()) for x in hsa_df_subset["combo_dict"]]

        if search_type == "all":
            search_results_bool = [search_terms == sorted(x) for x in search_vector]
        else:
            search_results_interim = [
                lists.find_items(search_terms, x, return_bools=True)
                for x in search_vector
            ]
            search_results_bool = [any(x) for x in search_results_interim]

        search_results = hsa_df_subset[search_results_bool]

        if len(search_results) > 0:
            return search_results
        else:
            print("0 results. Please try again.")


# %%

df_tips = sns.load_dataset("tips")
numbers = np.arange(10)
df_tips_plus = []
for i, _ in enumerate(numbers):
    # print(i)
    df_tips_temp = df_tips.copy()
    df_tips_temp["letter"] = pd.Series([i] * len(df_tips_temp))
    df_tips_plus.append(df_tips_temp)

df_tips_plus: pd.DataFrame = pd.concat(df_tips_plus)

# %%


#! Feature construction + aggregation function!
df_tips_plus["tip_perc"] = df_tips_plus["tip"] / df_tips_plus["total_bill"]


def tip_stats(data: pd.DataFrame) -> pd.DataFrame:
    """fake"""
    tmp = (
        data.agg(
            count_tips=pd.NamedAgg("tip", "count"),
            avg_tips=pd.NamedAgg("tip", "mean"),
            avg_tip_perc=pd.NamedAgg("tip_perc", "mean"),
        )
        .round(2)
        .reset_index()
    )

    return tmp


HSA = HotSpotAnalysis(
    # data=df_tips_plus.groupby(["sex", "size"], observed=True),
    # data=df_tips_plus.groupby("sex", observed=True),
    data=df_tips_plus,
    target_cols=["day", "smoker", "letter"],
    interaction_limit=3,
    objective_function=tip_stats,
)

# HSA.prep_analysis()
# HSA.test_objective_function(verbose=False)
HSA.run_hsa()
hsa_data = HSA.export_hsa_output_df()
hsa_data.head(10)


# %%
HSA.search_hsa_output(search_terms="Yes", search_across="values", search_type="any")
HSA.search_hsa_output(search_terms="smoker", search_across="keys", search_type="all")
HSA.search_hsa_output(
    search_terms=["smoker", "day"], search_across="keys", search_type="all"
)
HSA.search_hsa_output(search_terms="smoker", search_across="keys", interactions=1)
HSA.search_hsa_output(
    search_terms=["Male", "Yes"], search_across="values", search_type="all"
)


# %%


test = pop_pre_grouped_vars()
test

# %%
