from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

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
