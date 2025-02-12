from typing import Dict, List


def roman_to_int(roman: str | int) -> int:
    if isinstance(roman, int):
        return roman

    roman_numerals = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
    roman = roman.upper()
    result = 0
    prev_value = 0
    for char in reversed(roman):
        value = roman_numerals.get(char, 0)
        if value < prev_value:
            result -= value
        else:
            result += value
        prev_value = value
    return result if result > 0 else 0


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
                if key == "chef_licences":
                    for license in value:
                        license["license_level"] = roman_to_int(
                            license["license_level"]
                        )
                if key != "restaurant_name":
                    recipe[key] = value

    return recipes
