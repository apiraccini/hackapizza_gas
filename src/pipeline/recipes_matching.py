import json
from pathlib import Path
from typing import Dict, List

from src.utils.lookup_lists import (
    restaurant_names,
    technique_groups_names,
    technique_names,
)
from src.utils.misc import clean_data, extract_technique_groups


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
        # Clean data
        question_keys = [
            "techniques",
            "techniques_groups",
            "restaurants",
            "licence_name",
        ]
        recipe_keys = [
            "recipe_techniques",
            "recipe_techniques_groups",
            "recipe_restaurant",
            "chef_licences",
        ]
        mapping_list = [technique_names, technique_groups_names, restaurant_names]
        for q_key, r_key, map in zip(question_keys, recipe_keys, mapping_list):
            questions_data = clean_data(recipes_data, q_key, map)
            recipes_data = clean_data(questions_data, r_key, map)

        # Match recipes
        questions_recipes = match_recipes(recipes_data, questions_data)

        # Map dishes
        questions_recipes_mapped = map_dishes(questions_recipes, mapping)

        # Save to file
        with output_file.open("w") as f:
            json.dump(questions_recipes_mapped, f, indent=4)

    return questions_recipes_mapped


def match_recipes(recipe_data: List[Dict], question_data: List[Dict]) -> List[Dict]:
    """
    Matches recipes with the corresponding ingredients and techniques.
    Returns:
        list: A list of questions with appended matching recipes.
    """
    for recipe in recipe_data:
        recipe["recipe_technique_groups"] = extract_technique_groups(
            recipe.get("recipe_techniques", [])
        )

    for question in question_data:
        matching_recipes = []

        for recipe in recipe_data:
            skip_recipe = False
            # Check 'and' conditions
            for q_key, r_key in [
                ("ingredients", "recipe_ingredients"),
                ("techniques", "recipe_techniques"),
                ("technique_groups", "recipe_technique_groups"),
                ("restaurants", "recipe_restaurant"),
            ]:
                if question.get(q_key) and question.get(q_key).get("and"):
                    if recipe.get(r_key) is None:
                        continue
                    else:
                        if not all(
                            item in recipe.get(r_key, ["error"])
                            for item in question[q_key].get("and", [])
                        ):
                            skip_recipe = True
                            continue

            # Check 'or' conditions
            for q_key, r_key in [
                ("ingredients", "recipe_ingredients"),
                ("techniques", "recipe_techniques"),
                ("technique_groups", "recipe_technique_groups"),
                ("restaurants", "recipe_restaurant"),
            ]:
                if question.get(q_key):
                    or_conditions = question[q_key].get("or", [])
                    or_length = question[q_key].get("or_length", 1)
                    if or_conditions:
                        if recipe.get(r_key) is None:
                            continue
                        else:
                            if (
                                len(
                                    [
                                        item
                                        for item in or_conditions
                                        if item in recipe.get(r_key, ["error"])
                                    ]
                                )
                                < or_length
                            ):
                                skip_recipe = True
                                continue

            # Check 'not' conditions
            for q_key, r_key in [
                ("ingredients", "recipe_ingredients"),
                ("techniques", "recipe_techniques"),
                ("technique_groups", "recipe_technique_groups"),
                ("restaurants", "recipe_restaurant"),
            ]:
                if question.get(q_key) and question.get(q_key).get("not"):
                    if recipe.get(r_key) is None:
                        continue
                    else:
                        if any(
                            item in recipe.get(r_key, ["error"])
                            for item in question[q_key].get("not", [])
                        ):
                            skip_recipe = True
                            continue

            # Additional filters - planets, orders
            for q_key, r_key in [
                ("planet", "restaurant_planet"),
                ("group", "group"),
            ]:
                if question.get(q_key) and recipe.get(r_key):
                    if not any(
                        item in recipe.get(r_key) for item in question.get(q_key)
                    ):
                        skip_recipe = True
                        continue

            # Filter based on licenses
            if question.get("licence_name"):
                required_license_name = question["licence_name"]
                required_license_level = question["licence_level"]
                required_license_condition = question["licence_condition"]
                chef_licenses = recipe.get("chef_licences", [])
                if not any(
                    license_name == required_license_name
                    and (
                        license_level >= required_license_level
                        if required_license_condition == "higher"
                        else license_level == required_license_level
                    )
                    for license in chef_licenses
                    for license_name, license_level in license.items()
                ):
                    skip_recipe = True
                    continue

            if skip_recipe:
                continue
            else:
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
            if recipe_name in mapping:
                matching_recipes_ids.append(mapping[recipe_name])
        question["matching_recipes_ids"] = matching_recipes_ids

    return data
