import json
from pathlib import Path

from src.pipeline.questions import process_questions_pipeline
from src.pipeline.recipes import process_recipes_pipeline
from src.pipeline.recipes_matching import match_recipes_pipeline
from src.utils.misc import get_output_df, normalise_strings


def main():
    """Main pipeline"""
    print("Starting main pipeline")

    # Define paths
    data_path = Path("data")
    questions_path = data_path / "raw/domande.csv"
    raw_recipes_path = data_path / "processed/menu_md"
    recipes_mapping_path = data_path / "raw/Misc/dish_mapping.json"

    # Process questions
    print("Processing questions")
    questions_data = process_questions_pipeline(
        input_path=questions_path,
        output_path=data_path / "processed/parsed_questions.json",
    )
    questions_data = normalise_strings(questions_data)

    # Process recipes
    print("Processing recipes")
    recipes_data = process_recipes_pipeline(
        input_path=raw_recipes_path, output_path=data_path / "processed/recipes.json"
    )
    recipes_data = normalise_strings(recipes_data)
    recipes_mapping = json.load(open(recipes_mapping_path))

    # Match recipes with questions
    print("Matching recipes with questions")
    questions_recipes_mapped = match_recipes_pipeline(
        output_path="data/processed/questions_with_recipes.json",
        recipes_data=recipes_data,
        questions_data=questions_data,
        mapping=recipes_mapping,
    )

    # Save results
    print("Saving results")
    df = get_output_df(questions_recipes_mapped)
    df.to_csv(data_path / "processed/result.csv", index=False)

    print("Pipeline completed successfully")


if __name__ == "__main__":
    main()
