"""
Functions to handle list manipulations
"""
import pandas as pd


def remove_none(l: list):
    """
    Remove all instances of None from a list.

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
    Deduplicate a list & preserve the original list's order.

    Args:
        l (list): _description_
        drop_none (bool, optional): _description_. Defaults to False.

    Returns:
        _type_: _description_
    """
    tmp_dict = dict.fromkeys(l)
    unique_list = list(tmp_dict.keys())
    if drop_none:
        unique_list = remove_none(unique_list)

    return unique_list


def find_items(
    list1: list, list2: list, return_matching: bool = True, return_bools: bool = False
):
    """
    Find matching or non-matching items between two lists.

    Parameters:
    - list1: The first list to check.
    - list2: The second list to check.
    - return_matching: A boolean flag. If True, return matching items;
                    if False, return non-matching items.
    - return_bools: A boolean flag. If False (default), do nothing;
                    if True, get bools by checking output against list1.

    Returns:
    - A list containing matching or non-matching items, based on the flag.
    """
    if return_matching:
        output = [item for item in list1 if item in list2]
    else:
        output = [item for item in list1 if item not in list2]

    if return_bools:
        # xform matches into bools by checking if list1 is in output
        output = [item in output for item in list1 if item]

    return output


def lists_to_zipped_dict(
    keys_column: pd.Series | list, values_column: pd.Series | list
):
    """
    Creates a new column in a DataFrame using two columns as keys and values to form dictionaries.

    Parameters:
    - df: The DataFrame.
    - keys_column: Column name for keys in the DataFrame.
    - values_column: Column name for values in the DataFrame.

    Returns:
    - The DataFrame with the new column.
    """
    list_of_zipped_dicts = [
        dict(zip(keys, values)) for keys, values in zip(keys_column, values_column)
    ]
    return list_of_zipped_dicts


def zip_lists_of_dicts(list1, list2):
    """
    Zips two lists of dictionaries and returns a new list of dictionaries.

    Parameters:
    - list1: The first list of dictionaries.
    - list2: The second list of dictionaries.

    Returns:
    - A new list of dictionaries formed by zipping the corresponding dictionaries.
    """
    return [dict(list(d1.items()) + list(d2.items())) for d1, d2 in zip(list1, list2)]


# Example usage:
list_of_dicts1 = [{"a": 1, "b": 2}, {"x": 10, "y": 20}]
list_of_dicts2 = [{"c": 3, "d": 4}, {"z": 30, "w": 40}]

result_list_of_dicts = zip_lists_of_dicts(list_of_dicts1, list_of_dicts2)

print(result_list_of_dicts)
