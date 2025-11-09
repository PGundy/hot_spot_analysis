from dataclasses import dataclass
from typing import Callable, Union

import numpy as np
import pandas as pd

from hot_spot_analysis.utils import combos, demo, general, grouped_df, lists


@dataclass
class HotSpotAnalyzer:
    """HotSpotAnalyzer will help you find hotspots within your data by letting you easily drill down into your data.

    Attributes:
    -----------
    data : pd.DataFrame
        The dataset to be analyzed. Defaults to an empty DataFrame.
    target_cols : list[str]
        The target columns within the dataset to focus the analysis on.
    interaction_limit : int
        The maximum number of interactions to consider during the analysis.
    objective_function : Callable
        A function to evaluate the objective of the analysis.
    """

    data: pd.DataFrame
    target_cols: list[str]
    interaction_limit: int
    objective_function: Callable

    def __init__(
        self,  # Default values
        data: pd.DataFrame = pd.DataFrame(None),  # HSA.data.empty -> True
        target_cols: list = [None],  # []
        time_period: list = [None],  # []
        interaction_limit: int = 3,  # 3
        objective_function: Callable = None,  # type: ignore
    ):
        self.data_input = data
        self.target_cols = lists.unique(target_cols, drop_none=True)  # type: ignore
        self.time_period = lists.unique(time_period, drop_none=True)
        self.interaction_limit = interaction_limit
        self.objective_function = objective_function

        # Set defaults for variables set via functions
        self.grouped_by: list[str] = None  # type: ignore
        self.data_prep: pd.DataFrame = pd.DataFrame(None)
        self.combinations: list[list[str]] = None  # type: ignore
        self.obj_func_tested: bool = False
        self.hsa_raw_output_dicts: list[dict] = None  # type: ignore
        self.hsa_output_df: pd.DataFrame = pd.DataFrame(None)

    def _prep_class(self):
        """Extract any groups & the dataframe from the init"""
        self.data_prep = grouped_df.return_data(self.data_input)

        if grouped_df.is_grouped(self.data_input):
            self.grouped_by = grouped_df.get_groups(self.data_input)

    def _validate_input(self, validate=None):
        """Check if the target_cols are found in the input data.

        Parameters:
        -----------
        validate : str, optional
            The input type to validate, either 'target_cols' or 'time_period'.

        Raises:
        -------
        ValueError
            If the input columns are not found in the data_prep dataframe.
        """

        if validate == "target_cols":
            input_to_validate = self.target_cols
        elif validate == "time_period":
            if not self.time_period:
                return
            input_to_validate = self.time_period
        else:
            raise ValueError("validate must be either: 'target_cols' or 'time_period")

        valid_inputs = list(self.data_prep.columns)

        valid_columns_bools = lists.find_items(
            input_to_validate,
            valid_inputs,
            return_bools=True,
        )

        if not all(valid_columns_bools):
            invalid_inputs = lists.find_items(
                input_to_validate,
                valid_inputs,
                return_matching=False,
            )

            error = f"""'{validate}' contains an invalid input. Resolve the following:
            
            Problematic '{validate}': {', '.join(invalid_inputs)}
            Valid inputs: {', '.join(valid_inputs)}
            """
            raise ValueError(error)

    def _build_combos(self):
        """Build combinations of the target columns and other grouping variables."""
        if self.data_prep.empty:
            self._prep_class()

        combinations = combos.create_combos(
            target_cols=self.target_cols,
            interaction_max=self.interaction_limit,
        )

        combinations = [["Overall"]] + combinations

        if self.grouped_by is not None:
            # If the input data is grouped we add the groups!
            combinations = grouped_df.add_groups_to_combos(
                group_vars=self.grouped_by,
                combos=combinations,
            )

        if self.time_period:
            combinations = grouped_df.add_groups_to_combos(
                group_vars=self.time_period,
                combos=combinations,
            )

        self.combinations = combinations

        print(
            f"Combinations have been generated. There are {len(combinations)} across the target variables: {','.join(self.target_cols)}"
        )

    def _build_data(self):
        """Prepare the data for analysis by validating inputs and adding necessary columns."""
        if self.data_prep.empty:
            self._prep_class()

        self._validate_input("target_cols")
        self._validate_input("time_period")

        self.data_prep["Overall"] = "Overall"
        print("Data passed checks, and is ready for analysis.")

    def test_objective_function(
        self,
        row_limit: int = 100,
        verbose: bool = True,
    ):
        """Test if the objective function works with the data.

        Parameters:
        -----------
        row_limit : int, optional
            The number of rows to sample for testing. Defaults to 100.
        verbose : bool, optional
            If True, prints additional information during testing. Defaults to True.

        Raises:
        -------
        ValueError
            If the objective function is not compatible with the grouped data frame.
        """
        if self.data_prep.empty:
            self._build_data()

        if verbose:
            print(
                f"Using random sample of {row_limit} rows. Note that rows will be recycled to meet row_limit if data has insufficient rows."
            )

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

    def _prep_analysis(self):
        """Prepare the data and combinations for analysis, and test the objective function."""
        self._build_data()
        self._build_combos()
        if not self.obj_func_tested:
            self.test_objective_function(verbose=False)

    def _run_obj_func_iterations(self):
        """Run the objective function across all combinations of the data."""
        self._prep_analysis()

        if self.hsa_raw_output_dicts is not None:
            print("The objective function has already been run.")

        combination_outputs = []
        print("\n")
        for step_i, combo in enumerate(self.combinations):
            print(f"\tstep: {step_i} group by {combo}")
            df_grp_by_combo = self.data_prep.groupby(combo, observed=True)
            df_combo_output = self.objective_function(df_grp_by_combo)

            df_grp_nrows = df_grp_by_combo.size().reset_index(name="n_rows")  # type: ignore

            combination_output_df = df_grp_nrows.merge(df_combo_output, on=combo)

            if "Overall" in combo:
                interaction_count = len(combo) - 1
            else:
                interaction_count = len(combo)

            combination_output = {
                "combination": combo,
                "interaction_count": interaction_count,
                "df": combination_output_df.reset_index(drop=True),
            }
            combination_outputs.append(combination_output)
        print("\n")
        self.hsa_raw_output_dicts = combination_outputs

    def _process_hsa_raw_output_dicts(self):
        """Process the raw output dictionaries to create the final HSA output dataframe."""
        if not self.hsa_output_df.empty:
            print("The HSA data output already exsists.")
            return

        if self.hsa_raw_output_dicts is None:
            self._run_obj_func_iterations()

        combo_dfs = []
        for row_i, _ in enumerate(self.hsa_raw_output_dicts):
            combo_i_dict = self.hsa_raw_output_dicts[row_i]

            combo_i_combination = combo_i_dict["combination"]
            combo_i_df = combo_i_dict["df"]
            combo_i_df["interaction_count"] = combo_i_dict["interaction_count"]

            combo_i_df_obj_func_calcs = lists.find_items(
                combo_i_df.columns,
                combo_i_combination,
                return_matching=False,
            )

            #! Create combo_dict directly from row data without temporary columns
            combo_i_df["combo_dict"] = combo_i_df[combo_i_combination].apply(
                lambda row: dict(zip(combo_i_combination, row.values.astype(str))),
                axis=1,
            )

            #! Now we dynamically grab hsa cols & reorder
            hsa_columns = list(
                # Dynamically grab the HSA columns using sets
                # NOTE: This preserves the column order
                set(combo_i_df.columns)
                - set(combo_i_df_obj_func_calcs)
                - set(combo_i_combination)
            )
            hsa_columns.sort()

            column_ordered = hsa_columns + combo_i_df_obj_func_calcs

            combo_i_df_final = combo_i_df[column_ordered]
            combo_dfs.append(combo_i_df_final)

        hsa_df = pd.concat(combo_dfs).reset_index(drop=True)
        self.hsa_output_df = hsa_df

    def _pop_key_off_combo_dict(self, pop_type=None):
        """Pop a key off the combination dictionary.

        Parameters:
        -----------
        pop_type : str, optional
            The type of key to pop, either 'grouped_by' or 'time_period'.

        Raises:
        -------
        ValueError
            If the pop_type is not 'grouped_by' or 'time_period'.
        """

        if pop_type == "grouped_by":
            if self.grouped_by is None:
                return
            pop_key = self.grouped_by
            pop_dict = "grouped_by_dict"
        elif pop_type == "time_period":
            if not self.time_period:
                return
            pop_key = self.time_period
            pop_dict = "time_period_dict"
        else:
            raise ValueError("Invalid pop_type. Must be either: 'grouped_by' or 'time_period'")

        popped_dicts = []
        for _, combo_dict_i in enumerate(self.hsa_output_df["combo_dict"]):
            popped_dict = general.pop_keys(combo_dict_i, pop_key)
            popped_dicts.append(popped_dict)

        self.hsa_output_df[pop_dict] = popped_dicts

        # Reorder columns to have time_period then all others
        all_columns_with_dupes = [pop_dict] + list(self.hsa_output_df.columns)
        all_columns_ordered = lists.unique(all_columns_with_dupes)
        self.hsa_output_df = self.hsa_output_df[all_columns_ordered]

    def run_hsa(self):
        """Process all inputs, and then run HotSpotAnalyzer."""
        self._process_hsa_raw_output_dicts()
        self._pop_key_off_combo_dict(pop_type="grouped_by")
        self._pop_key_off_combo_dict(pop_type="time_period")
        print("HSA has been run & the output has been processed.")

    def lag_hsa_by_time_period(
        self,
        lag_iterations: Union[int, list[int]] = [1],
    ) -> pd.DataFrame:
        """Lag the HSA output by the specified time period to see time trends.

        Parameters:
        -----------
        lag_iterations : Union[int, list[int]], optional
            The number of lag iterations to apply. Defaults to [1].

        Returns:
        --------
        pd.DataFrame
            The lagged HSA output dataframe.

        Raises:
        -------
        TypeError
            If the data provided to HSA was not grouped.
        """

        # NOTE: This lag operations requires hashable, so we convert list(dict) --> JSON, compute the lags & merge, JSON -->  dict(list)

        if not self.time_period:
            return TypeError("Data provided to HSA was not grouped.")
        if isinstance(lag_iterations, int):
            lag_iterations = [lag_iterations]

        df = self.hsa_output_df.copy()

        lag_across = ", ".join(self.time_period)
        print(f"Attempting to lag data across: {lag_across}")

        dict_columns = ["combo_dict"]
        if self.grouped_by is not None:
            dict_columns = ["grouped_by_dict"] + dict_columns
        for dict_column in dict_columns:
            df[dict_column] = general.dict_to_json(df[dict_column])  # type: ignore

        # Loop through the lags & merge them back into df.
        df_baseline = df.copy()  # copy() is required to keep the objects separate
        for lag_i in lag_iterations:
            print(f"Running lag: {lag_i}")
            df_lag_i = df_baseline.groupby(["combo_dict", "interaction_count"]).shift(lag_i)

            df = df.merge(
                df_lag_i,
                how="left",
                left_index=True,
                right_index=True,
                suffixes=("", f"_lag{lag_i}"),
            )

        for dict_column in dict_columns:
            df[dict_column] = general.json_to_dict(df[dict_column])  # type: ignore

        return df

    def export_hsa_output_df(self) -> pd.DataFrame:
        """Export the HSA output dataframe.

        Returns:
        --------
        pd.DataFrame
            The HSA output dataframe.

        Raises:
        -------
        ValueError
            If the HSA output dataframe is not defined.
        """
        if self.hsa_output_df.empty:
            raise ValueError("hsa_output_df is not defined. Try: running run_hsa() then use this command.")
        return self.hsa_output_df

    def search_hsa_output(
        self,
        hsa_df: pd.DataFrame = pd.DataFrame(None),
        search_terms: Union[str, list[str]] = None,  # type: ignore
        search_across: str = "keys",
        search_type: str = "any",
        interactions: Union[int, list[int]] = [0],  # default defined below
        n_row_minimum: int = 0,
    ) -> pd.DataFrame:
        """Search across the HSA output dataframe for specific keys(columns) or values.

        Parameters:
        -----------
        hsa_df : pd.DataFrame, optional
            The HSA output dataframe to search within. Defaults to an empty DataFrame.
        search_terms : Union[str, list[str]], optional
            The terms to search for. Defaults to None.
        search_across : str, optional
            Whether to search across 'keys' or 'values'. Defaults to 'keys'.
        search_type : str, optional
            The type of search to perform, either 'any' or 'all'. Defaults to 'any'.
        interactions : Union[int, list[int]], optional
            The interaction levels to consider during the search. Defaults to [0].
        n_row_minimum : int, optional
            The minimum number of rows to include in the search. Defaults to 0.

        Returns:
        --------
        pd.DataFrame
            The search results.

        Raises:
        -------
        UserWarning
            If the HSA output dataframe is not defined.
        ValueError
            If the search parameters are invalid or no results are found.
        """

        if hsa_df.empty:
            if self.hsa_output_df.empty:
                raise UserWarning("You must first run: run_hsa()")
            hsa_df = self.hsa_output_df.copy()

        if isinstance(interactions, int):
            interactions = [interactions]
        if interactions == [0]:
            # default to all possible interactions
            interactions = list(np.arange(self.interaction_limit) + 1)

        df = hsa_df[(hsa_df["interaction_count"].isin(interactions)) & (hsa_df["n_rows"] >= n_row_minimum)].copy()
        df.reset_index(inplace=True, drop=True)

        has_grouped_by_dict = "grouped_by_dict" in df.columns
        has_time_period_dict = "time_period_dict" in df.columns

        df["hsa_dict"] = df["combo_dict"]
        if has_grouped_by_dict:
            df["hsa_dict"] = lists.zip_lists_of_dicts(df["grouped_by_dict"], df["hsa_dict"])
        if has_time_period_dict:
            df["hsa_dict"] = lists.zip_lists_of_dicts(df["time_period_dict"], df["hsa_dict"])

        if isinstance(search_terms, str):
            search_terms = [search_terms]
        search_terms = sorted(search_terms)

        #! START - TODO: migrate the following into a util func
        search_types = ["any", "all"]
        if search_type not in search_types:
            raise ValueError(f"'search_type' must be either: {search_types}")
        #! END

        search_vector = []
        if search_across in ["key", "value"]:
            print("Update search_across to 'keys' or 'values'")
            search_across = search_across + "s"
        if search_across == "keys":
            search_vector = [list(x.keys()) for x in df["hsa_dict"]]
        elif search_across == "values":
            search_vector = [list(x.values()) for x in df["hsa_dict"]]
        else:
            raise ValueError("search_across must be either: 'keys' or 'values'")

        if search_type == "all":
            search_results_bool = [search_terms == sorted(x) for x in search_vector]
        else:
            search_results_interim = [lists.find_items(search_terms, x, return_bools=True) for x in search_vector]
            search_results_bool = [any(x) for x in search_results_interim]

        search_results = df[search_results_bool]

        # If we have valid results return them else
        if len(search_results) > 0:
            return search_results.drop(columns="hsa_dict")
        else:
            if has_time_period_dict:
                extra_msg_search_across = " & time_period_dict"
            if has_grouped_by_dict:
                extra_msg_search_across = " & grouped_by_dict"
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
                + "\n\t"
                + f"n_row_minimum: {n_row_minimum}"
            )
            raise ValueError(search_failed_helper)
