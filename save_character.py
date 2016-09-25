"""
This module will take care for saving a character to the database
"""
import sqlite3

from entities import Character
from database_info import \
    (DB_PATH, DBINDEX_SAVED_CHARACTER_NAME, DBINDEX_SAVED_CHARACTER_CLASS, DBINDEX_SAVED_CHARACTER_LEVEL,
     DBINDEX_SAVED_CHARACTER_LOADED_SCRIPTS_TABLE_ID, DBINDEX_SAVED_CHARACTER_KILLED_MONSTERS_ID,
     DBINDEX_SAVED_CHARACTER_COMPLETED_QUESTS_ID, DBINDEX_SAVED_CHARACTER_INVENTORY_ID, DBINDEX_SAVED_CHARACTER_GOLD,

     DB_LOADED_SCRIPTS_TABLE_NAME)


ALLOWED_TABLES_TO_DELETE_FROM = ['saved_character_completed_quests', 'saved_character_inventory',
                                 'saved_character_killed_monsters', 'saved_character_loaded_scripts']

def save_character(character: Character):
    """
    Save the character into the database
    """

    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()

        character_info = cursor.execute("SELECT * FROM saved_character WHERE name = ?", ['Netherblood']).fetchone()

        character_level = character.level  # type: int
        character_class = character.get_class()
        character_gold = character.inventory['gold']  # type: int

        # see if the character already has it's row (has been saved)
        if character_info:
            # we have saved this character before, therefore we have the table IDs
            character_loaded_scripts_ID = character_info[DBINDEX_SAVED_CHARACTER_LOADED_SCRIPTS_TABLE_ID]
            character_killed_monsters_ID = character_info[DBINDEX_SAVED_CHARACTER_KILLED_MONSTERS_ID]
            character_completed_quests_ID = character_info[DBINDEX_SAVED_CHARACTER_COMPLETED_QUESTS_ID]
            character_inventory_ID = character_info[DBINDEX_SAVED_CHARACTER_INVENTORY_ID]
        else:
            # we have not saved this character before, therefore we need to generate new IDs for the other tables
            pass


def save_loaded_scripts(id: int, loaded_scripts: set):
    """
    This function saves the character's loaded scripts into the saved_character_loaded_scripts DB table
    Table sample contents:
    id,    script_name
      1,     HASKELL_PRAXTON_CONVERSATION

    :param id: the ID we have to save as
    :param loaded_scripts: a set containing all the names -> {HASKEL_PRAXTON_CONVERSATION} in this case
    """

    delete_rows_from_table(table_name=DB_LOADED_SCRIPTS_TABLE_NAME, id=id)  # delete the old values first

    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()

        for loaded_script in loaded_scripts:
            cursor.execute('INSERT INTO {} VALUES (?, ?)'.format(DB_LOADED_SCRIPTS_TABLE_NAME), [id, loaded_script])



def delete_rows_from_table(table_name: str, id: int):
    """
    This function will delete every row in TABLE_NAME with an id of ID
    :param table_name: a string -> "saved_character_loaded_scripts" for example
    :param id:  the id of the rows we want to delete -> 1

    The function is used whenever we want to save new information. To save the new updated information, we have to
    delete the old one first.
    """
    if table_name in ALLOWED_TABLES_TO_DELETE_FROM:
        with sqlite3.connect(DB_PATH) as connection:
            cursor = connection.cursor()

            cursor.execute("DELETE FROM {table_name} WHERE id = ?".format(table_name=table_name), [id])
    else:
        print("You do not have permission to delete from the {} table!".format(table_name))



