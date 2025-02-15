from .misc import roman_to_int


def check_and_conditions(question, recipe, conditions):
    for q_key, r_key in conditions:
        if question.get(q_key) and question.get(q_key).get("and"):
            if recipe.get(r_key) is None:
                return False
            else:
                if not all(
                    item in recipe.get(r_key, ["error"])
                    for item in question[q_key].get("and", [])
                ):
                    return False
    return True


def check_or_conditions(question, recipe, conditions):
    for q_key, r_key in conditions:
        if question.get(q_key):
            or_length = question[q_key].get("or_length", 1)
            if question[q_key].get("or"):
                if recipe.get(r_key) is None:
                    return False
                else:
                    if or_length is not None:
                        if (
                            len(
                                [
                                    item
                                    for item in question[q_key].get("or")
                                    if item in recipe.get(r_key, ["error"])
                                ]
                            )
                            < or_length
                        ):
                            return False
    return True


def check_not_conditions(question, recipe, conditions):
    for q_key, r_key in conditions:
        if question.get(q_key) and question.get(q_key).get("not"):
            if recipe.get(r_key) is None:
                return False
            else:
                if any(
                    item in recipe.get(r_key, ["error"])
                    for item in question[q_key].get("not", [])
                ):
                    return False
    return True


def check_additional_filters(question, recipe):
    # Single match 1 to 1
    for q_key, r_key in [
        ("group", "recipe_group"),
        ("restaurants", "recipe_restaurant"),
    ]:
        if question.get(q_key) and recipe.get(r_key):
            if question.get(q_key) != recipe.get(r_key):
                return False

    # Multiple many to 1
    for q_key, r_key in [
        ("planet", "restaurant_planet"),
    ]:
        if question.get(q_key) and recipe.get(r_key):
            if not any(item == recipe.get(r_key) for item in question.get(q_key)):
                return False

    # Multiple many to many
    if question["sirius_flag"]:
        print("jamm")
        for q_key, r_key in [
            ("sirius_techniques_groups", "recipe_technique_groups"),
        ]:
            if question.get(q_key) and recipe.get(r_key):
                if not all(
                    item in recipe.get(r_key, ["error"]) for item in question.get(q_key)
                ):
                    return False

    # Filter based on licenses
    if question.get("licence_name"):
        required_license_name = question["licence_name"]
        chef_licenses = recipe.get("chef_licences", [])

        if not any(
            license_name == required_license_name
            for license in chef_licenses
            for license_name in license.keys()
        ):
            return False

    if question.get("licence_level") and question.get("licence_condition"):
        chef_licenses = recipe.get("chef_licences", [])
        required_license_level = question["licence_level"]
        required_license_condition = question["licence_condition"]

        if not any(
            (
                roman_to_int(license_level) >= roman_to_int(required_license_level)
                if required_license_condition == "higher"
                else roman_to_int(license_level) == roman_to_int(required_license_level)
            )
            for license in chef_licenses
            for license_level in license.values()
        ):
            return False

    return True
