import json

import pandas as pd

from src.utils.questions import process_questions


def process_questions_pipeline():
    """
    Reads questions from a CSV file, processes them, and returns the processed questions.
    Returns:
        dict: A dictionary containing the processed questions.
    """

    questions_df = pd.read_csv("data/raw/domande.csv")
    processed_questions_list = process_questions(questions_df=questions_df)

    return processed_questions_list


def main():
    processed_questions = process_questions_pipeline()
    json.dumps(processed_questions[0], indent=4)


if __name__ == "__main__":
    main()
