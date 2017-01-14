from sqlalchemy import Column, Integer, String, Text

from database.main import Base


class Buff(Base):
    """
    A buff from the DB table spells_buffs, whose contents are the following:

    entry,             name, duration,    stat,   amount,   stat2,   amount2,stat3,   amount3, comment
        1,  Heart of a Lion,        5,strength,       10,                                      Increases strength by 10 for 5 turns

        stat - the stat this buff increases
        amount - the amount it increases the stat by
        duration - the amount of turns this buff lasts for
    This buff increases your strength by 10 for 5 turns.

    Load the information about the buff, convert it to an class Buff object and return it
    """
    __tablename__ = 'spell_buffs'

    entry = Column(Integer, primary_key=True)
    name = Column(String(60))
    duration = Column(Integer)
    stat1 = Column(String(60))
    amount1 = Column(Integer)
    stat2 = Column(String(60), nullable=True)
    amount2 = Column(Integer, nullable=True)
    stat3 = Column(String(60), nullable=True)
    amount3 = Column(Integer, nullable=True)
    comment = Column(Text)