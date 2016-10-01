"""
This module will take care for saving a character to the database
"""
import sqlite3

from entities import Character
from database_info import \
    (DB_PATH,
     DBINDEX_SAVED_CHARACTER_LOADED_SCRIPTS_TABLE_ID, DBINDEX_SAVED_CHARACTER_KILLED_MONSTERS_ID,
     DBINDEX_SAVED_CHARACTER_COMPLETED_QUESTS_ID, DBINDEX_SAVED_CHARACTER_INVENTORY_ID,

     DB_SAVED_CHARACTER_TABLE_NAME,
     DB_LOADED_SCRIPTS_TABLE_NAME, DB_KILLED_MONSTERS_TABLE_NAME,
     DB_COMPLETED_QUESTS_TABLE_NAME, DB_INVENTORY_TABLE_NAME)


ALLOWED_TABLES_TO_DELETE_FROM = ['saved_character_completed_quests', 'saved_character_inventory',
                                 'saved_character_killed_monsters', 'saved_character_loaded_scripts',
                                 'saved_character']


def save_character(character: Character):
    """
    Save the character into the database
    """

    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()

        character_info = cursor.execute("SELECT * FROM saved_character WHERE name = ?", [character.name]).fetchone()

        character_level = character.level  # type: int
        character_class = character.get_class()  # type: str
        character_gold = character.inventory['gold']  # type: int

        # see if the character already has it's row (has been saved)
        if character_info:
            # we have saved this character before, therefore we have the table IDs
            character_loaded_scripts_ID = character_info[DBINDEX_SAVED_CHARACTER_LOADED_SCRIPTS_TABLE_ID]
            character_killed_monsters_ID = character_info[DBINDEX_SAVED_CHARACTER_KILLED_MONSTERS_ID]
            character_completed_quests_ID = character_info[DBINDEX_SAVED_CHARACTER_COMPLETED_QUESTS_ID]
            character_inventory_ID = character_info[DBINDEX_SAVED_CHARACTER_INVENTORY_ID]
            cursor.execute("DELETE FROM {table_name} WHERE name = ?"  # delete the old table
                           .format(table_name=DB_SAVED_CHARACTER_TABLE_NAME), [character.name])
        else:
            # we have not saved this character before, therefore we need to generate new IDs for the other tables
            character_loaded_scripts_ID = get_highest_free_id_from_table(DB_LOADED_SCRIPTS_TABLE_NAME, cursor)
            character_killed_monsters_ID = get_highest_free_id_from_table(DB_KILLED_MONSTERS_TABLE_NAME, cursor)
            character_completed_quests_ID = get_highest_free_id_from_table(DB_COMPLETED_QUESTS_TABLE_NAME, cursor)
            character_inventory_ID = get_highest_free_id_from_table(DB_INVENTORY_TABLE_NAME, cursor)

        # save the main table
        cursor.execute("INSERT INTO saved_character VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                       [character.name, character_class, character_level, character_loaded_scripts_ID,
                        character_killed_monsters_ID, character_completed_quests_ID, character_inventory_ID,
                        character_gold])

        # save the sub-tables
        save_loaded_scripts(character_loaded_scripts_ID, character.loaded_scripts, cursor)
        save_killed_monsters(character_killed_monsters_ID, character.killed_monsters, cursor)
        save_completed_quests(character_completed_quests_ID, character.completed_quests, cursor)
        save_inventory(character_inventory_ID, character.inventory, cursor)

        print("-" * 40)
        print("Character {} was saved successfully!".format(character.name))
        print("-" * 40)


def save_loaded_scripts(id: int, loaded_scripts: set, cursor):
    """
    This function saves the character's loaded scripts into the saved_character_loaded_scripts DB table
    Table sample contents:
    id,    script_name
      1,     HASKELL_PRAXTON_CONVERSATION

    :param id: the ID we have to save as
    :param loaded_scripts: a set containing all the names -> {HASKEL_PRAXTON_CONVERSATION} in this case
    """

    delete_rows_from_table(table_name=DB_LOADED_SCRIPTS_TABLE_NAME, id=id, cursor=cursor)  # delete the old values first

    for loaded_script in loaded_scripts:
        cursor.execute('INSERT INTO {} VALUES (?, ?)'.format(DB_LOADED_SCRIPTS_TABLE_NAME), [id, loaded_script])


def save_killed_monsters(id: int, killed_monsters: set, cursor):
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

    delete_rows_from_table(table_name=DB_KILLED_MONSTERS_TABLE_NAME, id=id, cursor=cursor)  # delete the old values first

    for monster_guid in killed_monsters:
        cursor.execute('INSERT INTO {} VALUES (?, ?)'.format(DB_KILLED_MONSTERS_TABLE_NAME), [id, monster_guid])


def save_completed_quests(id: int, completed_quests: set, cursor):
    """
    This function saves all the quests that the character has completed into the saved_character_completed_quests DB table
    Table sample contents:
    id,  quest_name
      1,   A Canine Menace
      1,   Canine-Like Hunger

    :param id: the ID we have to save as
    :param completed_quests: a set containing all the names of the completed quests -> {"A Canine Menace", "Canine-Like Hunger"} in this case
    """

    delete_rows_from_table(table_name=DB_COMPLETED_QUESTS_TABLE_NAME, id=id, cursor=cursor)  # delete the old values first

    for quest_name in completed_quests:
        cursor.execute('INSERT INTO {} VALUES (?, ?)'.format(DB_COMPLETED_QUESTS_TABLE_NAME), [id, quest_name])


def save_inventory(id: int, inventory: dict, cursor):
    """
    This function saves the character's inventory into the saved_character_inventory DB table
    Table sample contents:

        id, item_id, item_count
     1,       1,        5
     Meaning the character has 5 Wolf Meats in his inventory

    :param id: the ID we have to save as
    :param inventory: A dictionary, Key: item_name, Value: tuple(Item class instance, Item Count)
    """

    delete_rows_from_table(table_name=DB_INVENTORY_TABLE_NAME, id=id, cursor=cursor)  # delete the old values first

    for item_name in inventory.keys():
        if item_name != 'gold':
            item_id = inventory[item_name][0].id  # get the instance of Item's ID
            item_count = inventory[item_name][1]

            cursor.execute('INSERT INTO {} VALUES (?, ?, ?)'.format(DB_INVENTORY_TABLE_NAME), [id, item_id, item_count])


def delete_rows_from_table(table_name: str, id: int, cursor):
    """
    This function will delete every row in TABLE_NAME with an id of ID
    :param table_name: a string -> "saved_character_loaded_scripts" for example
    :param id:  the id of the rows we want to delete -> 1

    The function is used whenever we want to save new information. To save the new updated information, we have to
    delete the old one first.
    """
    if table_name in ALLOWED_TABLES_TO_DELETE_FROM:
        cursor.execute("DELETE FROM {table_name} WHERE id = ?".format(table_name=table_name), [id])
    else:
        print("You do not have permission to delete from the {} table!".format(table_name))


def get_highest_free_id_from_table(table_name: str, cursor):
    """
    This function returns the highest free unique id from a table
    This ID is most likely used to insert a new row into it
    """
    cursor.execute('SELECT max(id) FROM {}'.format(table_name))
    max_id = cursor.fetchone()[0]

    return max_id + 1



