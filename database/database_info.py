"""
This module holds all kinds of information regarding the database and its tables.
"""
import os

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
DB_PATH = os.path.join(DIR_PATH, "python_wowDB.db")

DB_SC_EQUIPMENT_TABLE_NAME = 'saved_character_equipment'
DB_SC_LOADED_SCRIPTS_TABLE_NAME = 'saved_character_loaded_scripts'
DB_SC_KILLED_MONSTERS_TABLE_NAME = 'saved_character_killed_monsters'
DB_SC_INVENTORY_TABLE_NAME = 'saved_character_inventory'
DB_SC_COMPLETED_QUESTS_TABLE_NAME = 'saved_character_completed_quests'
