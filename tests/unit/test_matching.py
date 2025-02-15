import pytest

from src.utils.matching import (
    check_additional_filters,
    check_and_conditions,
    check_not_conditions,
    check_or_conditions,
)


@pytest.fixture
def sample_data():
    question_and = {
        "ingredients": {"and": ["tomato", "cheese"], "not": ["meat"]},
        "techniques": {"and": ["baking"], "not": ["frying"]},
        "technique_groups": {"and": ["group1"], "not": ["group3"]},
        "group": "groupA",
        "restaurants": "restaurant1",
        "planet": ["planet1", "planet2"],
        "licence_name": "basic",
        "licence_level": "II",
        "licence_condition": "higher",
    }
    question_or = {
        "ingredients": {
            "or": ["basil", "cheese", "banana"],
            "not": ["meat"],
            "or_length": 2,
        },
        "techniques": {"or": ["grilling"], "not": ["frying"]},
        "technique_groups": {"or": ["group2"], "not": ["group3"]},
        "group": "groupA",
        "restaurants": "restaurant1",
        "planet": ["planet1"],
        "licence_name": "basic",
        "licence_level": "II",
        "licence_condition": "higher",
    }
    recipe = {
        "recipe_ingredients": ["tomato", "cheese", "basil"],
        "recipe_techniques": ["baking", "grilling"],
        "recipe_technique_groups": ["group1", "group2"],
        "recipe_group": "groupA",
        "recipe_restaurant": "restaurant1",
        "restaurant_planet": "planet1",
        "chef_licences": [{"basic": "II"}],
    }
    return question_and, question_or, recipe


def test_check_and_conditions(sample_data):
    question_and, _, recipe = sample_data
    conditions = [
        ("ingredients", "recipe_ingredients"),
        ("techniques", "recipe_techniques"),
        ("technique_groups", "recipe_technique_groups"),
    ]
    assert check_and_conditions(question_and, recipe, conditions)


def test_check_or_conditions(sample_data):
    _, question_or, recipe = sample_data
    conditions = [
        ("ingredients", "recipe_ingredients"),
        ("techniques", "recipe_techniques"),
        ("technique_groups", "recipe_technique_groups"),
    ]
    assert check_or_conditions(question_or, recipe, conditions)


def test_check_or_conditions_with_or_length(sample_data):
    _, question_or, recipe = sample_data
    question_or["ingredients"]["or_length"] = 3
    conditions = [
        ("ingredients", "recipe_ingredients"),
        ("techniques", "recipe_techniques"),
        ("technique_groups", "recipe_technique_groups"),
    ]
    assert not check_or_conditions(question_or, recipe, conditions)


def test_check_not_conditions(sample_data):
    question_and, question_or, recipe = sample_data
    conditions = [
        ("ingredients", "recipe_ingredients"),
        ("techniques", "recipe_techniques"),
        ("technique_groups", "recipe_technique_groups"),
    ]
    assert check_not_conditions(question_and, recipe, conditions)
    assert check_not_conditions(question_or, recipe, conditions)


def test_check_additional_filters(sample_data):
    question_and, question_or, recipe = sample_data
    assert check_additional_filters(question_and, recipe)
    assert check_additional_filters(question_or, recipe)
