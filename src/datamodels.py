from typing import Dict, List

from pydantic import BaseModel, Field


class Request(BaseModel):
    """A Pydantic model to extract and validate the request information from clients."""

    ingredients: Dict[str, List[str]] = Field(
        default=None,
        description="Dictionary with keys 'and' for desired ingredients, 'or' for optional ingredients, 'or_lenght' for the lenght of optional arguments ('A or B' woud be 1, 'at lest two would' be 2,...) and 'not' for undesired ingredients",
    )
    techniques: Dict[str, List[str]] = Field(
        default=None,
        description="Dictionary with keys 'and' for desired techniques, 'or' for optional techniques, 'or_lenght' for the lenght of optional arguments and 'not' for undesired techniques",
    )
    techniques_group: str = Field(
        default=None,
        description="Group of techniques that must be present in the recipe (one of Marinatura, Affumicatura, Fermentazione, Decostruzione, Sferificazione, Tecniche di Taglio, Tecniche di Impasto, Surgelamento, Bolllitura, Grigliatura, Cottura al forno, Cottura al vapore, Cottura sottovuoto, Cottura al salto)",
    )
    restaurants: Dict[str, List[str]] = Field(
        default=None,
        description="Dictionary with keys 'and' for desired restaurants, 'or', 'or_lenght' for the lenght of optional arguments for optional techniques and 'not' for undesired restaurants",
    )
    groups: Dict[str, List[str]] = Field(
        default=None,
        description="Dictionary with keys 'and' for desired groups of appartenence, 'or' for optional groups, 'or_lenght' for the lenght of optional arguments and 'not' for undesired groups",
    )
    licences: List[Dict[str, str]] = Field(
        default=None,
        description="List of dict with keys 'name' and 'level' representing licences",
    )
    planets_ok: List[str] = Field(default=None, description="List of desired planets")
    planets_distance: List[str] = Field(
        default=None,
        description="List of distances in light years from the desired planets",
    )
    planets_ko: List[str] = Field(default=None, description="List of undesired planets")
    galactic_code: List[str] = Field(
        default=None,
        description="A list iwht one or more elements between 'corrette licenze e certificazioni', 'quantita legali'",
    )


class DishRecipe(BaseModel):
    """A Pydantic model to extract and validate the ingredients and techniques about a dish's recipe."""

    recipe_ingredients: List[str] = Field(
        default=None, description="List of ingredients that compose a recipe"
    )
    recipe_techniques: List[str] = Field(
        default=None, description="List of techniques used in the recipe"
    )
