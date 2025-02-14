from pathlib import Path
from typing import Dict, List

import pandas as pd


def update_planet_keys(questions: List[Dict], distances_file: Path | str) -> List[Dict]:
    """
    Updates the planet keys in the question list based on the distance logic.
    Args:
        questions (list): List of questions.
        distances_file (str): Path to the CSV file containing distances.
    Returns:
        list: List of questions with updated planet keys.
    """
    distances = pd.read_csv(distances_file)
    distances.index = distances["/"]
    distances = distances.drop(columns="/")

    for question in questions:
        if question.get("planet_distance") is not None:
            planet_ok = question.get("planet_ok")[0]
            if planet_ok:
                question["planet_ok"] = distances[
                    distances[f"{planet_ok}"] < question["planet_distance"]
                ].index.tolist()

    return questions
