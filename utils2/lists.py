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
