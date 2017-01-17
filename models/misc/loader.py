from database.main import session
from models.misc.levelup_stats import LevelUpStats
from decorators import run_once
from utils.helper import parse_int


@run_once
def load_character_level_stats() -> dict:
    """
    Return a dictionary holding information about the amount of stats that a character should get according
    to the level he has just attained
    """
    # Define these here as well. We can't import from constants because constants imports from here
    KEY_LEVELUP_STATS_HEALTH = 'health'
    KEY_LEVELUP_STATS_MANA = 'mana'
    KEY_LEVELUP_STATS_STRENGTH = 'strength'
    KEY_LEVELUP_STATS_ARMOR = 'armor'
    KEY_LEVELUP_STATS_AGILITY = 'agility'

    level_stats = {}
    loaded_stats = session.query(LevelUpStats).all()

    for stat in loaded_stats:
        level = stat.level
        health = parse_int(stat.health)
        mana = parse_int(stat.mana)
        strength = parse_int(stat.strength)
        agility = parse_int(stat.agility)
        armor = parse_int(stat.armor)

        level_stats[level] = {
            KEY_LEVELUP_STATS_HEALTH: health,
            KEY_LEVELUP_STATS_MANA: mana,
            KEY_LEVELUP_STATS_AGILITY: agility,
            KEY_LEVELUP_STATS_STRENGTH: strength,
            KEY_LEVELUP_STATS_ARMOR: armor
        }

    return level_stats
