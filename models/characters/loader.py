from models.characters.saved_character import SavedCharacter
from database.main import session


def load_saved_character(name: str):
    """
    This function loads the information about a saved chacacter in the saved_character DB table.

       name,   class,  level,  loaded_scripts_ID,  killed_monsters_ID, completed_quests_ID, inventory_ID, gold
Netherblood, Paladin,     10,                 1,                    1,                   1,            1,   23

    The attributes that end in ID like loaded_scripts_ID are references to other tables.

    For more information:
    https://github.com/Enether/python_wow/wiki/How-saving-a-Character-works-and-information-about-the-saved_character-database-table.
    """
    from classes import Paladin
    loaded_character = session.query(SavedCharacter).filter_by(name=name).one_or_none()

    if loaded_character is None:
        raise NoSuchCharacterError(f'There is no saved character by the name of {name}!')

    loaded_scripts: {str} = {script.script_name for script in loaded_character.loaded_scripts}
    killed_monsters: {int} = {monster.guid for monster in loaded_character.killed_monsters}
    completed_quests: {str} = {quest.id for quest in loaded_character.completed_quests}
    inventory: {str: tuple} = {item.item.name: (item.item, item.item_count) for item in loaded_character.inventory}
    inventory['gold'] = loaded_character.gold
    equipment = loaded_character.build_equipment()

    if loaded_character.character_class == 'paladin':
        return Paladin(name=loaded_character.name,
                            level=loaded_character.level,
                            loaded_scripts=loaded_scripts,
                            killed_monsters=killed_monsters,
                            completed_quests=completed_quests,
                            saved_inventory=inventory,
                            saved_equipment=equipment)
    else:
        raise Exception(f'Unsupported class - {loaded_character.character_class}')
