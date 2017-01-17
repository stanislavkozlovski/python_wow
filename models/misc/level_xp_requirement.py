from sqlalchemy import Column, Integer

from database.main import Base


class LevelXpRequirementSchema(Base):
    """
    This table holds information about the necessary XP needed to reach a certain level.
    The table's contents are as follows:
    level, xp_required(needed to reach the next one)
    1,     400 (meaning you need to have 400XP to reach level 2)
    2,     800 (800XP needed to reach level 3)
    """
    __tablename__ = 'level_xp_requirement'

    level = Column(Integer, primary_key=True)
    xp_required = Column(Integer)
