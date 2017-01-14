from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from utils.helper import parse_int
from entities import FriendlyNPC, VendorNPC
from database.main import Base


class Creatures(Base):
    # TODO: Remove the Type column from this table
    """
    This table holds information about SPECIFIC monsters in the game
    guid - the unique ID of the specific creature
    creature_id - the ID of the creature in the creature_template table where his general info is stored
    type - the type of creature. Currently supported:
        monster - hostile creature
        fnpc - friendly npc
        vendor - vendor npc
    zone - the zone this specific creature spawns in
    sub_zone - the subzone this specific creature spawns in

     guid, creature_id,       type,             zone,          subzone
           1,          11,  'monster',    Elwynn Forest, Northshire Abbey
    """
    __tablename__ = 'creatures'

    guid = Column(Integer, primary_key=True)
    creature_id = Column(Integer, ForeignKey('creature_template.entry'))
    creature = relationship('CreatureTemplate')
    type = Column(String(60))
    zone = Column(String(60))
    sub_zone = Column(String(60))

    def convert_to_living_thing_object(self) -> 'LivingThing':
        """ Converts the Creature to whatever object he is according to his type column """
        entry: int = self.creature_id
        name: str = self.creature.name
        type_: str = self.creature.type
        level: int = parse_int(self.creature.level)
        health: int = parse_int(self.creature.health)
        mana: int = parse_int(self.creature.mana)
        min_dmg: int = parse_int(self.creature.min_dmg)
        max_dmg: int = parse_int(self.creature.max_dmg)
        quest_relation_id: int = parse_int(self.creature.quest_relation_id)
        loot_table_id: int = parse_int(self.creature.loot_table_id)
        gossip: str = self.creature.gossip

        if type_ == "fnpc":
            return FriendlyNPC(name=name, health=health,
                               mana=mana, level=level,
                               min_damage=min_dmg,
                               max_damage=max_dmg,
                               quest_relation_id=quest_relation_id,
                               loot_table_ID=loot_table_id,
                               gossip=gossip)

        elif type_ == "vendor":
            return VendorNPC(name=name, entry=entry,
                             health=health, mana=mana, level=level,
                             min_damage=min_dmg,
                             max_damage=max_dmg,
                             quest_relation_id=quest_relation_id,
                             loot_table_ID=loot_table_id,
                             gossip=gossip)
        else:
            raise NotImplementedError()
