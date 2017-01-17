from decorators import run_once
from models.creatures.creature_defaults.creature_defaults import CreatureDefaultsSchema
from database.main import session


@run_once
def load_creature_defaults() -> {int: {str: int}}:
    """
    Load the default values that a creature should have/give at a certain level.

    :return: A dictionary as follows: Key: Level(ex: 1), Value: Dictionary{'armor': 50,
                                                                    'min_gold_reward': 2,
                                                                    'max_gold_reward': 5,
                                                                    'xp_reward': 50}
        """
    creature_defaults = {}

    loaded_creature_defaults: [CreatureDefaultsSchema] = session.query(CreatureDefaultsSchema).all()
    for creature_default in loaded_creature_defaults:
        creature_defaults[creature_default.creature_level] = {'armor': creature_default.armor,
                                                              'min_gold_reward': creature_default.min_gold_reward,
                                                              'max_gold_reward': creature_default.max_gold_reward,
                                                              'xp_reward': creature_default.xp_reward}

    return creature_defaults
