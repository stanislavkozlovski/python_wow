# TODO: Add talents system and Class classes
# TODO: Lots of things to do regarding quests
# TODO: Quest - add to DB
# TODO: Quest - tie to zones
# TODO: Quest - clean up code
# TODO: Quest - print commands
# TODO: Quest - commands to accept quest
# TODO: add more monsters and subzones
# TODO: Add a AddExperience method in Character and replace where appropriate
# TODO: Add list with last twenty prints, clear the console and rewrite again whenever a command has been added
# TODO: A million other things
"""
current commands:
attack - attacks the creature and ends the turn
print stats - prints your health and the monster's. does not end the turn
print xp - prints the XP you have and the necessary amount to reach the next level
engage - start the fight
"""
import sqlite3
import combat
from quest import Quest
from commands import pac_main_ooc, pac_map_directions
from items import Weapon
import classes
from zones.elwynn_forest import ElwynnForest
DB_PATH = './python_wowDB.db'
GAME_VERSION = '0.0.2.8 ALPHA'
ZONES = {"Elwynn Forest": ElwynnForest}

def main():
    welcome_print()

    main_character = classes.Paladin(name="Netherblood")
    starter_weapon = Weapon(min_damage=1, max_damage=3)
    main_character.equip_weapon(starter_weapon)
    print("Character {0} created!".format(main_character.name))
    main_character.add_quest(Quest(quest_name="Kill 2 Wolves", quest_id=1, creature_name="Wolf", kill_amount=2, xp_reward=1000))
    zone_object = get_zone_object(main_character.current_zone)

    alive_monsters, guid_name_set = zone_object.get_live_monsters_and_guid_name_set(zone_object, main_character.current_subzone)
    print_live_monsters(alive_monsters)
    while True:
        command = input()
        if command is '?':
            pac_main_ooc()  # print available commands in the main loop when out of combat
        elif command == 'go to ?':
            map_directions = zone_object.get_map_directions(zone_object, main_character.current_subzone)
            pac_map_directions(possible_routes=map_directions)
        elif 'engage' in command:
            target = command[7:] # name of monster to engage

            # return a list with the guids for each monster we've targeted and get the first guid [0]
            # using the guid, target him from the alive_monsters dictionary
            target_guid = [guid if name == target else None for guid, name in guid_name_set][0]

            if target_guid in alive_monsters.keys():
                target = alive_monsters[target_guid] # convert the string to a Monster object
                combat.engage_combat(main_character, target, alive_monsters, guid_name_set, target_guid)
        elif 'go to' in command:
            destination = command[6:]
            main_character.current_subzone = destination
            alive_monsters, guid_name_set = zone_object.get_live_monsters_and_guid_name_set(zone_object,
                                                                                            main_character.current_subzone)
            print("Moved to {0}".format(main_character.current_subzone))
            print_live_monsters(alive_monsters)
        elif command == 'print alive monsters' or command == 'pam':
            print_live_monsters(alive_monsters)
        elif command == 'print all alive monsters':
            print_live_monsters(alive_monsters, print_all=True)


def get_zone_object(zone: str):
    """

    :param zone: The name of the zone
    :return: Returns a class object from the ZONES dictionary
    """
    return ZONES[zone]


def print_live_monsters(alive_monsters: dict, print_all=False):
    print("Alive monsters: ")
    # sort them by level and print the five that are the lowest level
    sorted_list = sorted(alive_monsters.items(), key=lambda x: x[1].level)
    printed_monsters = 0
    for _, monster in sorted_list:
        print(monster)
        printed_monsters += 1

        if not print_all and printed_monsters == 5: # print only five monsters at once
            break


def welcome_print():
    print("WELCOME TO PYTHON WOW VERSION: {0}".format(GAME_VERSION))
    print("A simple console RPG game inspired by the Warcraft universe!")
    print()
    print("Type ? to see a list of available commands.")
    print()
if __name__ == '__main__':
    main()