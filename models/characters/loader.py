from sqlalchemy.orm import load_only

from exceptions import NoSuchCharacterError
from models.characters.saved_character import SavedCharacterSchema
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
    loaded_character: SavedCharacterSchema = session.query(SavedCharacterSchema).filter_by(name=name).one_or_none()

    if loaded_character is None:
        raise NoSuchCharacterError(f'There is no saved character by the name of {name}!')

    return loaded_character.convert_to_character_object()


def load_all_saved_characters_general_info() -> [dict()]:
    """
    This function loads general information about the saved characters in the DB and returns it as a list of
    dictionaries to  be easily printable.
    """
    loaded_characters: [SavedCharacterSchema] = session.query(SavedCharacterSchema).options(load_only("name", "character_class", "level")).all()

    return [{'name': ch.name, 'class': ch.character_class, 'level': ch.level} for ch in loaded_characters]
