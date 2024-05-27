import pandas as pd
import pytest

from hot_spot_analysis.utils import lists


# Test remove_none function
def test_remove_none():
    assert lists.remove_none([1, None, 3, None, 5]) == [1, 3, 5]
    assert lists.remove_none([]) == []


# Test unique function
def test_unique():
    assert lists.unique([1, 2, 3, 2, 1]) == [1, 2, 3]
    assert lists.unique([1, None, 3, None, 5], drop_none=True) == [1, 3, 5]


# Test find_items function
def test_find_items():
    assert lists.find_items([1, 2, 3, 4], [3, 4, 5, 6], return_matching=True) == [3, 4]
    assert lists.find_items([1, 2, 3, 4], [3, 4, 5, 6], return_matching=False) == [1, 2]
    assert lists.find_items([1, 2, 3, 4], [3, 4, 5, 6], return_bools=True) == [False, False, True, True]


# Test lists_to_dict function
def test_lists_to_dict():
    keys_column = [["a", "b"], ["c", "d"]]
    values_column = [[1, 2], [3, 4]]
    expected_output = [{"a": 1, "b": 2}, {"c": 3, "d": 4}]
    assert lists.lists_to_dict(keys_column, values_column) == expected_output


# Test zip_lists_of_dicts function
def test_zip_lists_of_dicts():
    list1 = [{"a": 1, "b": 2}, {"c": 3, "d": 4}]
    list2 = [{"e": 5, "f": 6}, {"g": 7, "h": 8}]
    expected_output = [{"a": 1, "b": 2, "e": 5, "f": 6}, {"c": 3, "d": 4, "g": 7, "h": 8}]
    assert lists.zip_lists_of_dicts(list1, list2) == expected_output


# Execute the tests
if __name__ == "__main__":
    pytest.main()
