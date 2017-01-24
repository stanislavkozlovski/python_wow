""" This file holds constant variables """
from models.creatures.creature_defaults.loader import load_creature_defaults
from models.misc.loader import load_character_level_stats, load_character_xp_requirements


ZONE_MOVE_BLOCK_SPECIAL_KEY = '$'
GARRICK_PADFOOT_GUID = 14

KEY_ARMOR_ATTRIBUTE = "armor"
KEY_STRENGTH_ATTRIBUTE = "strength"
KEY_HEALTH_ATTRIBUTE = "health"
KEY_MANA_ATTRIBUTE = "mana"
KEY_AGILITY_ATTRIBUTE = 'agility'
KEY_BONUS_HEALTH_ATTRIBUTE = 'bonus_health'
KEY_BONUS_MANA_ATTRIBUTE = 'bonus_mana'

KEY_LEVEL_STATS_HEALTH = 'health'
KEY_LEVEL_STATS_MANA = 'mana'

CHAR_STARTER_ZONE, CHAR_STARTER_SUBZONE = "Northshire Abbey", "Northshire Valley"

# these functions run only once due to a decorator
CREATURE_DEFAULT_VALUES = load_creature_defaults()
CHARACTER_LEVELUP_BONUS_STATS = load_character_level_stats()
CHARACTER_LEVEL_XP_REQUIREMENTS = load_character_xp_requirements()

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

KEY_LEVELUP_STATS_HEALTH = 'health'
KEY_LEVELUP_STATS_MANA = 'mana'
KEY_LEVELUP_STATS_STRENGTH = 'strength'
KEY_LEVELUP_STATS_ARMOR = 'armor'
KEY_LEVELUP_STATS_AGILITY = 'agility'
