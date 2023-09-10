import itertools

import pandas as pd

from utils import list_funcs

"""
Functions meant to check the content, values or attributes of a data object.
"""


def _is_data_grouped(dataframe: pd.DataFrame()):
    ## TODO: rename function to remove leading _
    """
    Check if the data argument is grouped.
    Returns boolean.
    """
    if dataframe.empty:
        raise ValueError("dataframe is empty.")

    return hasattr(dataframe, "groups")


def _get_data_group_by(dataframe: pd.DataFrame()):
    ## TODO: rename function to remove leading _
    """
    If grouped, then return [column_name(s)] ELSE [None].
    Returns list(str).
    """
    if _is_data_grouped(dataframe):
        group_vars = dataframe.keys
        if type(group_vars) == str:
            group_vars = [group_vars]
        return group_vars
    else:
        return [None]


def _add_to_groupby(dataframe: pd.DataFrame(), input_list: list):
    ## TODO: rename function to remove leading _
    """
    Modified version of pd.groupby() where it preserves the groups as
    supplied by the user while cycling through the
    hot spot analysis groups.

    Returns a dataframe with modified groups.
    """
    # list <- list of vars to group by
    if _is_data_grouped(dataframe):
        inputGrps = _get_data_group_by(dataframe)

        if len(inputGrps) > 1:
            inputGrps = list(itertools.chain(*[inputGrps]))

        grpVarList = inputGrps + input_list
        grpVarList = list_funcs._make_list_unique(grpVarList)
    else:
        grpVarList = input_list

    return dataframe.groupby(grpVarList)
