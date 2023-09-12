import itertools

import numpy as np
import pandas as pd

from utils import list_funcs, validators


# get the list of alphanumerically sorted combinations
def _create_combos(
    data_cuts: str, depth_limit: int = 3  ## rename to interaction_max
):
    """
    Creates the interaction combinations using the data_cuts input
    with an interaction maximum governed by depth_limit.

    Example:
        data_cuts = ['a','b','c']
        depth_limit = 2
        combinations: ['a','b','c', 'ab', 'bc']

    Returns a list(str)
    """

    if None in data_cuts:
        raise ValueError("\n\t\t" + "Invalid item in data_cuts: None")

    data_cuts = list_funcs._make_list_unique(data_cuts)

    data_cuts.sort()

    # define the interim objects
    combination_final = []
    for i in np.arange(1, depth_limit + 1, 1):
        combinations = list(itertools.combinations(data_cuts, int(i)))
        combinations = list(map(list, combinations))
        combinations.sort()

        # Build up nested list of all combinations
        combination_final = [*combination_final, combinations]

        if i == depth_limit:
            # unnest the combinations
            combination_final = list(
                itertools.chain.from_iterable(combination_final)
            )

    return combination_final


def analyze(dataframe: pd.DataFrame, combos: list, analysis_function):
    data = dataframe

    results = []
    total_steps = len(combos) - 1
    for step_i, grp_var_i in enumerate(combos):
        df = validators._add_to_groupby(
            dataframe=data, input_list=grp_var_i
        )
        grp_var_i_plus = df.keys
        grp_var_count = len(grp_var_i_plus)

        print(
            f"Step: {step_i} of {total_steps}"
            + f" -- Grouped By: {grp_var_i_plus}"
        )

        # Run the calculations for each step
        result = analysis_function(df)

        # Create variables to create 'clean' columns
        analysis_function_output_cols = list(result.columns)
        result.reset_index(inplace=True)

        # Add our HSA group variables
        result["depth"] = grp_var_count
        result["data_cuts"] = pd.Series([grp_var_i_plus] * len(result))
        result["data_content"] = result[grp_var_i_plus].apply(
            lambda row: list(row.values.astype(str)), axis=1
        )

        # Create the list zip("data_cuts","data_content")
        ##TODO: Resolve this step to a util function
        tmp_var_group_clean = []
        for row in np.arange(0, len(result), 1):
            # create empty pd.Series -- Then loop builds it
            if row == 0:
                result["data_cut_content"] = pd.Series(dtype=object)

            # NOTE: KNOWN BUG WITH CHAINED INDEXING

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
            + analysis_function_output_cols
        ]

        # Add the result to the results list
        results.append(result)

    # Combine all the results into a dataframe
    results_df = pd.concat(results).reset_index(drop=True)
    return results_df
