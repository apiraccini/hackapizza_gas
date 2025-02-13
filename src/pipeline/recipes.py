import json
from pathlib import Path
from typing import Dict, List

from src.config import Config
from src.utils.ingestion import ingest_md_to_json
from src.utils.llm import get_model_source, process_data
from src.utils.misc import normalise_strings, roman_to_int
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
            system_message_template=Config.system_message_template_dish_recipe,
            message_template=Config.message_template_dish_recipe,
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
            system_message_template=Config.system_message_template_restaurant_recipe,
            message_template=Config.message_template_restaurant_recipe,
            output_model_str=get_model_source("src.datamodels", "RestaurantModel"),
        )

        all_restaurants = normalise_strings(all_restaurants)

        for restaurant in all_restaurants:
            for license in restaurant.get("chef_licences", []):
                if license.get("level") is not None:
                    license["level"] = roman_to_int(license["level"])
                # import pdb

                # pdb.set_trace()

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

    with recipes_output_path.open("w") as f:
        json.dump(all_recipes, f, indent=4)

    with restaurant_output_path.open("w") as f:
        json.dump(all_restaurants, f, indent=4)

    return all_recipes, all_restaurants
