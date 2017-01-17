"""
This module will take care for saving a character to the database
"""
from database.database_info import \
    (DB_PATH,
     DBINDEX_SAVED_CHARACTER_LOADED_SCRIPTS_TABLE_ID, DBINDEX_SAVED_CHARACTER_KILLED_MONSTERS_ID,
     DBINDEX_SAVED_CHARACTER_COMPLETED_QUESTS_ID, DBINDEX_SAVED_CHARACTER_INVENTORY_ID,
     DBINDEX_SAVED_CHARACTER_EQUIPMENT_ID,

     DB_SAVED_CHARACTER_TABLE_NAME,
     DB_SC_LOADED_SCRIPTS_TABLE_NAME, DB_SC_KILLED_MONSTERS_TABLE_NAME, DB_SC_EQUIPMENT_TABLE_NAME,
     DB_SC_COMPLETED_QUESTS_TABLE_NAME, DB_SC_INVENTORY_TABLE_NAME)
from entities import Character
from constants import (CHARACTER_EQUIPMENT_BELT_KEY, CHARACTER_EQUIPMENT_BOOTS_KEY,
                       CHARACTER_EQUIPMENT_CHESTGUARD_KEY, CHARACTER_EQUIPMENT_SHOULDERPAD_KEY,
                       CHARACTER_EQUIPMENT_HEADPIECE_KEY, CHARACTER_EQUIPMENT_NECKLACE_KEY,
                       CHARACTER_EQUIPMENT_BRACER_KEY, CHARACTER_EQUIPMENT_GLOVES_KEY, CHARACTER_EQUIPMENT_LEGGINGS_KEY)
from items import Item
from database.main import session
from models.characters.saved_character import SavedCharacterSchema
from sqlalchemy.sql.functions import coalesce, max as max_table_id
from models.characters.saved_character import CompletedQuestsSchema, SavedCharacterSchema, InventorySchema, LoadedScriptsSchema, KilledMonstersSchema
ALLOWED_TABLES_TO_DELETE_FROM = {'saved_character_completed_quests': CompletedQuestsSchema,
                                 'saved_character_inventory': InventorySchema,
                                 'saved_character_killed_monsters': KilledMonstersSchema,
                                'saved_character_loaded_scripts': LoadedScriptsSchema,
                                 'saved_character': SavedCharacterSchema}

# TODO: Don't save a idx if you don't have anything to save in it!
def save_character(character: Character):
    """
    Save the character into the database
    """
    character_info: SavedCharacterSchema = session.query(SavedCharacterSchema).filter_by(name=character.name).one_or_none()

    character_level: int = character.level  # type: int
    character_class: str = character.get_class()  # type: str
    character_gold: int = character.inventory['gold']  # type: int
    equipment: {str: int} = character.equipment
    headpiece_id: int = get_item_id_or_none(equipment[CHARACTER_EQUIPMENT_HEADPIECE_KEY])
    shoulderpad_id: int = get_item_id_or_none(equipment[CHARACTER_EQUIPMENT_SHOULDERPAD_KEY])
    necklace_id: int = get_item_id_or_none(equipment[CHARACTER_EQUIPMENT_NECKLACE_KEY])
    chestguard_id: int = get_item_id_or_none(equipment[CHARACTER_EQUIPMENT_CHESTGUARD_KEY])
    bracer_id: int = get_item_id_or_none(equipment[CHARACTER_EQUIPMENT_BRACER_KEY])
    gloves_id: int = get_item_id_or_none(equipment[CHARACTER_EQUIPMENT_GLOVES_KEY])
    belt_id: int = get_item_id_or_none(equipment[CHARACTER_EQUIPMENT_BELT_KEY])
    leggings_id: int = get_item_id_or_none(equipment[CHARACTER_EQUIPMENT_LEGGINGS_KEY])
    boots_id: int = get_item_id_or_none(equipment[CHARACTER_EQUIPMENT_BOOTS_KEY])

    # see if the character already has its row (has been saved)
    if character_info:  # we have saved this character before, therefore we have the table IDs
        character_loaded_scripts_id = character_info.loaded_scripts_id
        character_killed_monsters_id = character_info.killed_monsters_id
        character_completed_quests_id = character_info.completed_quests_id
        character_inventory_id = character_info.inventory_id
    else:  # we have not saved this character before, therefore we need to generate new IDs for the other tables
        character_loaded_scripts_id = get_highest_free_id_from_table(DB_SC_LOADED_SCRIPTS_TABLE_NAME)
        character_killed_monsters_id = get_highest_free_id_from_table(DB_SC_KILLED_MONSTERS_TABLE_NAME)
        character_completed_quests_id = get_highest_free_id_from_table(DB_SC_COMPLETED_QUESTS_TABLE_NAME)
        character_inventory_id = get_highest_free_id_from_table(DB_SC_INVENTORY_TABLE_NAME)

    # save the main table
    character_values: {str: int or str} = {
        'name': character.name, 'character_class': character_class, 'level': character_level, 'gold': character_gold,
        'loaded_scripts_id': character_loaded_scripts_id, 'killed_monsters_id': character_killed_monsters_id,
        'completed_quests_id': character_completed_quests_id, 'inventory_id': character_inventory_id,
        'headpiece_id': headpiece_id, 'shoulderpad_id': shoulderpad_id, 'necklace_id': necklace_id,
        'chestguard_id': chestguard_id, 'belt_id': belt_id, 'bracer_id': bracer_id, 'gloves_id': gloves_id,
        'leggings_id': leggings_id, 'boots_id': boots_id}

    # if the character exists, update the row, otherwise create a new one
    if character_info:
        session.query(SavedCharacterSchema).filter_by(name=character.name).update(character_values)
    else:
        session.add(SavedCharacterSchema(**character_values))

    session.commit()
    char_entry = session.query(SavedCharacterSchema).filter_by(name=character.name).first().entry
    # save the sub-tables
    save_loaded_scripts(character_loaded_scripts_id, char_entry, character.loaded_scripts)
    save_killed_monsters(character_killed_monsters_id, char_entry, character.killed_monsters)
    save_completed_quests(character_completed_quests_id, char_entry, character.completed_quests)
    save_inventory(character_inventory_id, char_entry, character.inventory)

    session.commit()
    print("-" * 40)
    print(f'Character {character.name} was saved successfully!')
    print("-" * 40)


