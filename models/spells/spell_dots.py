from sqlalchemy import Column, Integer, String, Text

from database.main import Base


class Dot(Base):
    """
    Represents a DoT(Damage over Time effect) from the spell_dots table, whose contents are the following:
        entry - ID of the dot
        name - name of the DOT
        damage_per_tick - the damage this DOT deals every turn
        damage_school - the school of the damage (currently supported - magic and physical)
        duration - the amount of turns this DOT lasts for
        comment - A comment for the DOT
    entry,      name,    damage_per_tick, damage_school, duration, comment
        1,   Melting,                 2,          magic,        2,  For the Paladin spell Melting Strike
    This DoT deals 2 magic damage each turn and lasts for two turns.
    """
    __tablename__ = 'spell_dots'

    entry = Column(Integer, primary_key=True)
    name = Column(String(60))
    damage_per_tick = Column(Integer)
    damage_school = Column(String(60))
    duration = Column(Integer)
    comment = Column(Text)
