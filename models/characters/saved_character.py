from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from models.items.item_template import ItemTemplateSchema
from entities import Character
from constants import (CHARACTER_EQUIPMENT_BOOTS_KEY, CHARACTER_EQUIPMENT_LEGGINGS_KEY,
                       CHARACTER_EQUIPMENT_BELT_KEY, CHARACTER_EQUIPMENT_GLOVES_KEY,
                       CHARACTER_EQUIPMENT_BRACER_KEY,
                       CHARACTER_EQUIPMENT_CHESTGUARD_KEY, CHARACTER_EQUIPMENT_HEADPIECE_KEY,
                       CHARACTER_EQUIPMENT_NECKLACE_KEY,
                       CHARACTER_EQUIPMENT_SHOULDERPAD_KEY)
from classes import Paladin
from database.main import Base


class SavedCharacterSchema(Base):
    """
    This table holds information about saved player characters
        name - the name of the character
        character_class - the class of the character
        level - the level of the character
        gold - the amount of gold the character has
    """
    __tablename__ = 'saved_character'

    entry = Column(Integer, primary_key=True)
    name = Column(String(60))
    character_class = Column('class', String(60))
    level = Column(Integer)
    gold = Column(Integer)

    headpiece_id = Column(Integer, ForeignKey('item_template.entry'))
    shoulderpad_id = Column(Integer, ForeignKey('item_template.entry'))
    necklace_id = Column(Integer, ForeignKey('item_template.entry'))
    chestguard_id = Column(Integer, ForeignKey('item_template.entry'))
    bracer_id = Column(Integer, ForeignKey('item_template.entry'))
    gloves_id = Column(Integer, ForeignKey('item_template.entry'))
    belt_id = Column(Integer, ForeignKey('item_template.entry'))
    leggings_id = Column(Integer, ForeignKey('item_template.entry'))
    boots_id = Column(Integer, ForeignKey('item_template.entry'))

    headpiece: ItemTemplateSchema or None = relationship('ItemTemplateSchema', foreign_keys=[headpiece_id])
    shoulderpad: ItemTemplateSchema or None = relationship('ItemTemplateSchema', foreign_keys=[shoulderpad_id])
    necklace: ItemTemplateSchema or None = relationship('ItemTemplateSchema', foreign_keys=[necklace_id])
    chestguard: ItemTemplateSchema or None = relationship('ItemTemplateSchema', foreign_keys=[chestguard_id])
    bracer: ItemTemplateSchema or None = relationship('ItemTemplateSchema', foreign_keys=[bracer_id])
    gloves: ItemTemplateSchema or None = relationship('ItemTemplateSchema', foreign_keys=[gloves_id])
    belt: ItemTemplateSchema or None = relationship('ItemTemplateSchema', foreign_keys=[belt_id])
    leggings: ItemTemplateSchema or None = relationship('ItemTemplateSchema', foreign_keys=[leggings_id])
    boots: ItemTemplateSchema or None = relationship('ItemTemplateSchema', foreign_keys=[boots_id])

    def __init__(self, name: str, character_class: str, level: int, gold: int, headpiece_id: int,
                 shoulderpad_id: int, necklace_id: int, chestguard_id: int, bracer_id: int, gloves_id: int,
                 belt_id: int, leggings_id: int, boots_id: int):
        # A init function for easily creating an object when wanting to insert a new row in the table
        super().__init__()
        self.name = name
        self.character_class = character_class
        self.level = level
        self.gold = gold
        self.headpiece_id = headpiece_id
        self.shoulderpad_id = shoulderpad_id
        self.necklace_id = necklace_id
        self.chestguard_id = chestguard_id
        self.bracer_id = bracer_id
        self.gloves_id = gloves_id
        self.belt_id = belt_id
        self.leggings_id = leggings_id
        self.boots_id = boots_id

    def build_equipment(self) -> {str: 'Item' or None}:
        """
        Create a dictionary holding the character's equipment as the Character class holds it
        :return:
        """
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

    def convert_to_character_object(self) -> Character:
        """ Convert the SavedCharacter object to a Character object to be used in the game"""
        loaded_scripts: {str} = {script.script_name for script in self.loaded_scripts}
        killed_monsters: {int} = {monster.guid for monster in self.killed_monsters}
        completed_quests: {str} = {quest.quest_id for quest in self.completed_quests}
        inventory: {str: tuple} = {i_schema.item.name: (i_schema.item.convert_to_item_object(), i_schema.item_count)
                                   for i_schema in self.inventory}
        inventory['gold'] = self.gold
        equipment = self.build_equipment()
        print(equipment)

        if self.character_class == 'paladin':
            return Paladin(name=self.name,
                           level=self.level,
                           loaded_scripts=loaded_scripts,
                           killed_monsters=killed_monsters,
                           completed_quests=completed_quests,
                           saved_inventory=inventory,
                           saved_equipment=equipment)
        else:
            raise Exception(f'Unsupported class - {self.character_class}')


