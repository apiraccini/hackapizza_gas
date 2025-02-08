from typing import Dict, List

from pydantic import BaseModel, Field


class Request(BaseModel):
    """a pydantic model to extract the request information"""

    ingredients_yes: List[str] = Field(
        default=None, description="List of desired ingredients"
    )
    ingredients_no: List[str] = Field(
        default=None, description="List of undesired ingredients"
    )
    techniques_yes: List[str] = Field(
        default=None, description="List of desired techniques"
    )
    techniques_no: List[str] = Field(
        default=None, description="List of undesired techniques"
    )
    planets_ok: List[str] = Field(default=None, description="List of desired planets")
    planets_ok: List[str] = Field(default=None, description="List of desired planets")
    licences: List[Dict[str, str]] = Field(
        default=None, description="List of dict with keys 'name' and 'level'"
    )
