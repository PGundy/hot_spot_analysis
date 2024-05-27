import pytest

from hot_spot_analysis.utils import general


def test_pop_keys():
    # Given input dictionary and keys
    dictionary = {"a": 1, "b": 2, "c": 3, "d": 4}
    keys = ["b", "d"]

    # When pop_keys function is called
    popped_items = general.pop_keys(dictionary, keys)

    # Then assert that only popped items are returned
    assert popped_items == {"b": 2, "d": 4}


def test_dict_to_json():
    series_of_dicts = [{"a": 1, "b": 2}, {"x": 10, "y": 20}]
    expected_output = ['{"a": 1, "b": 2}', '{"x": 10, "y": 20}']
    assert general.dict_to_json(series_of_dicts) == expected_output


def test_json_to_dict():
    series_of_json = ['{"a": 1, "b": 2}', '{"x": 10, "y": 20}']
    expected_output = [{"a": 1, "b": 2}, {"x": 10, "y": 20}]
    assert general.json_to_dict(series_of_json) == expected_output


# Execute the tests
if __name__ == "__main__":
    pytest.main()
