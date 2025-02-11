import json

from src.config import Config
from src.pipeline.questions import process_questions_pipeline
from src.pipeline.recipes import process_recipes_pipeline
from src.pipeline.recipes_matching import match_recipes_pipeline
from src.utils.misc import get_output_df


def main():
    """Main pipeline"""

    # Get data paths
    paths = Config.get_data_paths()

    # Process questions
    questions_data = process_questions_pipeline(
        input_path=paths["questions_path"],
        output_path=paths["output_questions_path"],
    )

    # Process recipes
    recipes_data = process_recipes_pipeline(
        input_path=paths["raw_recipes_path"],
        recipes_output_path=paths["output_recipes_path"],
        restaurant_output_path=paths["output_restaurants_path"],
    )
    recipes_mapping = json.load(open(paths["recipes_mapping_path"]))

    # Match recipes with questions
    questions_recipes_mapped = match_recipes_pipeline(
        output_path=paths["output_mapped_path"],
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
