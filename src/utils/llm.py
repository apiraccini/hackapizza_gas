import importlib
import inspect
import json
import os
from typing import Dict, List

import aisuite as ai
from dotenv import load_dotenv
from tqdm import tqdm

from src.config import Config

load_dotenv()


def process_data(
    data: List[Dict[str, str]],
    key: str,
    system_message_template: str,
    message_template: str,
    output_model_str: str,
) -> List[Dict[str, str]]:
    """Processes a list of dictionaries to extract relevant information using a language model.

    Args:
        data (List[Dict[str, str]]): List of dictionaries containing the data.
        key (str): Key to process.
        system_message_template (str): Template for the system message.
        message_template (str): Template for the user message.
        output_model_str (str): String representation of the output model.

    Returns:
        List[Dict[str, str]]: List of dictionaries with original and parsed data.
    """

    provider = Config.provider
    model = Config.model

    for item in tqdm(data):
        system_message = system_message_template.format(
            output_model_str=output_model_str
        )
        message = message_template.format(request=item[key])

        try:
            response = call_llm(
                message=message,
                sys_message=system_message,
                model=f"{provider}:{model}",
                json_output=True,
            )
            response = json.loads(response)
            item.update(response)
        except Exception:
            item["error"] = "Error"

    return data


def call_llm(
    message,
    sys_message="You are a helpful agent.",
    model=f"{Config.provider}:{Config.model}",
    json_output=False,
):
    """Call the llm model with the given message and system message

    Args:
        message (str): the message to be sent to the model
        sys_message (str): the system message to be sent to the model
        model (str): the model to be used
        json_output (bool): whether to return the output in json format

    Returns:
        str: the response from the model
    """

    client = ai.Client(
        provider_configs={"groq": {"api_key": os.getenv("GROQ_API_KEY")}}
    )

    messages = [
        {"role": "system", "content": sys_message},
        {"role": "user", "content": message},
    ]

    if json_output:
        response_format = {"type": "json_object"}
        response = client.chat.completions.create(
            model=model, messages=messages, response_format=response_format
        )
    else:
        response = client.chat.completions.create(model=model, messages=messages)

    return response.choices[0].message.content


def get_model_source(module_name, class_name):
    """Get the source code of a class in a module

    Args:
        module_name (str): the name of the module
        class_name (str): the name of the class

    Returns:
        str: the source code of the class
    """

    module = importlib.import_module(module_name)
    model_class = getattr(module, class_name)
    return inspect.getsource(model_class)
