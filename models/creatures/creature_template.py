from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from database.main import Base


class CreatureTemplate(Base):
    """
    This table holds the information about each creature in the game
    entry - the unique ID of this creature
    creature_name - the name of this creature
    type - the type of creature. Currently supported:
        monster - hostile creature
        fnpc - friendly npc
        vendor - vendor npc
    level - the level of this creature
    hp - the health points of this creature
    mana - the mana points of this creature
    armor - the armor points of this creature NOTE: If not specified, the creature will take the default armor for
        his level from the creature_defaults table
    min_dmg - the minimum damage this creature does per swing
    max_dmg - the maximum damage this creature does per swing
    quest_relation_id - the id of the quest this creature is related with (if applicable)
    loot_table_id - the id of the loot this creature drops (in the loot_table table)
    gossip - the text this creature says when he is talked to (if applicable)
    respawnable - whether this creature will respawn on different game starts. Ex: Some special creatures should not be
        killed more than once

    Example:
     entry, creature name,      type,   level, hp, mana, armor, min_dmg, max_dmg, quest_relation_ID, loot_table,ID,      gossip,   respawnable
         1,       Zimbab,   "monster"       1, 10,   10,   50,       2,       4                  1,              1, "Hey there",      False

        type is "monster" meaning this is a hostile NPC
        Creature Level: 1 Zimbab, HP: 10, MANA: 10, Damage: 2-4.
        He is needed to complete quest with ID 1 and the loot he drops is from the row in the loot_table DB table with
        entry 1. If talking to him is enabled, he would say "Hey there".
    """
    __tablename__ = 'creature_template'

    entry = Column(Integer, primary_key=True)
    name = Column(String(60))
    type = Column(String(60))
    level = Column(Integer)
    health = Column(Integer)
    mana = Column(Integer)
    armor = Column(Integer)
    min_dmg = Column(Integer)
    max_dmg = Column(Integer)
    quest_relation_id = Column(Integer, ForeignKey('quest_template.entry'))
    loot_table_id = Column(Integer, ForeignKey('loot_table.entry'))
    loot_table =  relationship('LootTable', foreign_keys=[loot_table_id])
    gossip = Column(Text)
    respawnable = Column(Boolean)
