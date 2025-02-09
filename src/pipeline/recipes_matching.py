import json
from pathlib import Path
from typing import Dict, List

# example_data = [
#     {
#         "recipe_name": "Nebulosa Celestiale alla Stellaris",
#         "recipe_raw_text": """
#         Lasciatevi trasportare in un viaggio attraverso le profondità cosmiche con la nostra “Nebulosa Celestiale alla Stellaris”, una sinfonia culinaria che
#         fonde la magia delle stelle con l'arte della cucina quantistica. Al centro del piatto brilla un arrosto di Carne di Balena Spaziale, sapientemente cotto
#         utilizzando microonde entropiche sincronizzate per ottenere una superficie croccante e dorata che racchiude un cuore succulento.
#         Accanto, la carne di Mucca, teneramente preparata con la cottura a vapore termocinetica multipla, si fonde armoniosamente con funghi dell'Etere
#         fluttuanti, esaltando un delicato profumo che solletica i sensi. Un contorno di Riso di Cassandra cuoce con vapore a flusso di particelle
#         isoarmoniche, ogni singolo chicco brilla come una stella danzante, conservando i suoi nutrienti e colori translucidi.
#         Il sapore imprevedibile delle Shard di Materia Oscura è catturato in un'infusione sublime, avvolgendo tutto in un'atmosfera di meraviglia
#         gravitazionale. Sorprendetevi con delle finissime teste di Idra, immerse in un consommé rigenerativo, la cui preparazione segue tecniche di taglio
#         a risonanza sonica rigenerativa per assicurarne la sicurezza e il sapore impeccabile.
#         A completare questa opera d'arte, il nostro Pane di Luce irradia energia dorata, pronto a raccogliere ogni sapore con la sua morbidezza. E, come
#         culmine di questo viaggio stellare, una degustazione di Biscotti della Galassia ruota allegramente intorno al piatto; scaglie di stelle e zucchero
#         cosmico, accanto a un velato sentore di spezie Melange, che prolungano l'esperienza con un dolce indugio presciente che eleva l'anima oltre le
#         stelle.
#         Ingredienti
#         Shard di Materia Oscura
#         Carne di Balena spaziale
#         Carne di Mucca
#         Teste di Idra
#         Riso di Cassandra
#         Biscotti della Galassia
#         Pane di LuceFunghi dell'Etere
#         Spezie Melange
#         Tecniche
#         Cottura a Vapore con Flusso di Particelle Isoarmoniche
#         Cottura a Vapore Termocinetica Multipla
#         Taglio a Risonanza Sonica Rigenerativa
#         Cottura con Microonde Entropiche Sincronizzate""",
#         "recipe_ingredients": [
#             "Shard di Materia Oscura",
#             "Carne di Balena spaziale",
#             "Carne di Mucca",
#             "Teste di Idra",
#             "Riso di Cassandra",
#             "Biscotti della Galassia",
#             "Pane di Luce",
#             "Funghi dell'Etere",
#             "Spezie Melange",
#         ],
#         "recipe_techniques": [
#             "Cottura a Vapore con Flusso di Particelle Isoarmoniche",
#             "Cottura a Vapore Termocinetica Multipla",
#             "Taglio a Risonanza Sonica Rigenerativa",
#             "Cottura con Microonde Entropiche Sincronizzate",
#         ],
#     }
# ]


# def process_recipes_pipeline():
#     """
#     Processes the recipe data.
#     Returns:
#         dict: A dictionary containing the processed recipe data.
#     """
#     return example_data


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

    for question in question_data:
        parsed_question = question["parsed_question"]
        matching_recipes = []
        matching_recipes_metadata = []

        for recipe in recipe_data:
            recipe_ingredients = recipe["recipe_ingredients"]
            recipe_techniques = recipe["recipe_techniques"]

            # Check if any ingredient in the parsed question matches the recipe ingredients
            if parsed_question["ingredients_ok"]:
                if any(
                    ingredient in recipe_ingredients
                    for ingredient in parsed_question["ingredients_ok"]
                ):
                    matching_recipes.append(recipe["recipe_name"])
                    matching_recipes_metadata.append(recipe)

            # Check if any technique in the parsed question matches the recipe techniques
            if parsed_question["techniques_ok"]:
                if any(
                    technique in recipe_techniques
                    for technique in parsed_question["techniques_ok"]
                ):
                    matching_recipes.append(recipe["recipe_name"])
                    matching_recipes_metadata.append(recipe)

            # Exclude recipes with ingredients or techniques in the ko lists
            if parsed_question["ingredients_ko"]:
                if any(
                    ingredient in recipe_ingredients
                    for ingredient in parsed_question["ingredients_ko"]
                ):
                    matching_recipes = [
                        r for r in matching_recipes if r != recipe["recipe_name"]
                    ]
                    matching_recipes_metadata = [
                        r for r in matching_recipes_metadata if r != recipe
                    ]

            if parsed_question["techniques_ko"]:
                if any(
                    technique in recipe_techniques
                    for technique in parsed_question["techniques_ko"]
                ):
                    matching_recipes = [
                        r for r in matching_recipes if r != recipe["recipe_name"]
                    ]
                    matching_recipes_metadata = [
                        r for r in matching_recipes_metadata if r != recipe
                    ]

        question["matching_recipes"] = matching_recipes
        question["matching_recipes_metadata"] = matching_recipes_metadata

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
