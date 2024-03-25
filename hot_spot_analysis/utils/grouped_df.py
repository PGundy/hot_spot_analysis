import pandas as pd

"""
Functions meant to check the content, values or attributes of a data object.
"""


def is_grouped(dataframe: pd.DataFrame):
    """
    Check if the data argument is grouped.
    Returns boolean.
    """
    return hasattr(dataframe, "groups")


def get_groups(dataframe: pd.DataFrame):
    """
    If grouped, then return [column_name(s)] ELSE [None].
    Returns list(str).
    """
    if is_grouped(dataframe):
        group_vars = dataframe.keys
        if isinstance(group_vars, str):
            group_vars = [group_vars]
        return group_vars
    else:
        return [None]


def return_data(dataframe: pd.DataFrame = pd.DataFrame(None)):
    """return dataframe from grouped or standard DataFrame"""
    if is_grouped(dataframe):
        return dataframe.obj
    else:
        return dataframe


def add_groups_to_combos(group_vars: list[str], combos: list[list[str]]):
    """adds a fixed list to a list of lists"""
    combos_plus = []
    for combo in combos:
        combo_plus = group_vars + combo
        combos_plus.append(combo_plus)
    return combos_plus
