import pandas as pd

from utils import validators


def _get_useful_depth(dataframe: pd.DataFrame):
    """
    Get the useful level of depth for the hot spot analysis. Normally
    this is a depth of 1. However if the input data is grouped
    then it is formulaic by (number of grouping columns) + 1.

    Returns int.
    """
    useful_depth_level = validators._get_data_group_by(dataframe)
    if useful_depth_level == [None]:
        useful_depth_level = 1
    else:
        useful_depth_level = len(useful_depth_level) + 1
    return useful_depth_level
