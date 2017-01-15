""" This file holds constant variables """
from models.creatures.creature_defaults.loader import load_creature_defaults

CREATURE_DEFAULT_ATTRIBUTES = load_creature_defaults()  # this function runs only once due to a decorator
