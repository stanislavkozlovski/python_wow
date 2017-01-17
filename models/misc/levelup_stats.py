from sqlalchemy import Column, Integer

from database.main import Base


class LevelUpStatsSchema(Base):
    """
    This table holds information about the amount of stats a character should gain according to the level he has attained
    Example:
        level, health, mana, strength, agility, armor
            4,     10,   10,        7,       4,    15
    A character who has just became level 4 will add 10hp, 10mana, 7strength, 4agiltiy and 15 armor to his stats
        from the level up
    """
    __tablename__ = 'levelup_stats'

    level = Column(Integer, primary_key=True)
    health = Column(Integer)
    mana = Column(Integer)
    strength = Column(Integer)
    agility = Column(Integer)
    armor = Column(Integer)