class CompletedQuestsSchema(Base):
    """
    This table holds information about the completed quests for a specific character
        saved_character_id - id of the character (NOT unique)
        quest_id - the id of the quest that is completed
    Ex:
    saved_character_id, quest_id
                    1,   1
                    1,   2
    Meaning that the character whose completed_quests_id points to 1 has completed both quests - (1)Kill Wolves and (2)Kill Bears
    """
    # TODO: Holds more completed quests per row to minimize queries
    __tablename__ = 'saved_character_completed_quests'

    id = Column(Integer, primary_key=True)
    saved_character_id = Column(Integer, ForeignKey('saved_character.entry'))
    quest_id = Column(String, ForeignKey('quest_template.entry'))

    _ = relationship('SavedCharacterSchema', foreign_keys=[saved_character_id], backref='completed_quests')
    quest = relationship('QuestSchema')


class InventorySchema(Base):
    """
    This table holds information about the inventory of a specific character
        saved_character_id - id of the character (NOT unique)
        item_id - the ID of the item in item_template
        item_count - the count of the item
    Example:
        saved_character_id, item_id, item_count
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

    _ = relationship('SavedCharacterSchema', foreign_keys=[saved_character_id], backref='inventory')
    item = relationship('ItemTemplateSchema')


class KilledMonstersSchema(Base):
    """
    This table holds information about all the monsters that the character has killed into the saved_character_killed_monsters DB table
        saved_character_id - id of the character (NOT unique)
        GUID - GUID of the monster in the creatures DB table
    Table sample contents:
         saved_character_id,    GUID(of monster)
                          1,     14
                          1,      7
    IMPORTANT: This works only for monsters that by design should not be killed twice if the player restarts the game
    """
    # TODO: Hold more killed monsters per row to minimize queries
    __tablename__ = 'saved_character_killed_monsters'

    id = Column(Integer, primary_key=True)
    saved_character_id = Column(Integer, ForeignKey('saved_character.entry'))
    guid = Column(Integer, ForeignKey('creatures.guid'))

    _ = relationship('SavedCharacterSchema', foreign_keys=[saved_character_id], backref='killed_monsters')
    monster = relationship('CreaturesSchema')


class LoadedScriptsSchema(Base):
    """
    This table holds the character's loaded scripts into the saved_character_loaded_scripts DB table
        saved_character_id - id of the character (NOT unique)
        script_name - the name of the script
    Table sample contents:
    saved_character_id,    script_name
                     1,     HASKELL_PRAXTON_CONVERSATION
                     1,     Something_Something_Something
    Meaning the character whose loaded_scripts_id has seen both scripts and should not see them again in the game.
    """
    # TODO: Hold more scripts per row to minimize queries
    __tablename__ = 'saved_character_loaded_scripts'

    id = Column(Integer, primary_key=True)
    saved_character_id = Column(Integer, ForeignKey('saved_character.entry'))

    _ = relationship('SavedCharacterSchema', foreign_keys=[saved_character_id], backref='loaded_scripts')
    script_name = Column(Text)
