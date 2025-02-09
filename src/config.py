class Config:
    provider = "groq"
    model = "llama-3.3-70b-versatile"

    system_message_template_questions = """
    You are a helpful assistant that parses the request of the user.
    In this case, the users will be clients of a restaurant that want to know which dishes satisfy their requirements.
    You must extract the information using the pydantic model below and return a JSON format.\n\n{output_model_str}"""
    message_template_questions = """
    This is the client request: {request}.
    Return only the JSON instance representing the request, with every field (empty ones as well).
    """
    
    system_message_template_dish_recipe = """
    You are a helpful assistant that receive a text containing information about a recipe as input.
    You must extract the information using the pydantic model below and return a JSON format.\n\n{output_model_str}"""
    message_template_dish_recipe = """
    This is the text containing information about the recipe: {dish_recipe}.
    Return only the JSON instance representing information about the recipe.
    """
