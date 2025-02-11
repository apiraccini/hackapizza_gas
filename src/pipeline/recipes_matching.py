import json
from pathlib import Path
from typing import Dict, List


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

    for question in question_data:
        parsed_question = question.get("parsed_question", {})
        matching_recipes = []
        # matching_recipes_metadata = []

        for recipe in recipe_data:
            # Check 'and' conditions
            for key in [
                "recipe_ingredients",
                "recipe_techniques",
                "recipe_techniques_groups",
                "recipe_restaurants",
            ]:
                if parsed_question.get(key) and parsed_question.get(key).get("and"):
                    if not all(
                        item in recipe.get(key)
                        for item in parsed_question[key].get("and", [])
                    ):
                        continue

            # Check 'or' conditions
            for key in [
                "recipe_ingredients",
                "recipe_techniques",
                "recipe_techniques_groups",
                "recipe_restaurants",
            ]:
                if parsed_question.get(key) and parsed_question.get(key).get("or"):
                    if not any(
                        item in recipe.get(key)
                        for item in parsed_question[key].get("or", [])
                    ):
                        continue

            # Check 'not' conditions
            for key in [
                "recipe_ingredients",
                "recipe_techniques",
                "recipe_techniques_groups",
                "recipe_restaurants",
            ]:
                if parsed_question.get(key) and parsed_question.get(key).get("not"):
                    if any(
                        item in recipe.get(key)
                        for item in parsed_question[key].get("not", [])
                    ):
                        continue

            # Additional filters - planets
            for key1, key2 in [("planet_info", "planets_ok")]:
                if parsed_question.get(key2):
                    if not any(
                        item in recipe.get(key1) for item in parsed_question[key]
                    ):
                        continue

            # Additional filters - orders
            for key1, key2 in [("order_info", "order_ok")]:
                if parsed_question.get(key2):
                    if not any(
                        item in recipe.get(key1) for item in parsed_question[key]
                    ):
                        continue

            matching_recipes.append(recipe.get("recipe_name"))
            # matching_recipes_metadata.append(recipe)

        question["matching_recipes"] = matching_recipes
        # question["matching_recipes_metadata"] = matching_recipes_metadata

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
