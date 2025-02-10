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
    techniques_groups: Dict[
        Literal["and", "or", "or_length", "not"],
        List[
            Literal[
                "Marinatura",
                "Affumicatura",
                "Fermentazione",
                "Decostruzione",
                "Sferificazione",
                "Tecniche di Taglio",
                "Tecniche di Impasto",
                "Surgelamento",
                "Bolllitura",
                "Grigliatura",
                "Cottura",
            ]
        ],
    ] = Field(
        default=None,
        description="Dictionary with keys: 'and' for desired techniques groups, 'or' for optional techniques groups, 'or_length' for the length of optional techniques groups, 'not' for undesired techniques groups",
    )
    restaurants: Dict[
        Literal["and", "or", "or_length", "not"],
        List[
            Literal[
                "Il Firmamento",
                "Anima Cosmica",
                "L'Equilibrio Quantico",
                "L'Essenza del Multiverso su Pandora",
                "Le Dimensioni del Gusto",
                "L'Essenza di Asgard",
                "Datapizza",
                "Sapore del Dune",
                "L'Essenza Cosmica",
                "L'Oasi delle Dune Stellari",
                "Quantico",
                "Le Stelle Danzanti",
                "Stelle Astrofisiche",
                "Le Stelle che Ballano",
                "L'Eco dei Sapori",
                "Sala del Valhalla",
                "Cosmica Essenza",
                "L'Architetto dell'Universo",
                "L'Eco di Pandora",
                "Stelle dell'Infinito Celestiale",
                "Tutti a TARSvola",
                "L'Infinito in un Boccone",
                "L'Eredità Galattica",
                "L'Etere del Gusto",
                "Armonia Universale",
                "Il Ristorante delle Dune Stellari",
                "Universo Gastronomico di Namecc",
                "L'Universo in Cucina",
                "L'Essenza dell'Infinito",
            ]
        ],
    ] = Field(
        default=None,
        description="Dictionary with keys: 'and' for desired restaurants, 'or' for optional restaurants, 'or_length' for the length of optional restaurants, 'not' for undesired restaurants",
    )
    groups: Dict[Literal["and", "or", "or_length", "not"], List[str]] = Field(
        default=None,
        description="Dictionary with keys: 'and' for desired groups of appartenence, 'or' for optional groups, 'or_length' for the length of optional groups, 'not' for undesired groups",
    )
    licences: conlist(Dict[Literal["name", "level"], str], min_items=0) = Field(
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
        min_items=0,
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
        min_items=0,
    ) = Field(
        default=None,
        description="List of undesired planets",
    )
    galactic_code: conlist(
        Literal["corrette licenze e certificazioni", "quantita legali"], min_items=0
    ) = Field(
        default=None,
        description="List of galactic code requirements",
    )


class DishRecipe(BaseModel):
    """A Pydantic model to extract and validate the ingredients and techniques about a dish's recipe."""

    recipe_ingredients: conlist(str, min_items=0) = Field(
        default=None, description="List of ingredients that compose a recipe"
    )
    recipe_techniques: conlist(str, min_items=0) = Field(
        default=None, description="List of techniques used in the recipe"
    )
    recipe_techniques_groups: conlist(
        Literal[
            "Marinatura",
            "Affumicatura",
            "Fermentazione",
            "Decostruzione",
            "Sferificazione",
            "Tecniche di Taglio",
            "Tecniche di Impasto",
            "Surgelamento",
            "Bolllitura",
            "Grigliatura",
            "Cottura",
        ],
        min_items=0,
    ) = Field(
        default=None,
        description="List of parent groups of the techniques used in the recipe",
    )
