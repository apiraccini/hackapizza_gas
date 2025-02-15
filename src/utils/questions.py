from pathlib import Path
from typing import Dict, List

import pandas as pd


def update_planet_keys(questions: List[Dict], distances_path: Path | str) -> List[Dict]:
    """
    Updates the planet keys in the question list based on the distance logic.
    Args:
        questions (list): List of questions.
        distances_path (str): Path to the CSV file containing distances.
    Returns:
        list: List of questions with updated planet keys.
    """
    distances = pd.read_csv(distances_path)
    distances.index = distances["/"]
    distances = distances.drop(columns="/")
    distances.columns = distances.columns.str.lower()
    distances.index = distances.index.str.lower()

    for question in questions:
        if question.get("planet_distance") is not None:
            planet_ok = question.get("planet")[0]
            if planet_ok:
                question["planet"] = distances[
                    distances[f"{planet_ok.lower()}"] < question["planet_distance"]
                ].index.tolist()

    return questions
