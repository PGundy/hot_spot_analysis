"""
Functions to handle list manipulations
"""


def remove_none(l: list):
    """
    Remove ALL None values from a list.

    Returns:
        list: All instances of None are removed
    """
    if None in l:
        output = [x for x in l if x is not None]
    else:
        output = l
    return output


def unique(l: list, drop_none: bool = False):
    """
    Make the list unique & preserve the original order.
    We utilize the benefits of the dictionary class to do this.

    Returns:
        list
    """
    tmp_dict = dict.fromkeys(l)
    unique_list = list(tmp_dict.keys())
    if drop_none:
        unique_list = remove_none(unique_list)

    return unique_list
