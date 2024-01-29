"""Below are functions that don't fit into one of the other util themes"""
import json


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


def dict_to_json(series_of_dicts):
    return [json.dumps(d) for d in series_of_dicts]


def json_to_dict(series_of_json):
    return [json.loads(s) for s in series_of_json]


# %%


def print_each_item(vector):
    for i in vector:
        print(i)


# %%

test = [
    {
        "b": 2,
        "c": 3,
    },
    {"z": 26},
    {"a": 1},
]
print("\n\nBelow we run: print_each_item(test)")
print_each_item(test)

print("\n\nBelow we run: dict_to_json(test)")
print_each_item(dict_to_json(test))


print("\n\nBelow we run: json_to_dict(dict_to_json(test))")
print_each_item(json_to_dict(dict_to_json(test)))


# %%
