import re
from difflib import get_close_matches
from typing import Dict, List

import pandas as pd

from .lookup_lists import technique_groups_names


def clean_data(data_list: List[Dict], key: str, mapping_list: List[str]) -> List[Dict]:
    """
    Cleans the data list by updating values with the most similar string from the mapping list.
    Args:
        data_list (list): List of dictionaries containing the data.
        key (str): Key to process.
        mapping_list (list): List of strings to map to.
    Returns:
        list: Cleaned data list.
    """

    def get_most_similar(value: str, mapping_list: List[str]) -> str:
        normalized_value = normalise_string(value)
        normalized_mapping_list = [normalise_string(item) for item in mapping_list]
        matches = get_close_matches(
            normalized_value, normalized_mapping_list, n=1, cutoff=0
        )
        out = matches[0]
        return normalise_string(out)

    def clean_value(value):
        if isinstance(value, str):
            return get_most_similar(value, mapping_list)
        elif isinstance(value, dict):
            return {k: clean_value(v) for k, v in value.items()}
        elif isinstance(value, list):
            return [clean_value(v) for v in value]
        else:
            return value

    cleaned_data_list = []
    for item in data_list:
        new_item = item.copy()
        if key in new_item:
            if key == "chef_licences":
                new_item[key] = [
                    {clean_value(k): roman_to_int(v) for k, v in licence.items()}
                    for licence in new_item[key]
                ]
            else:
                new_item[key] = clean_value(new_item[key])
        cleaned_data_list.append(new_item)

    return cleaned_data_list


def get_output_df(data: List[Dict]) -> pd.DataFrame:
    """Creates a DataFrame from a list of dictionaries."""
    df = pd.DataFrame(
        {
            "row_id": range(1, len(data) + 1),
            "result": [
                str(item["matching_recipes_ids"][0])
                if len(item["matching_recipes_ids"]) == 1
                else ",".join(map(str, item["matching_recipes_ids"]))
                if item["matching_recipes_ids"]
                else "0"
                for item in data
            ],
        }
    )
    return df


def normalise_strings(data: List[Dict]) -> List[Dict]:
    """Normalises strings in a list of dictionaries."""

    def normalise_value(value):
        if isinstance(value, str):
            return normalise_string(value)
        elif isinstance(value, dict):
            return {k: normalise_value(v) for k, v in value.items()}
        elif isinstance(value, list):
            return [normalise_value(v) for v in value]
        else:
            return value

    normalised_data = []
    for item in data:
        normalised_item = {k: normalise_value(v) for k, v in item.items()}
        normalised_data.append(normalised_item)

    return normalised_data


def normalise_keys(data: dict) -> dict:
    return {normalise_string(key): value for key, value in data.items()}


def normalise_string(s: str) -> str:
    s = s.lower()
    s = re.sub(r"\W+", " ", s)
    s = re.sub(r"\s+", "_", s)
    return s


def extract_technique_groups(techniques: List[str] | None) -> List[str]:
    """
    Extracts macro categories from techniques.
    Args:
        techniques (list): List of techniques.
    Returns:
        list: List of technique groups.
    """
    if techniques is None:
        return []

    result = []
    for technique in techniques:
        normalized_techique = normalise_string(technique)
        normalized_technique_groups = [
            normalise_string(technique_group)
            for technique_group in technique_groups_names
        ]
        matches = get_close_matches(
            normalized_techique, normalized_technique_groups, n=1, cutoff=0
        )
        if matches:
            result.append(matches[0])
        else:
            result.append("not matched")

    return result


def roman_to_int(roman: str | int) -> int:
    if isinstance(roman, int):
        return roman

    roman = roman.upper()
    if roman == "0":
        return 0

    roman_numerals = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
    result = 0
    prev_value = 0
    for char in reversed(roman):
        if char == "+":
            result = +1
        value = roman_numerals.get(char, 0)
        if value < prev_value:
            result -= value
        else:
            result += value
        prev_value = value
    return result if result >= 0 else 0
