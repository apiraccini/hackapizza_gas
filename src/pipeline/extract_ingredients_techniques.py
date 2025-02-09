import json
from pathlib import Path
from typing import Dict, List
import json
from tqdm import tqdm
from src.config import Config
from src.utils.llm import call_llm, get_model_source


def extract_ingredients_techniques(data_partial_info:List[Dict]) -> List[Dict]:
    provider = Config.provider
    model = Config.model
    output_model_str = get_model_source("src.datamodels", "DishRecipe")

    output_data_full_info = []
    for data in tqdm(data_partial_info):
        recipe_text = data['recipe_raw_text']
        system_message = Config.system_message_template_dish_recipe.format(
            output_model_str=output_model_str
        )
        message = Config.message_template_dish_recipe.format(dish_recipe=recipe_text)

        try:
            response = call_llm(
                message=message,
                sys_message=system_message,
                model=f"{provider}:{model}",
                json_output=True,
            )
            response = json.loads(response)
            updated_data = {**data, **response}
            output_data_full_info.append(updated_data)
        except Exception as e:
            output_data_full_info.append({**data, "full_info": "Error"})
    return output_data_full_info