import json


def pop_keys(dictionary: dict, keys: list) -> dict:
    """
    Removes the specified keys from the dictionary and returns a dictionary
    containing the popped items.

    Parameters:
    - dictionary (dict): The input dictionary.
    - keys (list): A list of keys to be popped.

    Returns:
    - dict: A dictionary containing the popped items.
    """
    popped_items = {key: dictionary.pop(key, None) for key in keys}
    return popped_items


def dict_to_json(series_of_dicts: list) -> list:
    """
    Convert a list of dictionaries to a list of JSON strings.

    Parameters:
    - series_of_dicts (list): A list of dictionaries.

    Returns:
    - list: A list of JSON strings.
    """
    return [json.dumps(d) for d in series_of_dicts]


def json_to_dict(series_of_json: list) -> list:
    """
    Convert a list of JSON strings to a list of dictionaries.

    Parameters:
    - series_of_json (list): A list of JSON strings.

    Returns:
    - list: A list of dictionaries.
    """
    return [json.loads(s) for s in series_of_json]
