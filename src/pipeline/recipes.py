import json
from pathlib import Path
from typing import Dict, List

from src.config import Config
from src.utils.ingestion import ingest_md_to_json
from src.utils.llm import get_model_source, process_data
from src.utils.lookup_lists import (
    license_names,
    planets_names,
    restaurant_names,
    technique_groups_names,
    technique_names,
)
from src.utils.misc import clean_data, normalise_strings, roman_to_int
from src.utils.recipes import add_restaurant_info_to_recipes


def load_and_process_recipes(
    input_path: Path | str,
    recipes_output_path: Path | str,
    restaurant_output_path: Path | str,
) -> List[Dict]:
    """
    Loads and processes the recipe data from markdown files.
    Args:
        input_path (str): Path to the input directory containing markdown files.
        recipes_output_path (str): Path to the output JSON file.
        restaurant_output_path (str): Path to the output JSON file for restaurants.
    Returns:
        list: A list of dictionaries containing the processed recipe data.
    """
    recipes_output_path = Path(recipes_output_path)

    if recipes_output_path.exists():
        with recipes_output_path.open("r") as f:
            all_recipes = json.load(f)
    else:
        ingestion_dict = ingest_md_to_json(input_path)
        all_recipes = ingestion_dict["recipes"]

        print("Processing menus")
        all_recipes = process_data(
            data=all_recipes,
            key="recipe_text",
            system_message_template=Config.system_message_template_recipes,
            message_template=Config.message_template_recipes,
            output_model_str=get_model_source("src.datamodels", "RecipeModel"),
        )

        all_recipes = normalise_strings(all_recipes)

        with recipes_output_path.open("w") as f:
            json.dump(all_recipes, f, indent=4)

    return all_recipes


def load_and_process_restaurants(
    input_path: Path | str, restaurant_output_path: Path | str
) -> List[Dict]:
    """
    Loads and processes the restaurant data from markdown files.
    Args:
        input_path (str): Path to the input directory containing markdown files.
        restaurant_output_path (str): Path to the output JSON file.
    Returns:
        list: A list of dictionaries containing the processed restaurant data.
    """
    restaurant_output_path = Path(restaurant_output_path)

    if restaurant_output_path.exists():
        with restaurant_output_path.open("r") as f:
            all_restaurants = json.load(f)
    else:
        ingestion_dict = ingest_md_to_json(input_path)
        all_restaurants = ingestion_dict["restaurants"]

        print("Processing restaurants info")
        all_restaurants = process_data(
            data=all_restaurants,
            key="restaurant_text",
            system_message_template=Config.system_message_template_restaurant,
            message_template=Config.message_template_restaurant,
            output_model_str=get_model_source("src.datamodels", "RestaurantModel"),
        )

        all_restaurants = normalise_strings(all_restaurants)

        for restaurant in all_restaurants:
            if restaurant.get("chef_licences"):
                for license in restaurant.get("chef_licences", []):
                    if license.get("level") is not None:
                        license["level"] = roman_to_int(license["level"])

        with restaurant_output_path.open("w") as f:
            json.dump(all_restaurants, f, indent=4)

    return all_restaurants


def process_recipes_pipeline(
    input_path: Path | str,
    recipes_output_path: Path | str,
    restaurant_output_path: Path | str,
) -> List[Dict]:
    """
    Processes the recipe data from markdown files, adds ingredients and techniques, and saves the result to a JSON file.
    Args:
        input_path (str): Path to the input directory containing markdown files.
        recipes_output_path (str): Path to the output JSON file.
        restaurant_output_path (str): Path to the output JSON file for restaurants.
    Returns:
        list: A list of dictionaries containing the processed recipe data.
    """
    all_recipes = load_and_process_recipes(
        input_path, recipes_output_path, restaurant_output_path
    )
    all_restaurants = load_and_process_restaurants(input_path, restaurant_output_path)

    all_recipes = add_restaurant_info_to_recipes(all_recipes, all_restaurants)

    keys = [
        "recipe_techniques",
        "recipe_techniques_groups",
        "recipe_restaurant",
        "chef_licences",
        "restaurant_planet",
    ]
    mapping_list = [
        technique_names,
        technique_groups_names,
        restaurant_names,
        license_names,
        planets_names,
    ]
    for key, map in zip(keys, mapping_list):
        all_recipes = clean_data(all_recipes, key, map)

    with recipes_output_path.open("w") as f:
        json.dump(all_recipes, f, indent=4)

    with restaurant_output_path.open("w") as f:
        json.dump(all_restaurants, f, indent=4)

    return all_recipes, all_restaurants
