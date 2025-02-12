import re
from typing import Dict, List

import pandas as pd


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
    s = s.replace(" ", "_")
    return s


def extract_technique_groups(techniques: List[str]) -> List[str]:
    """
    Extracts macro categories from techniques.
    Args:
        techniques (list): List of techniques.
    Returns:
        list: List of technique groups.
    """
    technique_groups = {
        "Marinatura": ["marinatura"],
        "Affumicatura": ["affumicatura"],
        "Fermentazione": ["fermentazione"],
        "Decostruzione": ["decostruzione"],
        "Sferificazione": ["sferificazione"],
        "Tecniche di taglio": ["taglio"],
        "Tecniche di impasto": ["impasto"],
        "Surgelamento": ["surgelamento"],
        "Bollitura": ["bollitura"],
        "Grigliatura": ["grigliatura"],
        "Cottura al Forno": ["forno"],
        "Cottura al vapore": ["vapore"],
        "Cottura sottovuoto": ["sottovuoto"],
        "Cottura al Salto": ["salto"],
    }

    result = set()
    for technique in techniques:
        for group, keywords in technique_groups.items():
            if any(keyword in technique.lower() for keyword in keywords):
                result.add(group)
                break
    return list(result)


def roman_to_int(roman: str | int) -> int:
    if isinstance(roman, int):
        return roman

    roman_numerals = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
    roman = roman.upper()
    result = 0
    prev_value = 0
    for char in reversed(roman):
        value = roman_numerals.get(char, 0)
        if value < prev_value:
            result -= value
        else:
            result += value
        prev_value = value
    return result if result > 0 else 0
