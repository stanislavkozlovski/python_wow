from sqlalchemy import Column, Integer, String, Text

from buffs import DoT
from damage import Damage

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

    def convert_to_dot_object(self, caster_lvl) -> DoT:
        """
        Convert the Dot schema object to a DoT object
        """
        dot_name: str = self.name
        dot_damage_per_tick: int = self.damage_per_tick
        dot_damage_school: str = self.damage_school
        dot_duration: int = self.duration

        if dot_damage_school == "magic":
            dot_damage: Damage = Damage(magic_dmg=dot_damage_per_tick)
        elif dot_damage_school == "physical":
            dot_damage: Damage = Damage(phys_dmg=dot_damage_per_tick)
        else:
            raise Exception('Unsupported Damage type!')

        return DoT(name=dot_name, damage_tick=dot_damage, duration=dot_duration, caster_lvl=caster_lvl)
