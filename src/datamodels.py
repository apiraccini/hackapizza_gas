from typing import Dict, List, Literal

from pydantic import BaseModel, Field, conlist


class Request(BaseModel):
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
    groups: Dict[
        Literal["and", "or", "or_length", "not"],
        List[
            Literal[
                "Ordine della Galassia di Andromeda",
                "Ordine dei Naturalisti",
                "Ordine degli Armonisti",
            ]
        ],
    ] = Field(
        default=None,
        description="Dictionary with keys: 'and' for desired groups of appartenence, 'or' for optional groups, 'or_length' for the length of optional groups, 'not' for undesired groups",
    )
    licences: conlist(Dict[Literal["name", "level"], str], min_length=0) = Field(
        default=None,
        description="List of dicts with keys: 'name' for license name, 'level' for licences",
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
    planets_distance: List[str] = Field(
        default=None,
        description="List of distances in light years from the desired planets",
    )
    planets_ko: conlist(
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
        description="List of undesired planets",
    )
    galactic_code: conlist(
        Literal["corrette licenze e certificazioni", "quantita legali"], min_length=0
    ) = Field(
        default=None,
        description="List of galactic code requirements",
    )


class DishRecipe(BaseModel):
    """A Pydantic model to extract and validate the ingredients and techniques about a dish's recipe."""

    recipe_ingredients: conlist(str, min_length=0) = Field(
        default=None, description="List of ingredients that compose a recipe"
    )
    recipe_techniques: conlist(str, min_length=0) = Field(
        default=None, description="List of techniques used in the recipe"
    )


class Restaurant(BaseModel):
    """A Pydantic model to extract and validate the information about a restaurant."""

    planet: conlist(
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
    ) = (
        Field(
            default=None,
            description="Planet of the restaurant",
        ),
    )
    groups: List[
        Literal[
            "Ordine della Galassia di Andromeda",
            "Ordine dei Naturalisti",
            "Ordine degli Armonisti",
        ]
    ] = Field(
        default=None,
        description="List of groups that can be served by the restaurant, if specifically mentioned",
    )
