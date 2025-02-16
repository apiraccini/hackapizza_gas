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
        description="Dictionary with keys: 'and' for desired techniques, 'or' for optional techniques, 'or_length' for the length of optional techniques ('A or B' would be 1, 'at least two would' be 2,...), 'not' for undesired techniques",
    )
    restaurants: Literal[
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
    ] = Field(
        default=None,
        description="Name of the desired restaurant.",
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
        "licenza psionica (P)",
        "licenza temporale (t)",
        "licenza gravitazionale (G)",
        "licenza antimateria (e+)",
        "licenza magnetica (Mx)",
        "licenza quantica (Q)",
        "licenza luce (C)",
        "licenza tecnologica LTK",
    ] = Field(default=None, description="Name of the license")
    licence_level: str = Field(
        default=None,
        description="Level of the license",
    )
    licence_condition: Literal["higher", "equal"] = Field(
        default=None, description="Condition for the license level"
    )
    planet: Literal[
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
    ] = Field(
        default=None,
        description="List of desired planets",
    )
    planet_distance: int = Field(
        default=None,
        description="Distance in light years from the desired planet",
    )
    sirius_flag: bool = Field(
        default=None,
        description="Flag to indicate if the manual 'Sirius Cosmo' (or 'Sirius') is mentioned",
    )
    sirius_techniques_groups: conlist(
        Literal[
            "marinatura",
            "affumicatura",
            "fermentazione",
            "decostruzione",
            "sferificazione",
            "tecniche di taglio",
            "tecniche di impasto",
            "surgelamento",
            "bollitura",
            "grigliatura",
            "cottura al forno",
            "cottura al vapore",
            "cottura sottovuoto",
            "cottura al salto",
        ],
        min_length=0,
    ) = Field(
        default=None,
        description="List of techniques categories that must be mentioned in the 'Sirius Cosmo' manual if specifically required",
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
        description="Group of people that can eat that recipe (if specifically mentioned). This field is not null only if there is a string like '!! Questo piatto va bene per gli appartenenti all'<recipe_group>!!' in the original text",
    )


class RestaurantModel(BaseModel):
    """A Pydantic model to extract and validate the information about a restaurant."""

    restaurant_chef: str = Field(
        default=None, description="Name of the chef of the restaurant"
    )
    restaurant_planet: Literal[
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
    ] = Field(
        default=None,
        description="Planet of the restaurant",
    )
    chef_licences: Dict[
        Literal[
            "licenza psionica (P)",
            "licenza temporale (t)",
            "licenza gravitazionale (G)",
            "licenza antimateria (e+)",
            "licenza magnetica (Mx)",
            "licenza quantica (Q)",
            "licenza luce (C)",
            "licenza tecnologica LTK",
        ],
        str,
    ] = Field(
        default=None,
        description="List of licenses held by the chef with their levels (e.g. {'licenza psionica (P)': 'II', 'licenza quantica (Q)': 'VI+',...})",
    )
    restricted_ingredients: conlist(
        Dict[
            str,
            Literal[
                "Erba Pipa",
                "Cristalli di Memoria",
                "Petali di Eco",
                "Carne di Drago",
                "Uova di Fenice",
                "Lacrime di Unicorno",
                "Foglie di Mandragora",
                "Muffa Lunare",
                "Nettare di Sirena",
                "Spore Quantiche",
                "Essenza di Vuoto",
                "Funghi dell Etere",
                "Sale Temporale",
                "Radici di Gravita",
                "Polvere di Stelle",
            ],
            int,
        ],
        min_length=0,
    ) = Field(
        default=None,
        description="List of dictionaries with keys 'recipe', 'ingrendient' and 'quantity' to indicate the restricted ingredients",
    )
