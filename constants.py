""" This file holds constant variables """
from models.creatures.creature_defaults.loader import load_creature_defaults

CREATURE_DEFAULT_VALUES = load_creature_defaults()  # this function runs only once due to a decorator

CHARACTER_EQUIPMENT_HEADPIECE_KEY = 'headpiece'
CHARACTER_EQUIPMENT_SHOULDERPAD_KEY = 'shoulderpad'
CHARACTER_EQUIPMENT_NECKLACE_KEY = 'necklace'
CHARACTER_EQUIPMENT_CHESTGUARD_KEY = 'chestguard'
CHARACTER_EQUIPMENT_BRACER_KEY = 'bracer'
CHARACTER_EQUIPMENT_GLOVES_KEY = 'gloves'
CHARACTER_EQUIPMENT_BELT_KEY = 'belt'
CHARACTER_EQUIPMENT_LEGGINGS_KEY = 'leggings'
CHARACTER_EQUIPMENT_BOOTS_KEY = 'boots'

CHARACTER_DEFAULT_EQUIPMENT = {CHARACTER_EQUIPMENT_HEADPIECE_KEY: None,
                               CHARACTER_EQUIPMENT_SHOULDERPAD_KEY: None,
                               CHARACTER_EQUIPMENT_NECKLACE_KEY: None,
                               CHARACTER_EQUIPMENT_CHESTGUARD_KEY: None,
                               CHARACTER_EQUIPMENT_BRACER_KEY: None,
                               CHARACTER_EQUIPMENT_GLOVES_KEY: None,
                               CHARACTER_EQUIPMENT_BELT_KEY: None,
                               CHARACTER_EQUIPMENT_LEGGINGS_KEY: None,
                               CHARACTER_EQUIPMENT_BOOTS_KEY: None}
