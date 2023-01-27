# %%
import itertools
import warnings

import numpy as np
import pandas as pd

# %%


class HotSpotAnalysis:
    data: pd.DataFrame
    data_cuts: list
    depth_limit: int
    _combinations: list
    dataCombos: pd.DataFrame

    def __init__(
        self,  # Default values
        data=pd.DataFrame(None),  # HSA.data.empty -> True
        data_cuts=list(),  # []
        depth_limit=int(),  # 0
        _combinations=list(),  # []
        _outputHSA=pd.DataFrame(None),  # HSA.data.empty -> True
    ):
        self.data = data
        self.data_cuts = data_cuts
        self.depth_limit = depth_limit
        self._combinations = _combinations
        self._outputHSA = _outputHSA

    def _is_data_grouped(self):
        """
        Check if the data argument is grouped.
        Returns boolean.
        """
        return hasattr(self.data, "groups")

    def _get_data_group_by(self):
        """
        Gets the groupby arguments from the data argument.
        Returns list.
        """
        if self._is_data_grouped():
            group_vars = self.data.keys
            if type(group_vars) == str:
                group_vars = [group_vars]

            return group_vars
        else:
            return [None]

    # Modify pd.DataFrame.groupby() to add to pre-grouped DataFrames
    def _add_to_groupby(self, input_list: list):
        """
        Modified version of pd.groupby() where it preserves the groups as
        supplied by the user while cycling through the
        hot spot analysis groups.

        Returns a dataframe with modified groups.
        """
        # list <- list of vars to group by
        if not self._is_data_grouped():
            df = self.data
            grpVarList = input_list
        else:
            df = self.data.obj
            inputGrps = self._get_data_group_by()

            if len(inputGrps) > 1:
                inputGrps = list(itertools.chain(*[inputGrps]))

            grpVarList = inputGrps + input_list
            grpVarList = self._make_list_unique(grpVarList)

        return df.groupby(grpVarList)

    def _remove_none_in_list(self, input_list: list):
        """
        Remove None from a list of values.
        Returns all values except None.
        """
        if None in input_list:
            input_list.remove(None)
        return input_list

    def _validate_inputs(self):
        """
        Checks all user inputs and print a message to resolve invalid entries.
        Returns boolean.
        """
        validInputs = None
        if self.data_cuts == []:
            print("data_cuts is empty.")
            validInputs = False

        elif self.depth_limit <= 0:
            print("depth_limit is invalid.")
            validInputs = False

        # Check if empty exists, then when not empty -> valid
        elif hasattr(self.data, "empty"):
            if self.data.empty:
                print("data is empty.")

            validInputs = not self.data.empty

        # If the object has a groups method we assume data is not empty
        elif hasattr(self.data, "groups"):
            print(
                f"""
                  data appears valid but is grouped.\n
                  {self.data.keys}: {list(self.data.groups.keys())}
                  """
            )
            validInputs = hasattr(self.data, "groups")

        else:
            validInputs = True
        return validInputs

    # get the list of alphanumerically sorted combinations
    def _create_combos(self):
        """
        Creates the interaction combinations using the data_cuts input
        with an interaction maximum governed by depth_limit.

        Returns nothing; Updates 'self._combinations'.
        """

        if not self._validate_inputs():
            raise ValueError("Ensure all parameters have been set.")

        self.data_cuts.sort()

        # define the interim objects
        combination_final = []

        for i in np.arange(0, self.depth_limit, 1) + 1:
            combinations = list(
                itertools.combinations(self.data_cuts, int(i))
            )
            combinations = list(map(list, combinations))
            combinations.sort()

            # Build up nested list of all combinations
            combination_final = [*combination_final, combinations]

            if i == self.depth_limit:
                # unnest the combinations
                combination_final = list(
                    itertools.chain.from_iterable(combination_final)
                )
                self._combinations = list(filter(None, combination_final))

            if self._is_data_grouped():
                self._combinations = [
                    self._get_data_group_by()
                ] + self._combinations

    def get_combos(self):
        """
        Runs self._create_combos() and returns a list of lists where
        each item is a combination that will be used in the hot spot analysis.

        Returns a list.
        """
        if self._combinations == []:
            self._create_combos()

        print(
            "In total there are",
            len(self._combinations),
            "combinations with a depth_limit max of",
            self.depth_limit,
        )

        return self._combinations

    def _make_list_unique(self, input_list: list):
        """
        Remove duplicates, but preserve the order of the items as they are
        found in the input list. This is required as set() does this,
        but reordered the items in the input list.

        Returns a list.
        """
        # normally we would use set(), but that orders the input.
        # Thus we use list comprehension to return the as-ordered list.
        unique_list = []
        for item in input_list:
            if item not in unique_list:
                unique_list.append(item)
        return unique_list

    def test_user_agg_function(self, user_agg_function):
        """
        Run the user_agg_function on the data provided. If not
        grouped it creates a constant 'All Rows' to maintain
        a consistent data structure as the hot spot
        analysis output.

        Returns a pd.DataFrame.
        """
        if self._is_data_grouped():
            data = self.data.obj
        else:
            data = self.data

        data["All Rows"] = "All Rows"
        grouping_vars = ["All Rows"] + self._get_data_group_by()
        grouping_vars = self._remove_none_in_list(grouping_vars)
        data = data.groupby(grouping_vars)

        print("\n\nBelow is the output of the user_agg_function:")
        return user_agg_function(data)

    # Iterate using user_agg_function & data using groupby(Combos)
    def run_hsa(self, user_agg_function):
        """
        The primary function for user. This runs the entire
        hot spot analysis after creating the combos
        (and validating the inputs). The user will see
        each step print as it begins running to help monitor progress.

        Returns nothing; Creates self._outputHSA.
        """

        # Create the backbone of the analysis
        self._create_combos()

        resultList = []
        for step_i, grp_var_i in enumerate(self._combinations):

            dataObj = self._add_to_groupby(grp_var_i)
            grp_var_i_full = dataObj.keys

            print(
                "Step:",
                step_i,
                "of",
                len(self._combinations) - 1,
                " -- Grouped by:",
                grp_var_i_full,
            )

            # Run the calculations for each step
            result = []
            result = user_agg_function(dataObj)

            # Create variables to create 'clean' columns
            result_col_names = list(result.columns)
            result.reset_index(inplace=True)

            # !Create the easy to read variables
            # Count of interactions
            result["depth"] = len(grp_var_i_full)

            # pd.Series of list(relevant variable names)
            result["data_cuts"] = pd.Series([grp_var_i_full] * len(result))

            # pd.Series of the corresponding variable's values
            result["data_content"] = result[grp_var_i_full].apply(
                lambda row: list(row.values.astype(str)), axis=1
            )

            # Create the list zip("data_cuts","data_content")
            tmp_var_group_clean = []
            for row in np.arange(0, len(result), 1):

                # create empty pd.Series -- Then loop builds it
                if row == 0:
                    result["data_cut_content"] = pd.Series(dtype=object)
                #
                # KNOWN BUG WITH CHAINED INDEXING
                # TODO: Is this solvable with pd.Series of lists?
                #
                tmp_var_group_clean.append(
                    [
                        i + ": " + j + ""
                        for i, j in zip(
                            result["data_cuts"].iloc[row],
                            result["data_content"].iloc[row],
                        )
                    ]
                )

            result["data_cut_content"] = tmp_var_group_clean

            # Select & order our final columns
            result = result[
                list(
                    [
                        "depth",
                        "data_cuts",
                        "data_content",
                        "data_cut_content",
                    ]
                )
                + result_col_names
            ]

            # Final step - compile the aggregated object
            resultList.append(result)

        resultDataFrame = pd.concat(resultList).reset_index(drop=True)
        self._outputHSA = resultDataFrame

    # export the HotSpotAnalysis output dataframe
    def get_hsa_data(self):
        """
        Export _outputHSA after running hsa.run_hsa()

        Returns pd.DataFrame()
        """
        return self._outputHSA

    # convert list to string using a delimiter
    def _list_to_string(self, input_list: list):
        """
        Convert list into a string delimited by ' -- '.

        returns str.
        """
        delimiter = " -- "
        return delimiter.join(map(str, input_list))

    # convert delimited string back to a list
    def _string_to_list(self, string: str):
        """
        Convert string (delimited by ' -- ') into a list.

        returns list.
        """
        delimiter = " -- "
        return string.split(delimiter)

    # get the lowest level of useful interactions (1 or 1+[number of groups])
    def _get_useful_depth(self):
        """
        Get the useful level of depth for the hot spot analysis. Normally
        this is a depth of 1. However if the input data is grouped
        then it is formulaic by (number of grouping columns) + 1.

        Returns int.
        """
        useful_depth_level = self._get_data_group_by()
        if useful_depth_level == [None]:
            useful_depth_level = 1
        else:
            useful_depth_level = len(useful_depth_level) + 1
        return useful_depth_level

    def get_data_cuts(self):
        """
        Return the data_cuts at the most broad depth level.

        return pd.DataFrame.
        """
        key_variables = ["depth", "data_cuts"]
        filter_by = self._outputHSA["depth"].isin(
            [self._get_useful_depth()]
        )

        df_cuts = self._outputHSA[filter_by][key_variables]
        df_cuts["data_cuts"] = df_cuts["data_cuts"].apply(
            lambda x: self._list_to_string(x)
        )

        df_cuts = df_cuts.explode("data_cuts").value_counts().reset_index()
        df_cuts.columns = key_variables + ["unique_values"]
        df_cuts["data_cuts"] = df_cuts["data_cuts"].apply(
            lambda x: self._string_to_list(x)
        )

        return df_cuts

    def get_data_content(self, data_cut=None):
        """
        Return the data_content for the provided data_cut. If no data_cut
        is provided then it returns the possible and valid data_cuts.

        return pd.DataFrame.
        """
        if isinstance(data_cut, str):
            data_cut = [data_cut]

        if data_cut is None:
            output_data = self.get_data_cuts()
        else:
            # Convert lists -> strings
            data_cut_str = self._list_to_string(data_cut)
            data_cuts_str = self._outputHSA["data_cuts"].apply(
                lambda x: self._list_to_string(x)
            )

            # Filter data
            filter = data_cut_str == data_cuts_str
            output_data = self._outputHSA[filter]

        # If invalid then return warning & aid to user
        if output_data.empty:
            warn_msg = (
                "\n\nInvalid Argument: data_cut\n\n\n\n"
                "'data_cut' must appear in the following:"
            )
            warnings.warn(warn_msg)
            output_data = self.get_data_cuts()

        return output_data

    def filter_hsa_data(
        self,
        target_var: str | None = None,
        search_terms="",  # This works, but it kind of sucks
        # ! search_terms: str | list[str] | None = None
        # ! Try to get the above working!
        search_type: str | None = None,
        depth_filter: int | None = None,
        data: pd.DataFrame = None,
    ):
        """
        Search across the hot spot analysis data. Picking a specific
        data_cut (target_var) using search_terms (list of strings)
        to look across the data.

        Note: If you save the output of this function then
        you can pass that initial search into a second search.

        Returns a pd.DataFrame.
        """
        if data is None:
            df = self._outputHSA
        else:
            if not isinstance(data, pd.DataFrame):
                error = ValueError("data is not a pandas dataFrame")
                raise error
            df = data

        if target_var not in [
            "data_cuts",
            "data_content",
            "data_cut_content",
        ]:
            error = ValueError(
                """
                Invalid argument passed to target_var.
                \n
                target_var must be set to one of the following:
                - data_cuts: variable name
                - data_content: variable content
                - data_cut_content: pattern of 'variable_name:data_value'
                \n
                """
            )
            raise error

        if search_type not in ["broad", "strict"]:
            warn_msg = """
            \n\n
            search_type defaults to 'broad' when not specified.
            \n
            Use either 'broad' or 'strict' to remove this message.
            \n\n
            """
            warnings.warn(warn_msg)
            search_type = "broad"

        _search_terms_error = ValueError(
            "'search_terms' must be a string/int or a list of strings/ints."
        )
        if search_terms is None:
            raise _search_terms_error

        if isinstance(search_terms, (str, int)):
            search_terms = [search_terms]

        if not isinstance(search_terms, list):
            raise _search_terms_error

        # Require all search_terms to be str or int.
        search_terms_types = set([type(x) for x in search_terms])
        if not search_terms_types.issubset([str, int]):
            raise _search_terms_error

        # !The actual filtering is below
        search_result = []
        if search_type == "broad":
            # Return any (even partial) matches
            for search_term in search_terms:
                search_result.append(
                    df[[search_term in x for x in df[target_var]]]
                )

        elif search_type == "strict":
            # Return (all) full matches
            search_result.append(
                df[df[target_var].apply(set(search_terms).issuperset)]
            )
        else:
            error = ValueError("This should be impossible...")
            raise error

        # list into dataframe & optionally filter depth
        search_result_df = pd.concat(search_result)

        if depth_filter is not None:
            search_result_df = search_result_df[
                search_result_df["depth"].isin(depth_filter)
            ]

        search_result_df.sort_values("depth", ascending=True, inplace=True)
        return search_result_df
