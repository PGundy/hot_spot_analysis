import pandas as pd

"""
Functions meant to check the content, values or attributes of a data object.
"""


def is_grouped(dataframe: pd.DataFrame) -> bool:
    # TODO: remove the need for this function, and just take groupby as arg in HSA
    """
    Check if the DataFrame is grouped.

    Parameters:
    - dataframe (pd.DataFrame): Input DataFrame.

    Returns:
    - bool: True if the DataFrame is grouped, False otherwise.
    """
    return hasattr(dataframe, "groups")


def get_groups(dataframe: pd.DataFrame) -> list:
    # TODO: remove the need for this function, and just take groupby as arg in HSA
    """
    If the DataFrame is grouped, return the group variable(s).
    Otherwise, return [None].

    Parameters:
    - dataframe (pd.DataFrame): Input DataFrame.

    Returns:
    - list: List of group variable(s) if the DataFrame is grouped, otherwise [None].
    """
    if is_grouped(dataframe):
        group_vars = list(dataframe.keys)  # type: ignore
        return group_vars
    else:
        return [None]


def return_data(dataframe: pd.DataFrame = pd.DataFrame(None)) -> pd.DataFrame:
    # TODO: remove the need for this function, and just take groupby as arg in HSA
    """Return the original DataFrame from a grouped DataFrame if it's grouped."""
    if is_grouped(dataframe):
        return dataframe.obj  # type: ignore
    else:
        return dataframe


def add_groups_to_combos(group_vars: list, combos: list[list]) -> list[list]:
    """
    Adds group variables to each combination in a list of combinations.

    Parameters:
    - group_vars (list): List of group variables.
    - combos (list[list]): List of combinations.

    Returns:
    - list[list]: List of combinations with group variables added.
    """
    return [group_vars + combo for combo in combos]
