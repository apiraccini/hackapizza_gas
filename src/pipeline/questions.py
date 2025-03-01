import json
from pathlib import Path
from typing import Dict, List

import pandas as pd

from src.config import Config
from src.utils.llm import get_model_source, process_data
from src.utils.lookup_lists import (
    ingredient_names,
    license_names,
    planets_names,
    restaurant_names,
    technique_groups_names,
    technique_names,
)
from src.utils.misc import (
    clean_data,
    normalise_strings,
    roman_to_int,
)


def process_questions_pipeline(input_path: Path | str, output_path: Path | str):
    """
    Reads questions from a CSV file, processes them, and returns the processed questions.
    Args:
        input_path (str): Path to the input CSV file.
        output_path (str): Path to the output JSON file.
    Returns:
        dict: A dictionary containing the processed questions.
    """
    input_file = Path(input_path)
    output_file = Path(output_path)

    if output_file.exists():
        with output_file.open("r") as f:
            processed_questions_list = json.load(f)
    else:
        questions_df = pd.read_csv(input_file)
        questions_data = questions_df.to_dict(orient="records")
        processed_questions_list = process_data(
            data=questions_data,
            key="domanda",
            system_message_template=Config.system_message_template_questions,
            message_template=Config.message_template_questions,
            output_model_str=get_model_source("src.datamodels", "RequestModel"),
        )

    out = postprocess_results(processed_questions_list)

    with output_file.open("w") as f:
        json.dump(out, f, indent=4)

    return out


def postprocess_results(question_data: List[Dict]) -> List[Dict]:
    """
    Post-processes the questions results.

    Args:
        question_data (list): List of questions.

    Returns:
        list: A list of post-processed questions.
    """
    out = normalise_strings(question_data)
    out = update_planet_keys(out, Config.distances_path)

    for question in out:
        if question.get("sirius_flag"):
            question["techniques"] = {}

        for key in [
            "ingredients",
            "techniques",
        ]:
            if (
                question.get(key)
                and question[key].get("or")
                and len(question[key].get("or")) == 2
            ):
                question[key]["or_length"] = 1

        if question.get("licence_level"):
            question["licence_level"] = roman_to_int(question["licence_level"])

    keys = [
        "techniques",
        "restaurants",
        "licence_name",
        "planet",
        "sirius_techniques_groups",
        "ingredients",
    ]
    mapping_list = [
        technique_names,
        restaurant_names,
        license_names,
        planets_names,
        technique_groups_names,
        ingredient_names,
    ]
    for key, map in zip(keys, mapping_list):
        out = clean_data(out, key, map)

    out = normalise_strings(out)

    return out


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
        if question.get("planet_distance") and question.get("planet"):
            planet_ok = question.get("planet")
            if planet_ok:
                question["planet"] = distances[
                    distances[f"{planet_ok.lower()}"] < question["planet_distance"]
                ].index.tolist()

    return questions
