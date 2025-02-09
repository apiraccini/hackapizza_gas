import json
from pathlib import Path

import pandas as pd

from src.pipeline.questions import process_questions_pipeline
from src.pipeline.recipes import process_recipes_pipeline
from src.pipeline.recipes_matching import match_recipes_pipeline


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

    # Process recipes
    print("Processing recipes")
    recipes_data = process_recipes_pipeline(
        input_path=raw_recipes_path, output_path=data_path / "processed/recipes.json"
    )
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
    df = pd.DataFrame(
        {
            "row_id": range(1, len(questions_recipes_mapped) + 1),
            "result": [
                str(item["matching_recipes_ids"][0])
                if len(item["matching_recipes_ids"]) == 1
                else ",".join(map(str, item["matching_recipes_ids"]))
                if item["matching_recipes_ids"]
                else "0"
                for item in questions_recipes_mapped
            ],
        }
    )
    df.to_csv(data_path / "processed/result.csv", index=False)

    print("Pipeline completed successfully")
    print(json.dumps(questions_recipes_mapped, indent=4))


if __name__ == "__main__":
    main()
