from typing import Dict, List


def add_restaurant_info_to_recipes(
    recipes: List[Dict], restaurants: List[Dict]
) -> List[Dict]:
    """
    Adds restaurant information to recipes by joining on the recipe_restaurant key from recipes and restaurant_name from restaurants.
    Args:
        recipes (list): List of recipes.
        restaurants (list): List of restaurants.
    Returns:
        list: List of recipes with added restaurant information.
    """
    restaurant_dict = {
        restaurant["restaurant_name"]: restaurant for restaurant in restaurants
    }

    for recipe in recipes:
        restaurant_name = recipe.get("recipe_restaurant")
        if restaurant_name and restaurant_name in restaurant_dict:
            restaurant_info = restaurant_dict[restaurant_name]
            for key, value in restaurant_info.items():
                if key != "restaurant_name":
                    recipe[key] = value

    return recipes
