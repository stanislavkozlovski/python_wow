from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from models.items.item_template import ItemTemplate
from database.main import Base


class SavedCharacter(Base):
    """
    This table holds information about saved player characters
        name - the name of the character
        character_class - the class of the character
        level - the level of the character
        XXX_id - the ID to the row in the saved_character_XXX table associated with this saved character
        gold - the amount of gold the character has
    """
    __tablename__ = 'saved_character'

    entry = Column(Integer, primary_key=True)
    name = Column(String(60))
    character_class = Column('class', String(60))
    level = Column(Integer)
    loaded_scripts_id = Column(Integer, ForeignKey('saved_character_loaded_scripts.saved_character_id'))
    killed_monsters_id = Column(Integer, ForeignKey('saved_character_killed_monsters.saved_character_id'))
    completed_quests_id = Column(Integer, ForeignKey('saved_character_completed_quests.saved_character_id'))
    inventory_id = Column(Integer, ForeignKey('saved_character_inventory.saved_character_id'))
    gold = Column(Integer)

    loaded_scripts = relationship('LoadedScripts', foreign_keys=[loaded_scripts_id], uselist=True)
    killed_monsters = relationship('KilledMonsters', foreign_keys=[killed_monsters_id], uselist=True)
    inventory = relationship('Inventory', foreign_keys=[inventory_id], uselist=True)
    completed_quests = relationship('CompletedQuests', foreign_keys=[completed_quests_id], uselist=True)

    headpiece_id = Column(Integer, ForeignKey('item_template.entry'))
    shoulderpad_id = Column(Integer, ForeignKey('item_template.entry'))
    necklace_id = Column(Integer, ForeignKey('item_template.entry'))
    chestguard_id = Column(Integer, ForeignKey('item_template.entry'))
    bracer_id = Column(Integer, ForeignKey('item_template.entry'))
    gloves_id = Column(Integer, ForeignKey('item_template.entry'))
    belt_id = Column(Integer, ForeignKey('item_template.entry'))
    leggings_id = Column(Integer, ForeignKey('item_template.entry'))
    boots_id = Column(Integer, ForeignKey('item_template.entry'))

    headpiece: ItemTemplate or None = relationship('ItemTemplate', foreign_keys=[headpiece_id])
    shoulderpad: ItemTemplate or None = relationship('ItemTemplate', foreign_keys=[shoulderpad_id])
    necklace: ItemTemplate or None = relationship('ItemTemplate', foreign_keys=[necklace_id])
    chestguard: ItemTemplate or None = relationship('ItemTemplate', foreign_keys=[chestguard_id])
    bracer: ItemTemplate or None = relationship('ItemTemplate', foreign_keys=[bracer_id])
    gloves: ItemTemplate or None = relationship('ItemTemplate', foreign_keys=[gloves_id])
    belt: ItemTemplate or None = relationship('ItemTemplate', foreign_keys=[belt_id])
    leggings: ItemTemplate or None = relationship('ItemTemplate', foreign_keys=[leggings_id])
    boots: ItemTemplate or None = relationship('ItemTemplate', foreign_keys=[boots_id])

    def build_equipment(self) -> {str: 'Item' or None}:
        """
        Create a dictionary holding the character's equipment as the Character class holds it
        :return:
        """
        from entities import (CHARACTER_EQUIPMENT_BOOTS_KEY, CHARACTER_EQUIPMENT_LEGGINGS_KEY,
                              CHARACTER_EQUIPMENT_BELT_KEY, CHARACTER_EQUIPMENT_GLOVES_KEY,
                              CHARACTER_EQUIPMENT_BRACER_KEY,
                              CHARACTER_EQUIPMENT_CHESTGUARD_KEY, CHARACTER_EQUIPMENT_HEADPIECE_KEY,
                              CHARACTER_EQUIPMENT_NECKLACE_KEY,
                              CHARACTER_EQUIPMENT_SHOULDERPAD_KEY)

        saved_equipment = {CHARACTER_EQUIPMENT_BOOTS_KEY: self.boots,
                           CHARACTER_EQUIPMENT_LEGGINGS_KEY: self.leggings,
                           CHARACTER_EQUIPMENT_BELT_KEY: self.belt,
                           CHARACTER_EQUIPMENT_GLOVES_KEY: self.gloves,
                           CHARACTER_EQUIPMENT_BRACER_KEY: self.bracer,
                           CHARACTER_EQUIPMENT_CHESTGUARD_KEY: self.chestguard,
                           CHARACTER_EQUIPMENT_SHOULDERPAD_KEY: self.shoulderpad,
                           CHARACTER_EQUIPMENT_NECKLACE_KEY: self.necklace,
                           CHARACTER_EQUIPMENT_HEADPIECE_KEY: self.headpiece}

        # convert the each equipment ItemTemplate to an Item object
        for slot, item in saved_equipment.items():
            if item is not None:
                saved_equipment[slot] = item.convert_to_item_object()

        return saved_equipment


