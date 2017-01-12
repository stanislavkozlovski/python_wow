from sqlalchemy import Column, Integer, String, Text, Boolean

from database.main import Base


class CreatureDefaults(Base):
    """
    This table holds the default values that a creature should have/give at a certain level.
    The table's contents are as follows:
    creature_level - the level of the creature which should have these attributes
    armor - the default amount of armor points a creature of this level should have
    min_gold_reward - the minimum amount of gold a creature of this level should give
    max_gold_reward - the maximum amount of gold a creature of this level should give
    xp_reward - the default amount of experience points a creature of this level should give

    Example:
        creature_level, armor, min_gold_reward, max_gold_reward, xp_reward
                    1,     50,              2,                5,        50
                    2,     65,              4,                6,        75
                    etc...
        A creature of level 1 would drop between 2-5 gold and reward 50 XP on death
    """
    __tablename__ = 'creature_defaults'

    creature_level = Column(Integer, primary_key=True)
    armor = Column(Integer)
    min_gold_reward = Column(Integer)
    max_gold_reward = Column(Integer)
    xp_reward = Column(Integer)