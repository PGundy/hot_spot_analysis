"""Below are functions that don't fit into one of the other util themes"""


def pop_keys(dictionary, keys):
    """
    Removes the specified keys from the dictionary and returns a tuple
    with the updated dictionary and a new dictionary containing the popped items.

    Parameters:
    - dictionary: The input dictionary.
    - keys: A list of keys to be popped.

    Returns:
    - A new dictionary with the popped items.
    """
    popped_items = {key: dictionary.pop(key, None) for key in keys}
    return popped_items
