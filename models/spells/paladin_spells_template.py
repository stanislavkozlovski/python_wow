from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from utils.helper import parse_int
from spells import PaladinSpell
from database.main import Base


class PaladinSpellsSchema(Base):
    """
    A table that holds spells specifically for the Paladin class
    id - id of the spell
    name - name of the spell
    rank - the rank (or level) of the spell. Higher ranks required a higher level and deal more damage etc.
    level - the required level for the given rank of the spell
    damage1 - the primary damage of the spell (if applicable)
    damage2, damage3 - secondary damage of the spell (if applicable)
    heal1 - primary heal points given by the spell (if applicable)
    heal2, heal3 - secondary heal points given by the spell (if applicable)
    mana_cost - the mana points this spell costs to cast
    beneficial_effect - the ID of the beneficial effect given by the spell, in the DB table spell_buffs
    harmful_effect - the ID of the harmful effect given by the spell, in the DB table spell_dots
    cooldown - the amount of turns it takes for the spell to be ready again after being cast
    comment - just a comment on the spell
    paladin_spells_template table is as follows:
            ID, Name of Spell, Rank of Spell, Level Required for said Rank, Damage1, Damage2, Damage3, Heal1, Heal2, Heal3, beneficial_effect, harmful_effect, mana_cost, Cooldown, Comment
            1,Seal of Righteousness,       1,                            1,       2,       0,       0,     0,     0,     0,                 0,              0,       10,         0,  Seal of Righteousness
            :return: A dictionary holding keys for each row (rank, damage1, damage2 etc.)
    """
    __tablename__ = 'paladin_spells_template'

    id = Column(Integer, primary_key=True)
    name = Column(String(60))
    rank = Column(Integer)
    level_required = Column(Integer)
    damage1 = Column(Integer)
    damage2 = Column(Integer)
    damage3 = Column(Integer)
    heal1 = Column(Integer)
    heal2 = Column(Integer)
    heal3 = Column(Integer)
    mana_cost = Column(Integer)
    beneficial_effect = Column(Integer, ForeignKey('spell_buffs.entry'))
    harmful_effect = Column(Integer, ForeignKey('spell_dots.entry'))
    cooldown = Column(Integer)
    comment = Column(Text)

    buff = relationship('BuffSchema')
    dot = relationship('DotSchema')

    def convert_to_paladin_spell_object(self) -> PaladinSpell:
        """
        Converts the PaladinSpells schema object to a Paladin Spell object
        """
        level: int = parse_int(self.level_required)
        damage1: int = parse_int(self.damage1)
        damage2: int = parse_int(self.damage2)
        damage3: int = parse_int(self.damage3)
        mana_cost: int = parse_int(self.mana_cost)
        heal1: int = parse_int(self.heal1)
        heal2: int = parse_int(self.heal2)
        heal3: int = parse_int(self.heal3)
        cooldown: int = parse_int(self.cooldown)
        buff: 'BeneficialBuff' = self.buff.convert_to_beneficial_buff_object() if self.buff else None
        harmful_effect: 'DoT' = self.dot.convert_to_dot_object(level) if self.dot else None

        return PaladinSpell(name=self.name, rank=self.rank, cooldown=cooldown, beneficial_effect=buff,
                            harmful_effect=harmful_effect, damage1=damage1, damage2=damage2, damage3=damage3,
                            heal1=heal1, heal2=heal2, heal3=heal3, mana_cost=mana_cost)
