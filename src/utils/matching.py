import csv
import json
from functools import lru_cache

import pandas as pd

from src.config import Config

from .misc import normalise_string, roman_to_int


def load_illegal_ingredients(filepath):
    illegal_ingredients = {}
    with open(filepath, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            illegal_ingredients[row["ingredient"]] = int(row["volume"])
    return illegal_ingredients


@lru_cache(maxsize=1)
def load_techniques_requirements():
    """
    Loads and normalizes the techniques requirements from JSON file.
    Returns:
        dict: Dictionary mapping technique names to required licenses.
    """
    try:
        with open(Config.techniques_requirements_path, "r") as f:
            requirements = json.load(f)

        # Normalize technique names to match recipe technique names
        normalized_requirements = {}
        for item in requirements:
            technique = normalise_string(item["technique"])
            normalized_requirements[technique] = item["required_licences"]

        return normalized_requirements
    except Exception as e:
        print(f"Error loading techniques requirements: {e}")
        return {}


def check_and_conditions(question, recipe, conditions):
    for q_key, r_key in conditions:
        if question.get(q_key) and question.get(q_key).get("and"):
            if recipe.get(r_key) is None:
                return False
            else:
                if not all(
                    item in recipe.get(r_key, ["error"])
                    for item in question[q_key].get("and", [])
                ):
                    return False
    return True


def check_or_conditions(question, recipe, conditions):
    for q_key, r_key in conditions:
        if question.get(q_key):
            or_length = question[q_key].get("or_length", 1)
            if question[q_key].get("or"):
                if recipe.get(r_key) is None:
                    return False
                else:
                    if or_length is not None:
                        if (
                            len(
                                [
                                    item
                                    for item in question[q_key].get("or")
                                    if item in recipe.get(r_key, ["error"])
                                ]
                            )
                            < or_length
                        ):
                            return False
    return True


def check_not_conditions(question, recipe, conditions):
    for q_key, r_key in conditions:
        if question.get(q_key) and question.get(q_key).get("not"):
            if recipe.get(r_key) is None:
                return False
            else:
                if any(
                    item in recipe.get(r_key, ["error"])
                    for item in question[q_key].get("not", [])
                ):
                    return False
    return True


def check_or_conditions_on_ingredients_techniques(question, recipe):
    if question.get("ingredients") and question.get("ingredients").get("or"):
        if question.get("techniques") and question.get("techniques").get("or"):
            question_ingredients_or = question.get("ingredients").get("or")
            question_techniques_or = question.get("techniques").get("or")

            if len(question_ingredients_or) == 1 and len(question_techniques_or) == 1:
                ingredient = question_ingredients_or[0]
                technique = question_techniques_or[0]
                recipe_ingredients = recipe.get("recipe_ingredients", [])
                recipe_techniques = recipe.get("recipe_techniques", [])

                if recipe_ingredients is None or recipe_techniques is None:
                    return False
                if (
                    ingredient not in recipe_ingredients
                    and technique not in recipe_techniques
                ):
                    return False
    return True


def check_license_requirements(recipe_techniques, chef_licenses):
    """
    Checks if the chef has all required licenses to perform the recipe techniques.
    Args:
        recipe_techniques (list): List of techniques used in the recipe.
        chef_licenses (dict): Dictionary of chef's licenses with their levels.
    Returns:
        bool: True if chef has all required licenses, False otherwise.
    """
    if not recipe_techniques or not chef_licenses:
        return False

    techniques_requirements = load_techniques_requirements()

    for technique in recipe_techniques:
        if technique in techniques_requirements:
            required_licenses = techniques_requirements[technique]
            for license_req in required_licenses:
                license_name = license_req["licence_name"]
                required_level = license_req["licence_level"]

                # Convert required level to int
                required_level_int = (
                    roman_to_int(required_level) if required_level else 0
                )

                # Check if chef has the license
                if license_name not in chef_licenses:
                    return False

                # Check if chef's license level meets the requirement
                chef_level = chef_licenses[license_name]
                chef_level_int = roman_to_int(chef_level) if chef_level else 0

                if chef_level_int < required_level_int:
                    return False

    return True


def check_additional_filters(question, recipe):
    # Filters based on groups, restaurant - single match 1 to 1
    for q_key, r_key in [
        ("group", "recipe_group"),  # TODO: fix groups
        ("restaurants", "recipe_restaurant"),
    ]:
        if question.get(q_key):
            if recipe.get(r_key) is not None:
                if question.get(q_key) != recipe.get(r_key):
                    return False
            else:
                return False

    # Filters based on planet - multiple many to 1
    for q_key, r_key in [
        ("planet", "restaurant_planet"),
    ]:
        if question.get(q_key):
            if recipe.get(r_key):
                if not any(item == recipe.get(r_key) for item in question.get(q_key)):
                    return False
            else:
                return False

    # Filters on technique groups based on Sirius flag - multiple many to many
    if question.get("sirius_flag"):
        for q_key, r_key in [
            ("sirius_techniques_groups", "recipe_technique_groups"),
        ]:
            if question.get(q_key):
                if recipe.get(r_key):
                    if not all(
                        item in recipe.get(r_key, ["error"])
                        for item in question.get(q_key)
                    ):
                        return False
                else:
                    return False

    # Filter based on licenses
    required_license_name = question.get("licence_name")
    required_license_level = question.get("licence_level")
    required_license_condition = question.get("licence_condition")
    chef_licenses = recipe.get("chef_licences", {})

    if not check_license_conditions(
        required_license_name,
        required_license_level,
        required_license_condition,
        chef_licenses,
    ):
        return False

    # Filter based on galactic code
    if question.get("galactic_code") and "quantita legali" in question.get(
        "galactic_code"
    ):
        illegal_ingredients_df = pd.read_csv(Config.illegal_ingredients_path)
        illegal_ingredients = dict(
            zip(
                illegal_ingredients_df["substance"],
                illegal_ingredients_df["volume_limit_perc"],
            )
        )
        recipe_name = recipe.get("recipe_name")
        for restricted in recipe.get("restricted_ingredients", []):
            if restricted.get("recipe") == recipe_name:
                ingredient = restricted.get("ingredient")
                quantity = restricted.get("quantity")
                if ingredient in illegal_ingredients:
                    quantity_int = int("".join(filter(str.isdigit, quantity)))
                    if quantity_int > illegal_ingredients[ingredient]:
                        return False

    if question.get(
        "galactic_code"
    ) and "corrette licenze e certificazioni" in question.get("galactic_code"):
        # Check if the chef has all the required licenses for the recipe's techniques
        recipe_techniques = recipe.get("recipe_techniques", [])
        chef_licenses = recipe.get("chef_licences", {})

        if not check_license_requirements(recipe_techniques, chef_licenses):
            return False

    return True


def check_license_conditions(
    required_license_name,
    required_license_level,
    required_license_condition,
    chef_licenses,
):
    if chef_licenses is None:
        return False

    if (
        required_license_name
        and not required_license_level
        and not required_license_condition
    ):
        if required_license_name not in chef_licenses:
            return False

    if required_license_name and required_license_level and required_license_condition:
        if required_license_name not in chef_licenses:
            return False
        chef_license_level = chef_licenses[required_license_name]
        if required_license_condition == "higher":
            if roman_to_int(chef_license_level) < roman_to_int(required_license_level):
                return False
        elif required_license_condition == "equal":
            if roman_to_int(chef_license_level) != roman_to_int(required_license_level):
                return False

    return True
