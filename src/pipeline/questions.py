import json
from pathlib import Path
from typing import Dict, List

import pandas as pd
from tqdm import tqdm

from src.config import Config
from src.utils.llm import call_llm, get_model_source


def process_questions_pipeline(input_path: Path | str, output_path: Path | str):
    """
    Reads questions from a CSV file, processes them, and returns the processed questions.
    Args:
        input_path (str): Path to the input CSV file.
        output_path (str): Path to the output JSON file.
    Returns:
        dict: A dictionary containing the processed questions.
    """
    input_file = Path(input_path)
    output_file = Path(output_path)

    if output_file.exists():
        with output_file.open("r") as f:
            processed_questions_list = json.load(f)
    else:
        questions_df = pd.read_csv(input_file)
        processed_questions_list = process_questions(questions_df=questions_df)
        with output_file.open("w") as f:
            json.dump(processed_questions_list, f, indent=4)

    return processed_questions_list


def process_questions(questions_df: pd.DataFrame) -> List[Dict[str, str]]:
    """Processes questions to extract relevant information using a language model.

    Args:
        questions_df (pd.DataFrame): DataFrame containing the questions.

    Returns:
        List[Dict[str, str]]: List of dictionaries with original and parsed questions.
    """

    provider = Config.provider
    model = Config.model
    output_model_str = get_model_source("src.datamodels", "Request")

    output = []
    for request in tqdm(questions_df["domanda"]):
        system_message = Config.system_message_template_questions.format(
            output_model_str=output_model_str
        )
        message = Config.message_template_questions.format(request=request)

        try:
            response = call_llm(
                message=message,
                sys_message=system_message,
                model=f"{provider}:{model}",
                json_output=True,
            )
            response = json.loads(response)
            output.append({"question": request, "parsed_question": response})
        except Exception:
            output.append({"question": request, "parsed_question": "Error"})

    return output
