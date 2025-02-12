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


def normalise_keys(data: dict) -> dict:
    def normalise_string(s: str) -> str:
        s = s.lower()  # Converte in minuscolo
        s = re.sub(r"\W+", " ", s)  # Sostituisce caratteri non alfanumerici con spazio
        s = s.strip()  # Rimuove eventuali spazi iniziali e finali
        s = s.replace(" ", "_")  # Sostituisce gli spazi con underscore
        return s

    # Crea un nuovo dizionario normalizzando le chiavi, mantenendo inalterati i valori
    return {normalise_string(key): value for key, value in data.items()}


def normalise_strings(data: List[Dict]) -> List[Dict]:
    """Normalises strings in a list of dictionaries."""

    def normalise_string(s: str) -> str:
        s = s.lower()
        s = re.sub(r"\W+", " ", s)
        s = s.replace(" ", "_")
        return s

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


def normalise_string(s: str) -> str:
    s = s.lower()
    s = re.sub(r"\W+", " ", s)
    s = s.replace(" ", "_")
    return s
