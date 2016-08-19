# TODO: Add talents system and Class classes
# TODO: add more monsters and subzones
# TODO: Add list with last twenty prints, clear the console and rewrite again whenever a command has been added
# TODO: A million other things
# TODO: Refactor combat.py, moving the commands into functions and print functions into their respective modules
# TODO: Refactor function parameter names in the command_handler and information_printer modules
# TODO: Maybe create subzone class?
# TODO: Print in colors
# TODO: Research more about the curses module and maybe about alternatives

import classes

from command_handler import handle_main_commands, print_live_monsters, print_live_npcs
from zones.zone import Zone
from items import Weapon
from zones.elwynn_forest import ElwynnForest

GAME_VERSION = '0.0.3.1 ALPHA'
ZONES = {"Elwynn Forest": ElwynnForest}


def main():
    welcome_print()

    main_character = classes.Paladin(name="Netherblood")
    starter_weapon = Weapon(name="Starter Weapon", min_damage=1, max_damage=3)
    main_character.equip_weapon(starter_weapon)
    print("Character {0} created!".format(main_character.name))
    zone_object = get_zone_object(main_character.current_zone)  # type: Zone
    '''
    alive_monsters: A Dictionary: Key: guid of monster, Value: Object of class entities.py/Monster
    guid_name_set: A Set of Tuples ((Monster GUID, Monster Name)) used to convert the engage X command to target a creature in alive_monsters
    available_quests: A Dictionary: Key: name of quest, Value: Object of class quest.py/Quest
    '''
    alive_monsters, guid_name_set, alive_npcs, npc_guid_name_set, available_quests,  _ = zone_object.get_zone_attributes(zone_object,
        main_character.current_subzone)

    print_live_npcs(alive_npcs, print_all=True)
    print_live_monsters(alive_monsters)
    while True:
        handle_main_commands(main_character, available_quests, alive_npcs,
                                              npc_guid_name_set, alive_monsters, guid_name_set, zone_object)


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
