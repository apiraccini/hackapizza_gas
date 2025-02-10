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

    def normalise_string(s: str) -> str:
        s = s.lower()
        s = re.sub(r"\W+", " ", s)
        s = s.replace(" ", "_")
        return s

    normalised_data = []
    for item in data:
        normalised_item = {
            k: normalise_string(v) if isinstance(v, str) else v for k, v in item.items()
        }
        normalised_data.append(normalised_item)

    return normalised_data
