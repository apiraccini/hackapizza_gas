from typing import Dict, List, Literal

from pydantic import BaseModel, Field, conlist


class RequestModel(BaseModel):
    """A Pydantic model to extract and validate the request information from clients."""

    ingredients: Dict[Literal["and", "or", "or_length", "not"], List[str]] = Field(
        default=None,
        description="Dictionary with keys: 'and' for desired ingredients, 'or' for optional ingredients, 'or_length' for the length of optional ingredients ('A or B' would be 1, 'at least two would' be 2,...) and 'not' for undesired ingredients",
    )
    techniques: Dict[Literal["and", "or", "or_length", "not"], List[str]] = Field(
        default=None,
        description="Dictionary with keys: 'and' for desired techniques, 'or' for optional techniques, 'or_length' for the length of optional techniques, 'not' for undesired techniques",
    )
    restaurants: Dict[
        Literal["and", "or", "or_length", "not"],
        List[
            Literal[
                "Anima Cosmica",
                "L Eco dei Sapori",
                "Sapore del Dune",
                "L Architetto dell Universo",
                "L Essenza di Asgard",
                "Il Firmamento",
                "Eco di Pandora",
                "L Equilibrio Quantico",
                "L Infinito Sapore",
                "Le Stelle che Ballano",
                "Essenza dell Infinito",
                "L infinito in un Boccone",
                "L Etere del Gusto",
                "L Universo in Cucina",
                "Cosmica Essenza",
                "Sala del Valhalla",
                "Le Stelle Danzanti",
                "Universo Gastronomico di Namecc",
                "Eredita Galattica",
                "L Oasi delle Dune Stellari",
                "Ristorante delle Dune Stellari",
                "L Essenza delle Dune",
                "Ristorante Quantico",
                "Stelle Astrofisiche",
                "Stelle dell Infinito Celestiale",
                "L Essenza del Multiverso su Pandora",
                "L Essenza Cosmica",
                "Armonia Universale",
                "Tutti a TARSvola",
                "Le Dimensioni del Gusto",
            ]
        ],
    ] = Field(
        default=None,
        description="Dictionary with keys: 'and' for desired restaurants, 'or' for optional restaurants, 'or_length' for the length of optional restaurants, 'not' for undesired restaurants",
    )
    group: Literal[
        "Ordine della Galassia di Andromeda",
        "Ordine dei Naturalisti",
        "Ordine degli Armonisti",
    ] = Field(
        default=None,
        description="Desired groups of appartenence for the client",
    )
    licence_name: Literal[
        "Psionica (P)",
        "Gravitazionale (G)",
        "Antimateria (e+)",
        "Magnetica (Mx)",
        "grado tecnologico LTK",
    ] = Field(default=None, description="Name of the license")
    licence_level: int = Field(
        default=None,
        description="Level of the license is integer",
    )
    licence_condition: Literal["higher", "equal"] = Field(
        default="equal", description="Condition for the license level"
    )
    planets_ok: conlist(
        Literal[
            "Tatooine",
            "Asgard",
            "Namecc",
            "Arrakis",
            "Krypton",
            "Pandora",
            "Cybertron",
            "Ego",
            "Montressosr",
            "Klyntar",
        ],
        min_length=0,
    ) = Field(
        default=None,
        description="List of desired planets",
    )
    planets_distance: int = Field(
        default=None,
        description="Distance in light years from the desired planet",
    )
    galactic_code: conlist(
        Literal["corrette licenze e certificazioni", "quantita legali"], min_length=0
    ) = Field(
        default=None,
        description="List of galactic code requirements",
    )


class RecipeModel(BaseModel):
    """A Pydantic model to extract and validate the ingredients and techniques about a dish's recipe."""

    recipe_ingredients: conlist(str, min_length=0) = Field(
        default=None, description="List of ingredients that compose a recipe"
    )
    recipe_techniques: conlist(str, min_length=0) = Field(
        default=None, description="List of techniques used in the recipe"
    )
    recipe_group: Literal[
        "Ordine della Galassia di Andromeda",
        "Ordine dei Naturalisti",
        "Ordine degli Armonisti",
    ] = Field(
        default=None,
        description="Group of people that can eat that recipe (if specifically mentioned)",
    )


class RestaurantModel(BaseModel):
    """A Pydantic model to extract and validate the information about a restaurant."""

    restaurant_chef: str = Field(
        default=None, description="Name of the chef of the restaurant"
    )
    restaurant_planet: conlist(
        Literal[
            "Tatooine",
            "Asgard",
            "Namecc",
            "Arrakis",
            "Krypton",
            "Pandora",
            "Cybertron",
            "Ego",
            "Montressosr",
            "Klyntar",
        ],
        min_length=0,
    ) = Field(
        default=None,
        description="Planet of the restaurant",
    )
    chef_licences: conlist(
        Dict[
            Literal[
                "Psionica (P)",
                "Gravitazionale (G)",
                "Antimateria (e+)",
                "Magnetica (Mx)",
                "grado tecnologico LTK",
            ],
            int,
        ],
        min_length=0,
    ) = Field(
        default=None,
        description="List of licenses held by the chef with their levels",
    )
    restricted_ingredients: conlist(
        Dict[str, Dict[str, int]],
        min_length=0,
    ) = Field(
        default=None,
        description="List of restricted ingredients with their quantities",
    )
