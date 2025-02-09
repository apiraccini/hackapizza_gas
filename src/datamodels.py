from typing import Dict, List

from pydantic import BaseModel, Field


class Request(BaseModel):
    """A Pydantic model to extract and validate the request information from clients."""

    ingredients_ok: List[str] = Field(
        default=None, description="List of desired ingredients"
    )
    ingredients_ko: List[str] = Field(
        default=None, description="List of undesired ingredients"
    )
    techniques_ok: List[str] = Field(
        default=None, description="List of desired techniques"
    )
    techniques_ko: List[str] = Field(
        default=None, description="List of undesired techniques"
    )
    planets_ok: List[str] = Field(default=None, description="List of desired planets")
    planets_ko: List[str] = Field(default=None, description="List of undesired planets")
    restaurants_ok: List[str] = Field(
        default=None, description="List of desired restaurants"
    )
    restaurants_ko: List[str] = Field(
        default=None, description="List of undesired restaurants"
    )
    groups_ok: List[str] = Field(
        default=None, description="List of desired groups of appartenence"
    )
    groups_ko: List[str] = Field(
        default=None, description="List of undesired groups of appartenence"
    )
    licences: List[Dict[str, str]] = Field(
        default=None,
        description="List of dict with keys 'name' and 'level' representing licences",
    )

class DishRecipe(BaseModel):
    """A Pydantic model to extract and validate the information about a dish's recipe."""

    
    # recipe_text:str = Field(
    #     default=None, description="Text of the recipe"
    # )
    recipe_ingredients: List[str] = Field(
        default=None, description="List of ingredients that compose a recipe"
    )
    recipe_techniques: List[str] = Field(
        default=None, description="List of techniques used in the recipe"
    )