class CompletedQuests(Base):
    """
    This table holds information about the completed quests for a specific character
        id - id of the row (NOT unique)
        quest_id - the id of the quest that is completed
    Ex:
    id, quest_id
     1,   1
     1,   2
    Meaning that the character whose completed_quests_id points to 1 has completed both quests - (1)Kill Wolves and (2)Kill Bears
    """
    # TODO: Holds more completed quests per row to minimize queries
    __tablename__ = 'saved_character_completed_quests'

    id = Column(Integer, primary_key=True)
    saved_character_id = Column(Integer, ForeignKey('saved_character.entry'))
    quest_id = Column(String, ForeignKey('quest_template.entry'))

    quest = relationship('Quest')


class Inventory(Base):
    """
    This table holds information about the inventory of a specific character
        id - id of the entry (NOT unique)
        item_id - the ID of the item in item_template
        item_count - the count of the item
    Example:
        id, item_id, item_count
         1,       1,         5
         1,       2,         1
    Meaning the character whose inventory_id points to 1 has
        - 5 items of id 1
        - 1 item of id 2
    """
    # TODO: Holds more items in the row to minimize queries
    __tablename__ = 'saved_character_inventory'

    id = Column(Integer, primary_key=True)
    saved_character_id = Column(Integer, ForeignKey('saved_character.entry'))
    item_id = Column(Integer, ForeignKey('item_template.entry'), primary_key=True)
    item_count = Column(Integer)

    item = relationship('ItemTemplate')


class KilledMonsters(Base):
    """
    This table holds information about all the monsters that the character has killed into the saved_character_killed_monsters DB table
        id - id of the entry (NOT unique)
        GUID - GUID of the monster in the creatures DB table
    Table sample contents:
         id,    GUID(of monster)
          1,     14
          1,      7
    IMPORTANT: This works only for monsters that by design should not be killed twice if the player restarts the game
    """
    # TODO: Hold more killed monsters per row to minimize queries
    __tablename__ = 'saved_character_killed_monsters'

    id = Column(Integer, primary_key=True)
    saved_character_id = Column(Integer, ForeignKey('saved_character.entry'))
    guid = Column(Integer, ForeignKey('creatures.guid'))

    monster = relationship('Creatures')


class LoadedScripts(Base):
    """
    This table holds the character's loaded scripts into the saved_character_loaded_scripts DB table
        id - id of the entry (NOT unique)
        script_name - the name of the script
    Table sample contents:
    id,    script_name
      1,     HASKELL_PRAXTON_CONVERSATION
      1,     Something_Something_Something
    Meaning the character whose loaded_scripts_id has seen both scripts and should not see them again in the game.
    """
    # TODO: Hold more scripts per row to minimize queries
    __tablename__ = 'saved_character_loaded_scripts'

    id = Column(Integer, primary_key=True)
    saved_character_id = Column(Integer, ForeignKey('saved_character.entry'))
    script_name = Column(Text)
