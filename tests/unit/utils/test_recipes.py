from src.utils.recipes import add_restaurant_info_to_recipes


def test_add_restaurant_info_to_recipes():
    recipes = [
        {"recipe_name": "Pizza Margherita", "recipe_restaurant": "Pizza Place"},
        {"recipe_name": "Pasta Carbonara", "recipe_restaurant": "Pasta House"},
    ]
    restaurants = [
        {"restaurant_name": "Pizza Place", "location": "Rome", "rating": 5},
        {"restaurant_name": "Pasta House", "location": "Milan", "rating": 4},
    ]
    expected = [
        {
            "recipe_name": "Pizza Margherita",
            "recipe_restaurant": "Pizza Place",
            "location": "Rome",
            "rating": 5,
        },
        {
            "recipe_name": "Pasta Carbonara",
            "recipe_restaurant": "Pasta House",
            "location": "Milan",
            "rating": 4,
        },
    ]
    result = add_restaurant_info_to_recipes(recipes, restaurants)
    assert result == expected