def save_loaded_scripts(id: int, char_id: int, loaded_scripts: set):
    """
    This function saves the character's loaded scripts into the saved_character_loaded_scripts DB table
    Table sample contents:
    id,    script_name
      1,     HASKELL_PRAXTON_CONVERSATION

    :param id: the ID we have to save as
    :param loaded_scripts: a set containing all the names -> {HASKEL_PRAXTON_CONVERSATION} in this case
    """

    delete_rows_from_table(table_name=DB_SC_LOADED_SCRIPTS_TABLE_NAME, char_id=char_id)  # delete the old values first

    for loaded_script in loaded_scripts:
        script_to_save = LoadedScriptsSchema()
        script_to_save.saved_character_id = char_id
        script_to_save.script_name = loaded_script

        session.add(script_to_save)


def save_killed_monsters(id: int, char_id: int, killed_monsters: set):
    """
    This function saves all the monsters that the character has killed into the saved_character_killed_monsters DB table
    Table sample contents:
    id,    GUID(of monster)
          1,     14
          1,      7
    IMPORTANT: This works only for monsters that by design should not be killed twice if the player restarts the game

    :param id:  the ID we have to save as
    :param killed_monsters: a set containing all the killed monster's GUIDs -> {14, 3, 2}
    """

    delete_rows_from_table(table_name=DB_SC_KILLED_MONSTERS_TABLE_NAME, char_id=char_id)  # delete the old values first

    for monster_guid in killed_monsters:
        k_monster_to_save = KilledMonstersSchema()
        k_monster_to_save.saved_character_id = char_id
        k_monster_to_save.guid = monster_guid

        session.add(k_monster_to_save)


def save_completed_quests(id: int, char_id: int, completed_quests: set):
    """
    This function saves all the quests that the character has completed into the saved_character_completed_quests DB table
    Table sample contents:
    id,  quest_name
      1,   A Canine Menace
      1,   Canine-Like Hunger

    :param id: the ID we have to save as
    :param completed_quests: a set containing all the names of the completed quests -> {"A Canine Menace", "Canine-Like Hunger"} in this case
    """

    delete_rows_from_table(table_name=DB_SC_COMPLETED_QUESTS_TABLE_NAME, char_id=char_id)  # delete the old values first

    for quest_id in completed_quests:
        c_quest_to_save = CompletedQuestsSchema()
        c_quest_to_save.saved_character_id = char_id
        c_quest_to_save.quest_id = quest_id

        session.add(c_quest_to_save)


def save_inventory(id: int, char_id: int, inventory: dict):
    """
    This function saves the character's inventory into the saved_character_inventory DB table
    Table sample contents:

        id, item_id, item_count
     1,       1,        5
     Meaning the character has 5 Wolf Meats in his inventory

    :param id: the ID we have to save as
    :param inventory: A dictionary, Key: item_name, Value: tuple(Item class instance, Item Count)
    """

    delete_rows_from_table(table_name=DB_SC_INVENTORY_TABLE_NAME, char_id=char_id)  # delete the old values first

    for item_name in inventory.keys():
        if item_name != 'gold':
            item_id = inventory[item_name][0].id  # get the instance of Item's ID
            item_count = inventory[item_name][1]

            inv_to_save = InventorySchema()
            inv_to_save.saved_character_id = char_id
            inv_to_save.item_id = item_id
            inv_to_save.item_count = item_count

            session.add(inv_to_save)


def delete_rows_from_table(table_name: str, char_id: int):
    """
    This function will delete every row in TABLE_NAME with an id of ID
    :param table_name: a string -> "saved_character_loaded_scripts" for example
    :param id:  the id of the rows we want to delete -> 1

    The function is used whenever we want to save new information. To save the new updated information, we have to
    delete the old one first.
    """
    if table_name in ALLOWED_TABLES_TO_DELETE_FROM:
        session.query(ALLOWED_TABLES_TO_DELETE_FROM[table_name]).filter_by(saved_character_id=char_id).delete()
        session.commit()
    else:
        raise Exception(f'You do not have permission to delete from the {table_name} table!')


def get_highest_free_id_from_table(table_name: str):
    """
    This function returns the highest free unique id from a table
    This ID is most likely used to insert a new row into it
    """
    loaded_id = session.query(coalesce(max_table_id(ALLOWED_TABLES_TO_DELETE_FROM[table_name].id), 0).label('max_id')).one()
    max_id = loaded_id.max_id

    return max_id + 1


def get_item_id_or_none(item):
    """
    This function returns the item_id of an item.
    We check if the item we're given is None. If it is None, we return None
    """
    if isinstance(item, Item):
        return item.id

    return None



