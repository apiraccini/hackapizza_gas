import json

# import pdb
# pdb.set_trace()
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
    contatore = 0
    contatore_condizione1 = 0
    for question in question_data:
        matching_recipes = []

        for recipe in recipe_data:
            contatore += 1
            skip_recipe = False
            # Check 'and' conditions
            for q_key, r_key in [
                ("ingredients", "recipe_ingredients"),
                ("techniques", "recipe_techniques"),
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
                            contatore_condizione1 += 1
                            skip_recipe = True
                            continue

            # Check 'or' conditions
            for q_key, r_key in [
                ("ingredients", "recipe_ingredients"),
                ("techniques", "recipe_techniques"),
                ("restaurants", "recipe_restaurant"),
            ]:
                if question.get(q_key) and question.get(q_key).get("or"):
                    if recipe.get(r_key) is None:
                        continue
                    else:
                        if not any(
                            item in recipe.get(r_key, ["error"])
                            for item in question[q_key].get("or", [])
                        ):
                            skip_recipe = True
                            continue

            # Check 'not' conditions
            for q_key, r_key in [
                ("ingredients", "recipe_ingredients"),
                ("techniques", "recipe_techniques"),
                ("restaurants", "recipe_restaurant"),
            ]:
                if question.get(q_key) and question.get(q_key).get("not"):
                    if recipe.get(r_key) is None:
                        continue
                    else:
                        if not any(
                            item in recipe.get(r_key, ["error"])
                            for item in question[q_key].get("not", [])
                        ):
                            skip_recipe = True
                            continue

            # Additional filters - planets, orders
            for q_key, r_key in [
                ("planets_ok", "planet"),
                ("group_info", "group"),
            ]:
                if question.get(r_key):
                    if not any(item in recipe.get(q_key) for item in question[q_key]):
                        skip_recipe = True
                        continue
            if skip_recipe:
                continue
            matching_recipes.append(recipe.get("recipe_name"))

        # import pdb

        # pdb.set_trace()
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
