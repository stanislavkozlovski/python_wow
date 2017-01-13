from sqlalchemy import Column, Integer, String, Text

from database.main import Base


class PaladinSpells(Base):
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
    effect - the ID of the effect given by the spell, depending on the spell specifically. (Only Melting Strike has one for now and it serves as the entry in spell_dots)
    cooldown - the amount of turns it takes for the spell to be ready again after being cast
    comment - just a comment on the spell
    paladin_spells_template table is as follows:
            ID, Name of Spell, Rank of Spell, Level Required for said Rank, Damage1, Damage2, Damage3, Heal1, Heal2, Heal3, Effect, mana_cost, Cooldown, Comment
            1,Seal of Righteousness,       1,                            1,       2,       0,       0,     0,     0,     0,      0,        10,        0,Seal of Righteousness
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
    effect = Column(Integer)
    cooldown = Column(Integer)
    comment = Column(Text)
