import json
from pathlib import Path
from typing import Dict, List

from src.utils.matching import (
    check_additional_filters,
    check_and_conditions,
    check_not_conditions,
    check_or_conditions,
    check_or_conditions_on_ingredients_techniques,
)


def match_recipes_pipeline(
    output_path: Path | str,
    recipes_data: List[Dict],
    questions_data: List[Dict],
    mapping: Dict,
):
    """
    Matches recipes with questions and maps dishes, then saves the result to a JSON file.
    Args:
        output_path (Path|str): Path to the output JSON file.
        recipes_data (list): List of recipes.
        questions_data (list): List of questions.
        mapping (dict): Dictionary containing the dish mappings.
    Returns:
        list: List of questions with matching recipes and mapped dishes.
    """
    output_file = Path(output_path)

    if output_file.exists():
        with output_file.open("r") as f:
            questions_recipes_mapped = json.load(f)
    else:
        questions_recipes = match_recipes(recipes_data, questions_data)
        questions_recipes_mapped = map_dishes(questions_recipes, mapping)

        with output_file.open("w") as f:
            json.dump(questions_recipes_mapped, f, indent=4)

    return questions_recipes_mapped


def match_recipes(recipe_data: List[Dict], question_data: List[Dict]) -> List[Dict]:
    """
    Matches recipes with the corresponding ingredients and techniques.
    Returns:
        list: A list of questions with appended matching recipes.
    """
    keys = [
        ("ingredients", "recipe_ingredients"),
        ("techniques", "recipe_techniques"),
    ]

    for question in question_data:
        matching_recipes = []

        for recipe in recipe_data:
            if not check_and_conditions(question, recipe, keys):
                continue  # skip recipe
            if not check_or_conditions(question, recipe, keys):
                continue
            if not check_not_conditions(question, recipe, keys):
                continue
            if not check_additional_filters(question, recipe):
                continue
            if not check_or_conditions_on_ingredients_techniques(question, recipe):
                continue

            matching_recipes.append(recipe.get("recipe_name"))

        question["matching_recipes"] = matching_recipes

    return question_data


def map_dishes(data: List[Dict], mapping: Dict) -> List[Dict]:
    """
    Maps dishes to their identifiers and adds the mapping to each question.
    Args:
        data (list): List of questions with matching recipes.
        mapping (dict): Dictionary containing the dish mappings.
    Returns:
        list: List of questions with added dish mappings.
    """

    for question in data:
        matching_recipes_ids = []
        for recipe_name in question.get("matching_recipes", []):
            if recipe_name.endswith("_"):
                recipe_name = recipe_name.rstrip("_")
            if recipe_name in mapping:
                matching_recipes_ids.append(mapping[recipe_name])
        question["matching_recipes_ids"] = matching_recipes_ids

    return data
