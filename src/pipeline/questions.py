import json
from pathlib import Path
from typing import Dict, List

import pandas as pd

from src.config import Config
from src.utils.llm import get_model_source, process_data
from src.utils.lookup_lists import (
    license_names,
    planets_names,
    restaurant_names,
    technique_groups_names,
    technique_names,
)
from src.utils.misc import (
    clean_data,
    extract_technique_groups,
    normalise_strings,
    roman_to_int,
)
from src.utils.questions import update_planet_keys


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
            out = json.load(f)
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

    out = update_planet_keys(question_data, Config.distances_path)
    out = normalise_strings(out)

    for question in out:
        technique_groups = {"and": [], "or": [], "not": []}
        for key in ["and", "or", "not"]:
            techniques = question.get("techniques", {})
            if techniques:
                technique_groups[key] = extract_technique_groups(
                    techniques.get(key, [])
                )
        question["technique_groups"] = technique_groups

        if question.get("licences"):
            required_license = question["licence"]
            required_license["level"] = roman_to_int(required_license["level"])

    keys = ["techniques", "techniques_groups", "restaurants", "licence_name", "planet"]
    mapping_list = [
        technique_names,
        technique_groups_names,
        restaurant_names,
        license_names,
        planets_names,
    ]
    for key, map in zip(keys, mapping_list):
        out = clean_data(out, key, map)

    return out
