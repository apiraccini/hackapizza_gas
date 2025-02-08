import pandas as pd

from src.utils import call_llm, get_model_source

provider = "groq"
model = "llama-3.3-70b-versatile"


questions = pd.read_csv("data/domande.csv")


def main():
    output_model_str = get_model_source("src.datamodels", "Request")

    request = questions["domanda"].sample(1).values[0]

    system_message = f"""
    Yuo are a helpful assistant that parsers the request of the user.
    In this case the users will be client of a restaurants that want to know which are the dishes that satisty their requirements.
    You must extract the information using the pydantic model below and return a json format.\n\n{output_model_str}"""
    message = f"This is the client request: {request}. Return only the json instance representing the request."

    response = call_llm(
        message=message,
        sys_message=system_message,
        model=f"{provider}:{model}",
        json_output=True,
    )

    print(f"Request: {request}\nResponse: {response}")


if __name__ == "__main__":
    main()
