import atexit

from command_router import route_main_commands
from information_printer import print_live_monsters, print_live_npcs, welcome_print
from zones.zone import Zone
from items import Weapon
from save_character import save_character
from start_game_prompt import get_player_character
from zones.northshire_abbey import NorthshireAbbey
GAME_VERSION = '0.0.5.8.5 ALPHA'
ZONES = {"Northshire Abbey": None}


def main():
    welcome_print(GAME_VERSION)
    main_character = get_player_character()
    atexit.register(on_exit_handler, main_character)
    ZONES["Northshire Abbey"] = NorthshireAbbey(main_character)
    starter_weapon = Weapon(name="Starter Weapon", item_id=0, min_damage=1, max_damage=3)
    main_character.equip_weapon(starter_weapon)
    print("Character {0} created!".format(main_character.name))

    zone_object = get_zone_object(main_character.current_zone)  # type: Zone

    alive_npcs, _ = zone_object.get_cs_npcs()
    alive_monsters, _ = zone_object.get_cs_monsters()

    print_live_npcs(zone_object, print_all=True)
    print_live_monsters(zone_object)

    # main game loop
    while True:
        route_main_commands(main_character, zone_object)


def get_zone_object(zone: str):
    """
    :param zone: The name of the zone
    :return: Returns a class object from the ZONES dictionary
    """
    return ZONES[zone]


def on_exit_handler(character):
    """ saves the character when the user quits the game"""
    save_character(character)

if __name__ == '__main__':
    main()
