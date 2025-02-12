from pathlib import Path


class Config:
    """Configuration class for the project."""

    debug = False

    provider = "groq"
    model = "deepseek-r1-distill-llama-70b"  # "deepseek-r1-distill-qwen-32b", "llama-3.3-70b-versatile"

    system_message_template_questions = """
    You are a helpful assistant that parses the request of the user.
    In this case, the users will be clients of a restaurant that want to know which dishes satisfy their requirements.
    You must extract the information using the pydantic model below and return a JSON format.\n\n{output_model_str}
    Some tricky  or techniques are :
        - Latte+
        - Nduja Fritta Tanto
        - Cioccorane
        - Grigliatura a Energia Stellare DiV
        - Grigliatura Elettro Molecolare A Spaziatura Variabile
    """
    message_template_questions = """
    This is the client request: {request}.
    Don't translate, you must keep the original text language.
    Return only the JSON instance representing the request, with every field (empty ones as well).
    """

    system_message_template_dish_recipe = """
    You are a helpful assistant that receive a text containing information about a recipe as input.
    You must extract the information using the pydantic model below and return a JSON format.\n\n{output_model_str}
    Some tricky  or techniques are :
        - Latte+
        - Nduja Fritta Tanto
        - Cioccorane
        - Grigliatura a Energia Stellare DiV
        - Grigliatura Elettro Molecolare A Spaziatura Variabile
    """
    message_template_dish_recipe = """
    This is the text containing information about the recipe: {request}.
    Don't translate, you must keep the original text language.
    Return only the JSON instance representing information about the recipe.
    """

    system_message_template_restaurant_recipe = """
    You are a helpful assistant that receive a text containing information about a restaurant as input.
    You must extract the information using the pydantic model below and return a JSON format.\n\n{output_model_str}
    """
    message_template_restaurant_recipe = """
    This is the text containing information about the restaurant: {request}.
    Don't translate, you must keep the original text language.
    Return only the JSON instance representing information about the restaurant.
    """

    distances_file = "data/raw/Misc/Distanze.csv"

    data_path = Path("data/debug") if debug else Path("data/processed")
    data_path_dict = {
        "input_questions_path": data_path / "domande.csv"
        if debug
        else Path("data/raw/domande.csv"),
        "input_recipes_path": data_path / "menu_md",
        "recipes_mapping_path": "data/raw/Misc/dish_mapping.json",
        "output_questions_path": data_path / "questions.json",
        "output_recipes_path": data_path / "recipes.json",
        "output_restaurants_path": data_path / "restaurants.json",
        "output_result_json": data_path / "result.json",
        "output_result_path": data_path / "result.csv",
    }
