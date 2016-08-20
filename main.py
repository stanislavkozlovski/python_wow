# TODO: Add talents system and Class classes
# TODO: add more monsters and subzones
# TODO: Add list with last twenty prints, clear the console and rewrite again whenever a command has been added
# TODO: A million other things
# TODO: Refactor function parameter names in the command_handler and information_printer modules
# TODO: Print in colors
# TODO: Research more about the curses module and maybe about alternatives
# TODO: Remove the int() calls from loader.py
# TODO: Print own inventory
# TODO: Print NPCs
# TODO: Move these TODOs to a separate file!
# TODO: Fix the targeting of NPCs by filtering the None variables (line 61 and etc)

import classes

from command_handler import handle_main_commands, print_live_monsters, print_live_npcs
from zones.zone import Zone
from items import Weapon
from zones.elwynn_forest import ElwynnForest

GAME_VERSION = '0.0.3.25 ALPHA'
ZONES = {"Elwynn Forest": ElwynnForest()}


def main():
    welcome_print()

    main_character = classes.Paladin(name="Netherblood")
    starter_weapon = Weapon(name="Starter Weapon", min_damage=1, max_damage=3)
    main_character.equip_weapon(starter_weapon)
    print("Character {0} created!".format(main_character.name))
    zone_object = get_zone_object(main_character.current_zone)  # type: Zone

    alive_npcs, _ = zone_object.get_cs_npcs()
    alive_monsters, _ = zone_object.get_cs_monsters()

    print_live_npcs(alive_npcs, print_all=True)
    print_live_monsters(alive_monsters)
    while True:
        handle_main_commands(main_character, zone_object)


def get_zone_object(zone: str):
    """
    :param zone: The name of the zone
    :return: Returns a class object from the ZONES dictionary
    """
    return ZONES[zone]


def welcome_print():
    print("WELCOME TO PYTHON WOW VERSION: {0}".format(GAME_VERSION))
    print("A simple console RPG game inspired by the Warcraft universe!")
    print()
    print("Type ? to see a list of available commands.")
    print()


if __name__ == '__main__':
    main()
