import aisuite as ai


def ask(
    message, sys_message="You are a helpful agent.", model="groq:llama-3.2-3b-preview"
):
    # Initialize the AI client for accessing the language model
    client = ai.Client()

    # Construct the messages list for the chat
    messages = [
        {"role": "system", "content": sys_message},
        {"role": "user", "content": message},
    ]

    # Send the messages to the model and get the response
    response = client.chat.completions.create(model=model, messages=messages)

    # Return the content of the model's response
    return response.choices[0].message.content


ask("Hi. what is capital of Japan?")
