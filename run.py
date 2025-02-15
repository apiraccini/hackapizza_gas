import json

from src.config import Config
from src.pipeline.matching import match_recipes_pipeline
from src.pipeline.questions import process_questions_pipeline
from src.pipeline.recipes import process_recipes_pipeline
from src.utils.misc import get_output_df, normalise_keys


def main():
    """Main pipeline"""
    print("Starting pipeline")

    # Get data paths
    paths = Config.data_path_dict
    print("Data paths retrieved")

    # Process questions
    print("Processing questions")
    questions_data = process_questions_pipeline(
        input_path=paths["input_questions_path"],
        output_path=paths["output_questions_path"],
    )

    # Process recipes
    print("Processing recipes")
    recipes_mapping = json.load(open(paths["recipes_mapping_path"]))
    recipes_mapping = normalise_keys(recipes_mapping)

    recipes_data, _ = process_recipes_pipeline(
        input_path=paths["input_recipes_path"],
        recipes_output_path=paths["output_recipes_path"],
        restaurant_output_path=paths["output_restaurants_path"],
    )

    # Match recipes with questions
    print("Matching recipes with questions")
    questions_recipes_mapped = match_recipes_pipeline(
        output_path=paths["output_result_json"],
        recipes_data=recipes_data,
        questions_data=questions_data,
        mapping=recipes_mapping,
    )

    # Save results
    print("Saving results")
    df = get_output_df(questions_recipes_mapped)
    df.to_csv(paths["output_result_path"], index=False)

    print("Pipeline completed successfully")


if __name__ == "__main__":
    main()
