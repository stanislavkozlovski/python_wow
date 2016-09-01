import classes

from command_handler import handle_main_commands
from information_printer import print_live_monsters, print_live_npcs, welcome_print
from zones.zone import Zone
from items import Weapon
from zones.northshire_abbey import NorthshireAbbey
GAME_VERSION = '0.0.4.9.1 ALPHA'
ZONES = {"Northshire Abbey": NorthshireAbbey()}


def main():
    welcome_print(GAME_VERSION)

    main_character = classes.Paladin(name="Netherblood")
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
