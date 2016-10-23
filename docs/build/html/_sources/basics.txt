Basics
======

For placeholders, this article will use these symbols {}


Starting out
============

When first starting the game, you're prompted to create a new character.
Immediately after creation, you're popped into the world and the monsters are shown.
You have the choice to type "?" to see all available commands or engage an attack on a monster with
    engage {monsterName}
You swing at the monster using the
    attack
command and all is well. Once you kill the monster, loot drops from it.
    Loot dropped:
        3 gold
        
        Wolf Meat - Miscellaneous Item
        
        Wolf Pelt - Miscellaneous Item
        
        Strength Potion - Potion (Increases strength by 15 for 5 turns.)
You can take specific items with the
    take {itemName}
command, take everything with the
    take all
command or simply exit the menu, using the (you guessed it)
    exit
command.

But enough about the action of playing the game, we can go on forever with that, let's see how it works under the hood.

Creating/Loading a character
============================

We get the character, which is an object of the class Character (more on that later) with this function in our main.py file::

    from start_game_prompt import get_player_character
    main_character = get_player_character()
    
In the start_game_prompt, we handle user input to see if we want to load or create a new character.

Creating a character
======================
The function, stripped down to it's essentials::

    def handle_create_character() -> Character:
        class_choice = str.lower(input())

        while class_choice not in AVAILABLE_CLASSES:  # check for valid class
            class_choice = str.lower(input())

        character_name = input()

        if class_choice == 'paladin':
            character = Paladin(name=character_name)

        return character
        
Really really straightforward, what we do is create a new Paladin object with default values.
Part of the Paladin constructor::
    def __init__(self, name: str, level: int = 1, health: int = 12, mana: int = 15, strength: int = 4):
    
Loading a character
====================
We do this by calling the load_saved_character function from the loader.py file.::

    from loader import load_saved_character, load_all_saved_characters_general_info
    character = load_saved_character(character_name)

I think the docstring to the method explains things fairly well::

    """
    This function loads the information about a saved chacacter in the saved_character DB table.

       name,   class,  level,  loaded_scripts_ID,  killed_monsters_ID, completed_quests_ID, inventory_ID, gold
       Netherblood, Paladin,     10,                 1,                    1,                   1,            1,   23

    The attributes that end in ID like loaded_scripts_ID are references to other tables.

    For more information:
    https://github.com/Enether/python_wow/wiki/How-saving-a-Character-works-and-information-about-the-saved_character-database-table.
    """

In steps:

#. We query the database and save the IDs used for sub-tables::

    sv_char_reader = cursor.execute("SELECT * FROM saved_character WHERE name = ?", [name]).fetchone()
    char_loaded_scripts_ID = sv_char_reader[DBINDEX_SAVED_CHARACTER_LOADED_SCRIPTS_TABLE_ID]
    char_killed_monsters_ID = sv_char_reader[DBINDEX_SAVED_CHARACTER_KILLED_MONSTERS_ID]
    char_completed_quests_ID = sv_char_reader[DBINDEX_SAVED_CHARACTER_COMPLETED_QUESTS_ID]
    char_equipment_ID = sv_char_reader[DBINDEX_SAVED_CHARACTER_EQUIPMENT_ID]
    char_inventory_ID = sv_char_reader[DBINDEX_SAVED_CHARACTER_INVENTORY_ID]
    
#. Using the IDs, we call a function associated with each sub-table.
    * load_saved_character_loaded_scripts returns a set, containing the name of special in-game scripts that the character has already seen, because we do not want him to see them again.
    * load_saved_character_killed_monsters returns a set, containing the unique GUID for every special monster that the character has killed. Only monsters that should be killed once in the game are added here.
    * load_saved_character_completed_quests returns a set, containing the names of the character's completed quests. This, like the previous two, is stored so as to not load the quests in the game again.
    * load_saved_character_inventory returns a dictionary, holding the inventory of the player as it is stored in the Character class, Key: item_name, Value: tuple(object of class Item, int item_count)
    * load_saved_character_equipment returns a dictionary, holding the equipment of the player as it is stored in the Character class. Key: the equipment's slot e.g: "Shoulderpad", Value: an object of class Item
    In the DB, the actual equipment's value is stored as the item's ID. In the function, we use a list comprehension to convert all the loaded IDs into objects of class Item::
    
            saved_equipment_info = [load_item(id) if id is not None else None for id in saved_equipment_info]

    

