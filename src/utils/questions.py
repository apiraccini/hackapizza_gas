import json
from typing import Dict, List

import pandas as pd
from tqdm import tqdm

from src.config import Config

from .llm import call_llm, get_model_source

questions = pd.read_csv("data/raw/domande.csv")


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
    for request in tqdm(questions["domanda"]):
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

    with open("data/processed/parsed_questions.json", "w") as f:
        json.dump(output, f)

    return output
