from sqlalchemy import Column, Integer, String, Text

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

    name = Column(String(60), primary_key=True)
    character_class = Column('class', String(60))
    level = Column(Integer)
    loaded_scripts_id = Column(Integer)
    killed_monsters_id = Column(Integer)
    completed_quests_id = Column(Integer)
    equipment_id = Column(Integer)
    inventory_id = Column(Integer)
    gold = Column(Integer)


class CompletedQuests(Base):
    """
    This table holds information about the completed quests for a specific character
        id - id of the row (NOT unique)
        quest_name - the name of the quest that is completed
    Ex:
    id, quest_name
     1,   Kill Wolves
     1,   Kill Bears
    Meaning that the character whose completed_quests_id points to 1 has completed both quests - Kill Wolves and Kill Bears
    """
    # TODO: Holds more completed quests per row to minimize queries
    __tablename__ = 'saved_character_completed_quests'

    id = Column(Integer, primary_key=True)
    quest_name = Column(String)


class Equipment(Base):
    """
    This table holds information about the equipment of a specific character
        id - the id of the row entry
        XXX_id - the ID of the item in the item_template
    """
    __tablename__ = 'saved_character_equipment'

    id = Column(Integer, primary_key=True)
    headpiece_id = Column(Integer)
    shoulderpad_id = Column(Integer)
    necklace_id = Column(Integer)
    chestguard_id = Column(Integer)
    bracer_id = Column(Integer)
    gloves_id = Column(Integer)
    belt_id = Column(Integer)
    leggings_id = Column(Integer)
    boots_id = Column(Integer)


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
    item_id = Column(Integer)
    item_count = Column(Integer)


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
    guid = Column(Integer)


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
    script_name = Column(Text)