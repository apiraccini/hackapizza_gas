import pandas as pd

from src.utils.misc import (
    clean_data,
    get_output_df,
    normalise_keys,
    normalise_strings,
    roman_to_int,
)


def test_clean_data():
    data_list = [{"technique": "Grilling"}, {"technique": "Boiling"}]
    mapping_list = ["grill", "boil"]
    expected = [{"technique": "grill"}, {"technique": "boil"}]
    result = clean_data(data_list, "technique", mapping_list)
    assert result == expected


def test_get_output_df():
    data = [
        {"matching_recipes_ids": [1]},
        {"matching_recipes_ids": [2, 3]},
        {"matching_recipes_ids": []},
    ]
    expected = {"row_id": [1, 2, 3], "result": ["1", "2,3", "0"]}
    result = get_output_df(data)
    pd.testing.assert_frame_equal(result, pd.DataFrame(expected))


def test_normalise_strings():
    data = [{"name": "Pizza Margherita"}, {"name": "Pasta Carbonara"}]
    expected = [{"name": "pizza_margherita"}, {"name": "pasta_carbonara"}]
    result = normalise_strings(data)
    assert result == expected


def test_normalise_keys():
    data = {"Pizza Margherita": "Delicious", "Pasta Carbonara": "Tasty"}
    expected = {"pizza_margherita": "Delicious", "pasta_carbonara": "Tasty"}
    result = normalise_keys(data)
    assert result == expected


def test_roman_to_int():
    assert roman_to_int("X") == 10
    assert roman_to_int("IV") == 4
    assert roman_to_int("MMXXI") == 2021
    assert roman_to_int(0) == 0
    assert roman_to_int("0") == 0
    assert roman_to_int("VI+") == 7
