# %%
import warnings
from typing import Union

import numpy as np
import pandas as pd

from utils import combos, list_funcs, reporting, validators

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

        self.data_obj = validators.return_data_obj(data)

        # Set defaults for internal references
        self.combinations = []

    ## TODO: MIGRATE FUNCTIONS TO THE FOLLOWING:
    #! validators
    def _check_inputs(self):
        """
        Below we pressure test the user arguments.
        """
        ### Check 01
        if self.data_obj.empty:
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

        ### Check 04 - data_cuts are subset of data.columns
        if not all(
            list_funcs.list1_in_list2(
                list1=self.data_cuts, list2=self.data_obj.columns
            )
        ):
            invalid_elements = list_funcs.list1_in_list2(
                list1=self.data_cuts,
                list2=self.data_obj.columns,
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

    #! prepare (backend)
    def create_combos(self):
        self.combinations = combos._create_combos(
            self.data_cuts, self.depth_limit
        )

    #! setup
    def setup(self):
        self._check_inputs()
        self.create_combos()

    #! validate
    def validate_metric_function(self, user_metric_function):
        """
        Run the user_metric_function on the data provided. If not
        grouped it creates a constant 'All Rows' to maintain
        a consistent data structure as the hot spot
        analysis output.

        Arguments:
            user_metric_function: an user defined function.

        Returns:
            a pd.DataFrame()
        """
        data = self.data_obj
        data = data.iloc[0:1].copy()

        data["All Rows"] = "All Rows"
        grouping_vars = ["All Rows"]
        data = data.groupby(grouping_vars)

        try:
            user_metric_function(data)
            did_func_run = True
        except:
            did_func_run = False

        return did_func_run

    def run_analysis(self, user_function):
        self.setup()

        if not callable(user_function):
            msg = "Invalid input type: user_function is not a callable function"
            raise TypeError(msg)

        self.data_analyzed = combos.analyze(
            dataframe=self.data,
            combos=self.combinations,
            analysis_function=user_function,
        )

    #! export
    def export_combos(self):
        if self.combinations == []:
            self.create_combos()
        return self.combinations

    def export_analyzed_data(self):
        return self.data_analyzed

    def export_data_cuts(self):
        ## TODO: Move this into reporting!
        ideal_depth = reporting._get_useful_depth(self.data)
        data = self.data_analyzed
        key_vars = ["depth", "data_cuts"]
        row_filter = data["depth"].isin([ideal_depth])

        df_cuts = data[row_filter][key_vars]
        df_cuts["data_cuts"] = pd.Series(
            [list_funcs._list_to_string(x) for x in df_cuts["data_cuts"]]
        )

        df_cuts = df_cuts.explode("data_cuts").value_counts().reset_index()
        df_cuts.columns = key_vars + ["unique_values"]
        df_cuts["data_cuts"] = pd.Series(
            [list_funcs._string_to_list(x) for x in df_cuts["data_cuts"]]
        )

        return df_cuts

    def export_data_content(self, data_cut: Union[str, list] = None):
        data = self.data_analyzed

        ## TODO: Move this into reporting.py!
        ##TODO: build validator.py function that checks the data argument

        if isinstance(data_cut, str):
            data_cut = [data_cut]

        valid_unique_data_cuts = list_funcs._make_list_unique(
            data["data_cuts"]
        )

        if not any([data_cut == x for x in valid_unique_data_cuts]):
            tip = "The data_cut should match one of the following:"
            viable_inputs = [str(x) for x in valid_unique_data_cuts]
            error_msg = "\n\t".join([tip] + viable_inputs)
            raise ValueError(error_msg)

        filter_bool = [data_cut == x for x in data["data_cuts"]]
        key_cols = [
            "data_cuts",
            "data_content",
            "data_cut_content",
        ]

        return data[key_cols][filter_bool]

    def search_hsa(
        self,
        target_var: Union[str, None] = None,
        search_terms="",  # This works, but it kind of sucks...
        # ! search_terms: str | list[str] | None = None
        # ! Try to get the above working! Problem is
        search_type: Union[str, None] = None,
        depth_filter: Union[int, None] = None,
        data: pd.DataFrame = None,
    ):
        # TODO: migrate this function from hot_spot_analysis.py
        # TODO: move this into reporting

        if data is None:
            df = self.data_analyzed
        else:
            if not isinstance(data, pd.DataFrame):
                raise ValueError("data is not a pd.DataFrame")
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


# %%

import numpy as np
import pandas as pd
import seaborn as sb

df = sb.load_dataset("tips")
data_multiplier = 10
dfs = [df for i in np.arange(0, data_multiplier)]
df = pd.concat(dfs)
df.info()

# df_prepared = df
df_prepared = df.groupby("sex", as_index=True)

test = HotSpotAnalysis(
    data=df_prepared, data_cuts=["day", "smoker"], depth_limit=2
)

test.setup()


# %%
def tip_stats(df: pd.DataFrame = None):
    result = df.agg(
        count=pd.NamedAgg("tip", "count"),
        mean=pd.NamedAgg("tip", np.mean),
        total=pd.NamedAgg("tip", np.sum),
    )

    result = result.round(1)
    # result["expected_total"] = result["count"] * result["mean"]
    # result["total_is_larger"] = result["total"] >= result["expected_total"]

    return result


# test.validate_metric_function(tip_stats)

test.run_analysis(tip_stats)
# test.export_data_cuts()
test.export_analyzed_data()

# test.export_data_content(data_cut=["day"])
# test.export_data_content(data_cut=["sex", "day"])


# %%

#! prepare
#! analyze <-- this would run prepare if not already ran
#! search
#! export <-- options that replace all get_X() functions
