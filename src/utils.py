import importlib
import inspect
import os

import aisuite as ai
from dotenv import load_dotenv

load_dotenv()

provider_configs = {"groq": {"api_key": os.getenv("GROQ_API_KEY")}}


def call_llm(
    message,
    sys_message="You are a helpful agent.",
    model="groq:llama-3.2-3b-preview",
    json_output=False,
):
    """Call the llm model with the given message and system message

    Args:
        message (str): the message to be sent to the model
        sys_message (str): the system message to be sent to the model
        model (str): the model to be used
        json_output (bool): whether to return the output in json format
    """

    client = ai.Client(provider_configs=provider_configs)

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
    """Get the source code of a class in a module"""

    module = importlib.import_module(module_name)
    model_class = getattr(module, class_name)
    return inspect.getsource(model_class)
