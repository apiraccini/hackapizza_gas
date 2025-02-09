import json
from pathlib import Path

from src.pipeline.questions import process_questions_pipeline
from src.pipeline.recipes import match_recipes_pipeline, process_recipes_pipeline


def main():
    """Main pipeline"""

    # Define paths
    data_path = Path("data")
    questions_path = data_path / "raw/domande.csv"
    parsed_questions_path = data_path / "processed/parsed_questions.json"
    recipes_mapping_path = data_path / "raw/Misc/dish_mapping.json"

    # Process questions
    questions_data = process_questions_pipeline(
        input_path=questions_path, output_path=parsed_questions_path
    )

    # Process recipes
    recipes_data = process_recipes_pipeline()
    recipes_mapping = json.load(open(recipes_mapping_path))

    questions_recipes_mapped = match_recipes_pipeline(
        output_path="data/processed/questions_with_recipes.json",
        recipes_data=recipes_data,
        questions_data=questions_data,
        mapping=recipes_mapping,
    )

    print(json.dumps(questions_recipes_mapped, indent=4))


if __name__ == "__main__":
    main()
