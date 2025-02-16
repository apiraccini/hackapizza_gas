import csv

import pandas as pd

from src.config import Config

from .misc import roman_to_int


def load_illegal_ingredients(filepath):
    illegal_ingredients = {}
    with open(filepath, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            illegal_ingredients[row["ingredient"]] = int(row["volume"])
    return illegal_ingredients


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


def check_additional_filters(question, recipe):
    # Filters based on groups, restaurant - single match 1 to 1
    for q_key, r_key in [
        ("group", "recipe_group"),  # TODO: fix groups
        ("restaurants", "recipe_restaurant"),
    ]:
        if question.get(q_key) and recipe.get(r_key):
            if question.get(q_key) != recipe.get(r_key):
                return False

    # Filters based on planet - multiple many to 1
    for q_key, r_key in [
        ("planet", "restaurant_planet"),
    ]:
        if question.get(q_key) and recipe.get(r_key):
            if not any(item == recipe.get(r_key) for item in question.get(q_key)):
                return False

    # Filters on technique groups based on Sirius flag - multiple many to many
    if question.get("sirius_flag"):
        for q_key, r_key in [
            ("sirius_techniques_groups", "recipe_technique_groups"),
        ]:
            if question.get(q_key) and recipe.get(r_key):
                if not all(
                    item in recipe.get(r_key, ["error"]) for item in question.get(q_key)
                ):
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
    if "quantita legali" in question.get("galactic_code", []):
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
                if (
                    ingredient in illegal_ingredients
                    and quantity > illegal_ingredients[ingredient]
                ):
                    return False

    return True


def check_license_conditions(
    required_license_name,
    required_license_level,
    required_license_condition,
    chef_licenses,
):
    if (
        required_license_name
        and not required_license_level
        and not required_license_condition
    ):
        if required_license_name not in chef_licenses:
            return False

    if (
        required_license_level
        and required_license_condition
        and not required_license_name
    ):
        if required_license_condition == "higher":
            if not all(
                roman_to_int(license_level) >= roman_to_int(required_license_level)
                for license_level in chef_licenses.values()
            ):
                return False
        elif required_license_condition == "equal":
            if not any(
                roman_to_int(license_level) == roman_to_int(required_license_level)
                for license_level in chef_licenses.values()
            ):
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
