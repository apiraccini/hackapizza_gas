from pathlib import Path


class Config:
    """Configuration class for the project."""

    debug = True

    provider = "groq"
    model = "deepseek-r1-distill-qwen-32b"  # "deepseek-r1-distill-llama-70b",  "llama-3.3-70b-versatile"

    # data paths
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
    distances_path = "data/raw/Misc/Distanze.csv"

    # prompt templates
    # questions
    system_message_template_questions = """
    You are a helpful assistant that parses the request of the user.
    In this case, the users will be clients of a restaurant that want to know which dishes satisfy their requirements.
    You must extract the information using the pydantic model below and return a JSON format.\n\n{output_model_str}
    
    Here are some few shot examples for tricky cases:
    
    - conditions on techniques and ingredients
    <user> : "Quali piatti utilizzano la Polvere di Crononite e la tecnica di Incisione Elettromagnetica Plasmica, ma non impiegano la Decostruzione Atomica a Strati Energetici nella loro preparazione?",
    <assistant> : {{
        "ingredients": {{
            "and": ["Polvere di Crononite"],
            "or": null,
            "or_length": null,
            "not": null
        }},
        "techniques": {{
            "and": ["Incisione Elettromagnetica Plasmica"],
            "or": null,
            "or_length": null,
            "not": ["Decostruzione Atomica a Strati Energetici"]
        }},
        "restaurants": null,
        "group": null,
        "licence_name": null,
        "licence_level": null,
        "licence_condition": "equal",
        "planet": [],
        "planet_distance": null,
        "galactic_code": [],
        "technique_groups": {{
            "and": [],
            "or": [],
            "not": []
        }}
    }}

    - "at least" condition on ingredients or techniques
    <user> : "Quali piatti contengono almeno 2 ingredienti tra Polvere di Crononite, Nduja Fritta Tanto, Spezie di Melange e Polvere di Stelle?",
    <assistant> : {{
        "ingredients": {{
            "and": null,
            "or": ["Polvere di Crononite", "Nduja Fritta Tanto", "Spezie di Melange","Polvere di Stelle"],
            "or_length": 2,
            "not": null
        }},
        "techniques": null,
        "restaurants": null,
        "group": null,
        "licence_name": null,
        "licence_level": null,
        "licence_condition": "equal",
        "planet": [],
        "planet_distance": null,
        "galactic_code": [],
        "technique_groups": {{
            "and": [],
            "or": [],
            "not": []
        }}
    }}

    - planets and licences
    <user> : "Quali piatti, preparati in un ristorante su Asgard, richiedono la licenza LTK non base e utilizzano Carne di Xenodonte?",
    <assistant> : {{
        "ingredients": null,
        "techniques": null,
        "restaurants": null,
        "group": null,
        "licence_name": certificazione di grado tecnologico LTK ,
        "licence_level": 1,
        "licence_condition": "greater",
        "planet": ["Asgard"],
        "planet_distance": null,
        "galactic_code": [],
        "technique_groups": {{
            "and": [],
            "or": [],
            "not": []
        }}
    }}
    """
    message_template_questions = """
    This is the client request: {request}.
    Don't translate, you must keep the original text language.
    Return only the JSON instance representing the request, with every field (empty ones as well).
    """

    # recipes
    system_message_template_recipes = """
    You are a helpful assistant that receive a text containing information about a recipe as input.
    You must extract the information using the pydantic model below and return a JSON format.\n\n{output_model_str}
    Some tricky  or techniques are :
        - Latte+
        - Nduja Fritta Tanto
        - Cioccorane
        - Grigliatura a Energia Stellare DiV
        - Grigliatura Elettro Molecolare A Spaziatura Variabile
    """
    message_template_recipes = """
    This is the text containing information about the recipe: {request}.
    Don't translate, you must keep the original text language.
    Return only the JSON instance representing information about the recipe.
    """

    # restaurant
    system_message_template_restaurant = """
    You are a helpful assistant that receive a text containing information about a restaurant as input.
    You must extract the information using the pydantic model below and return a JSON format.\n\n{output_model_str}
    """
    message_template_restaurant = """
    This is the text containing information about the restaurant: {request}.
    Don't translate, you must keep the original text language.
    Return only the JSON instance representing information about the restaurant.
    """
