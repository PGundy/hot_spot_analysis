"""
Functions to handle list manipulations
"""

from typing import Any, List, Union


def remove_none(lst: List[Union[object, None]]) -> List[object]:
    """
    Remove all instances of None from a list.

    Parameters:
    - lst (List[Union[object, None]]): Input list.

    Returns:
    - List[object]: List with all instances of None removed.
    """
    return [x for x in lst if x is not None]


def unique(lst: List[object], drop_none: bool = False) -> List[object]:
    """
    Deduplicate a list while preserving the original order.

    Parameters:
    - lst (List[object]): Input list.
    - drop_none (bool, optional): Whether to drop None values. Defaults to False.

    Returns:
    - List[object]: Deduplicated list.
    """
    unique_dict = dict.fromkeys(lst)
    unique_lst = list(unique_dict.keys())
    if drop_none:
        unique_lst = remove_none(unique_lst)
    return unique_lst


def find_items(
    list1: List[object], list2: List[object], return_matching: bool = True, return_bools: bool = False
) -> List[Union[object, bool]]:
    """
    Find matching or non-matching items between two lists.

    Parameters:
    - list1 (List[object]): The first list to check.
    - list2 (List[object]): The second list to check.
    - return_matching (bool, optional): Whether to return matching items. Defaults to True.
    - return_bools (bool, optional): Whether to return bools indicating presence in list1. Defaults to False.

    Returns:
    - List[Union[object, bool]]: List of matching or non-matching items or bools.
    """
    if return_matching:
        output = [item for item in list1 if item in list2]
    else:
        output = [item for item in list1 if item not in list2]

    if return_bools:
        output = [item in output for item in list1]
    return output  # type: ignore -- pylance :angry:


def lists_to_dict(
    keys_column: Union[List[Any], List[List[Any]]], values_column: Union[List[Any], List[List[Any]]]
) -> List[dict]:
    """
    Create dictionaries from two lists and zip them together.

    Parameters:
    - keys_column (Union[List[Any], List[List[Any]]]): List of keys.
    - values_column (Union[List[Any], List[List[Any]]]): List of values.

    Returns:
    - List[dict]: List of dictionaries formed by zipping keys and values.
    """
    list_of_zipped_dicts = [dict(zip(keys, values)) for keys, values in zip(keys_column, values_column)]  # type: ignore -- pylance :angry:
    return list_of_zipped_dicts


def zip_lists_of_dicts(list1: List[dict], list2: List[dict]) -> List[dict]:
    """
    Zip two lists of dictionaries together.

    Parameters:
    - list1 (List[dict]): The first list of dictionaries.
    - list2 (List[dict]): The second list of dictionaries.

    Returns:
    - List[dict]: List of dictionaries formed by zipping the corresponding dictionaries.
    """
    return [dict(list(d1.items()) + list(d2.items())) for d1, d2 in zip(list1, list2)]


# Demonstrate functionality
if __name__ == "__main__":

    # Example usage:
    list_of_dicts1 = lists_to_dict(keys_column=[["a", "b"], ["x", "y"]], values_column=[[1, 2], [10, 20]])
    print(f"list_of_dicts1: {list_of_dicts1}")

    list_of_dicts2 = lists_to_dict(keys_column=[["c", "d"], ["z", "aa"]], values_column=[[3, 4], [30, 40]])
    print(f"list_of_dicts1: {list_of_dicts2}")

    result_zip_lists_of_dicts = zip_lists_of_dicts(list_of_dicts1, list_of_dicts2)
    print(f"result_list_of_dicts: {result_zip_lists_of_dicts}")
