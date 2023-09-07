# %%
import warnings
from itertools import compress
from typing import Union

import numpy as np
import pandas as pd

from utils import combos, list_funcs

# %%


class HotSpotAnalysis:
    data: pd.DataFrame
    data_cuts: list
    depth_limit: int

    def __init__(
        self,  # Default values
        data=pd.DataFrame(None),  # HSA.data.empty -> True
        data_cuts=list(),  # []
        depth_limit=int(),  # 0
    ):
        self.data = data
        self.data_cuts = data_cuts
        self.depth_limit = depth_limit

    ## TODO: MIGRATE FUNCTIONS TO THE FOLLOWING:
    #! check_inputs
    def _check_inputs(self):
        """
        Below we pressure test the user arguments.
        """
        ### Check 01
        if self.data.empty:
            raise ValueError("data is invalid: dataframe is empty")

        ### Check 02
        if self.data_cuts == []:
            raise ValueError("data_cuts is Invalid: list is empty")

        ## Check 03
        if self.data_cuts != list_funcs._make_list_unique(self.data_cuts):
            raise ValueError(
                """data_cuts contains unexpected elements. 
                Duplicate elements in data_cuts are not allowed.
                """
            )

        ### Check 04
        if not all(
            list_funcs.list1_in_list2(
                list1=self.data_cuts, list2=self.data.columns
            )
        ):
            invalid_elements = list_funcs.list1_in_list2(
                list1=self.data_cuts,
                list2=self.data.columns,
                return_non_matches=True,
            )

            eror_msg = (
                """data_cuts contains invalid elements. 
                Ensure all elements are columns in the data."""
                + "\n\t"
                + "\n\t".join([i for i in invalid_elements])
            )
            raise ValueError(eror_msg)

        ### Check 05
        if not type(self.depth_limit) is int:
            raise ValueError(
                """depth_limit is invalid.
                depth_limit must be an integer.
                """
            )

        ## Check 06
        if not (1 <= self.depth_limit <= 10):
            raise ValueError(
                """depth_limit is invalid. 
                Integer must be between 1 and 10.
                """
            )

    #! setup
    def create_combos(self):
        self._combinations = combos._create_combos(
            self.data_cuts, self.depth_limit
        )

    def setup(self):
        self.create_combos()

    def export_combos(self):
        if self._combinations == []:
            self.create_combos()
        return self._combinations


# %%

import seaborn as sb

df = sb.load_dataset("tips")

test = HotSpotAnalysis(data=df, data_cuts=["day", "smoker"], depth_limit=9)

test._check_inputs()

# %%

import seaborn as sb

from utils import list_funcs

df = sb.load_dataset("tips")


# %%


#! prepare
#! analyze <-- this would run prepare if not already ran
#! search
#! export <-- options that replace all get_X() functions


class legacy_hsa_placeholder:
    ##TODO: RENAME EVERYTHING TO BE MORE LOGICAL. REMOVE leading '_' where possible

    ## TODO: Update this to check each condition and append result to list
    def _validate_inputs(self):
        """
        Checks all user inputs and print a message to resolve invalid entries.
        Returns boolean.
        """

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

    ## TODO: evaluate the benefits of this & RENAME IT to return_combos
    def get_combos(self):
        """
        Runs self._create_combos() and returns a list of lists where
        each item is a combination that will be used in the hot spot analysis.

        Returns a list.
        """
        if self._combinations == []:
            self._create_combos()  ##TODO: Update to use utils.combos

        print(
            "In total there are",
            len(self._combinations),
            "combinations with a depth_limit max of",
            self.depth_limit,
        )

        return self._combinations

    def test_user_function(self, user_function):
        """
        Run the user_function on the data provided. If not
        grouped it creates a constant 'All Rows' to maintain
        a consistent data structure as the hot spot
        analysis output.

        Arguments:
            user_function: an user defined function.

        Returns:
            a pd.DataFrame()
        """
        if self._is_data_grouped():
            data = self.data.obj
        else:
            data = self.data

        data["All Rows"] = "All Rows"
        grouping_vars = ["All Rows"] + self._get_data_group_by()
        grouping_vars = self._remove_none_in_list(grouping_vars)
        data = data.groupby(grouping_vars)

        print("\n\nBelow is the output of the user_function:")
        return user_function(data)

    # Iterate using user_function & data using groupby(Combos)
    def run_hsa(self, user_function):
        """
        The primary function for user. This runs the entire
        hot spot analysis after creating the combos
        (and validating the inputs). The user will see
        each step print as it begins running to help monitor progress.

        Arguments:
            user_function: an user defined function.

        Returns:
            Nothing. Runs the hot spot analysis, and saves the output.
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
            result = user_function(dataObj)

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
        Returns:
            a pd.DataFrame()
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

        Returns:
            a pd.DataFrame()
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

    def search_data(
        self,
        target_var: Union[str, None] = None,
        search_terms="",  # <-- workaround for python 3.7
        # ! search_terms: str | list[str] | None = None # Ideal solution
        search_type: Union[str, None] = None,
        depth_filter: Union[int, None] = None,
        data: pd.DataFrame = None,
    ):
        """
        Search across the hot spot analysis data. Picking a specific
        data_cut (target_var) using search_terms (list of strings)
        to look across the data.

        Note: If you save the output of this function then
        you can pass that initial search into a second search.

        Returns:
            a pd.DataFrame()
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

    # export the HotSpotAnalysis output dataframe
    ##TODO: rename the following function
    def get_hsa_data(self):
        """
        Export _outputHSA after running hsa.run_hsa()

        Returns:
            a pd.DataFrame()
        """
        return self._outputHSA
