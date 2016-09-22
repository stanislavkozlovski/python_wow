import classes

from command_handler import handle_main_commands
from information_printer import print_live_monsters, print_live_npcs, welcome_print
from zones.zone import Zone
from items import Weapon
from zones.northshire_abbey import NorthshireAbbey
GAME_VERSION = '0.0.4.9.4 ALPHA'
ZONES = {"Northshire Abbey": None}

# TODO: CURRENT TASK:Add the ability to save/load the character
#  Subtasks

# TODO: Current SUBTASK: Adding the loading of saved_character_killed_monsters and it's implementation in the game

# TODO: Fix Brother Haskel/Paxton in subzone after the script is not loaded (because of it being in saved_character_loaded_scripts)
# TODO: Add a prompt where you choose if you want to create a new character or save one
# TODO: Move the load character to another module
# TODO: Save/load the quests you've done
# TODO: Save/load special monsters that you've killed
# TODO: Save/load scripts that you've seen

def main():
    welcome_print(GAME_VERSION)
    from loader import load_saved_character
    main_character = load_saved_character(name='Netherblood')
    ZONES["Northshire Abbey"] = NorthshireAbbey(main_character)
    starter_weapon = Weapon(name="Starter Weapon", min_damage=1, max_damage=3)
    main_character.equip_weapon(starter_weapon)
    print("Character {0} created!".format(main_character.name))

    zone_object = get_zone_object(main_character.current_zone)  # type: Zone

    alive_npcs, _ = zone_object.get_cs_npcs()
    alive_monsters, _ = zone_object.get_cs_monsters()

    print_live_npcs(zone_object, print_all=True)
    print_live_monsters(zone_object)

    # main game loop
    while True:
        handle_main_commands(main_character, zone_object)


def get_zone_object(zone: str):
    """
    :param zone: The name of the zone
    :return: Returns a class object from the ZONES dictionary
    """
    return ZONES[zone]


if __name__ == '__main__':
    main()
