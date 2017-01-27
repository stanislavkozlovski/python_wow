"""
This module holds helper functions.
i.e functions that do not serve any specific purpose but are needed in multiple places
"""
from copy import deepcopy


def parse_int(value) -> int:
    """
    this function is used to parse data from the DB into an integer.
    because a lot of the cells can be empty, we get None as the return type. This function makes sure we
    get 0 if the value is None or empty

    !!! IMPORTANT !!!
    This is to be added to values where we would not want to cause an exception if they were None(Null), like
    the amount of gold a character has or the amount of armor an item gives.
    On other cases, like cells pointing to certain other database IDs, a missing number there makes the row
    invalid, thus we want to create an exception.
    """
    try:
        val = int(value)
        return val
    except (TypeError, ValueError):
        return 0


def create_attributes_dict(bonus_health: int=0, bonus_mana: int=0, armor: int=0, strength: int=0,
                           agility: int=0) -> dict:
    """
    This function takes in stats (attributes) like bonus_health, strength, armor, etc and converts them into a
    pre-defined dictionary holding all of them. This enables easier passing and application of said attributes
    :return: a dict like {"strength": 10, "armor": 4}
    """
    from constants import (  # Hackish import to prevent an import loop
        KEY_ARMOR_ATTRIBUTE, KEY_BONUS_HEALTH_ATTRIBUTE, KEY_BONUS_MANA_ATTRIBUTE,
        KEY_AGILITY_ATTRIBUTE, KEY_STRENGTH_ATTRIBUTE)

    return {KEY_BONUS_HEALTH_ATTRIBUTE: bonus_health, KEY_BONUS_MANA_ATTRIBUTE: bonus_mana,
            KEY_ARMOR_ATTRIBUTE: armor, KEY_STRENGTH_ATTRIBUTE: strength, KEY_AGILITY_ATTRIBUTE: agility}


def display_attributes(attributes: dict) -> str:
    """
    This function read a dictionary with attributes and returns a string displaying the attributes it gives.
    A template: {armor} {health} {mana} {strength} {agility}
    If any are missing, we don't add them
    """

    attributes_to_print = [f'{attr.replace("bonus_", "")}: {val}' for attr, val in attributes.items() if val]

    return ", ".join(attributes_to_print)


def create_character_attributes_template() -> dict:
    """
    Gets the CHARACTER_ATTRIBUTES_TEMPLATE from constants.py,
        copies it and returns it.
    This is needed, otherwise Characters would have the same reference to a dictionary, which
    creates problems while testing and would create problems if players could switch characters
    """
    from constants import CHAR_ATTRIBUTES_TEMPLATE  # Hackish import to prevent an import loop
    return deepcopy(CHAR_ATTRIBUTES_TEMPLATE)
