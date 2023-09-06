"""
Functions that improve python's native ability to resolve problematic lists
"""

from itertools import compress


def _remove_none_in_list(input_list: list):
    ## TODO: rename function to remove leading _
    """
    Remove ALL None values from a list.
    Returns a list.
    """
    if None in input_list:
        input_list = [x for x in input_list if x is not None]
    return input_list


def _make_list_unique(input_list: list):
    ## TODO: rename function to remove leading _
    """
    Remove duplicates, but preserves the list's order. This is required as set() re-orders the list when resolving dupes.

    Returns a list.
    """
    unique_list = []
    for item in input_list:
        if item not in unique_list:
            unique_list.append(item)
    return unique_list


def _list_to_string(input_list: list):
    ## TODO: rename to transmute_list_to_str (xmute?)
    """
    Convert list into a string delimited by ' -- '.

    returns str.
    """
    delimiter = " -- "
    return delimiter.join(map(str, input_list))


def _string_to_list(string: str):
    ## TODO: rename to transmute_str_to_list (xmute?)
    """
    Convert string (delimited by ' -- ') into a list.

    returns list.
    """
    delimiter = " -- "
    return string.split(delimiter)


def list1_in_list2(
    list1: list, list2: list, return_non_matches: bool = None
):
    """
    Check if list1 is contained in list2
    """
    bool_list1_in_list2 = [col in list2 for col in list1]

    if return_non_matches is None:
        return bool_list1_in_list2
    elif return_non_matches:
        # flip bools to then return missing values
        list_filter = [not ele for ele in bool_list1_in_list2]
    else:
        list_filter = bool_list1_in_list2

    filtered_list1_elements = list(compress(list1, list_filter))
    return filtered_list1_elements
