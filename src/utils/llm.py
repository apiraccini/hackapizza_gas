import importlib
import inspect
import os

import aisuite as ai
from dotenv import load_dotenv

from src.config import Config

load_dotenv()


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
