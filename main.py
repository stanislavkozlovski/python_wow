# TODO: Add talents system and Class classes
# TODO: add more monsters and subzones
# TODO: Add a AddExperience method in Character and replace where appropriate
# TODO: Add list with last twenty prints, clear the console and rewrite again whenever a command has been added
# TODO: A million other things
# TODO: Add friendly NPCs
# TODO: Handle stackable items
import classes
import combat
from commands import pac_main_ooc, pac_map_directions
from items import Weapon
from zones.elwynn_forest import ElwynnForest

GAME_VERSION = '0.0.3 ALPHA'
ZONES = {"Elwynn Forest": ElwynnForest}


def main():
    welcome_print()

    main_character = classes.Paladin(name="Netherblood")
    starter_weapon = Weapon(name="Starter Weapon", min_damage=1, max_damage=3)
    main_character.equip_weapon(starter_weapon)
    print("Character {0} created!".format(main_character.name))
    zone_object = get_zone_object(main_character.current_zone)
    # map_directions - a list of all the possible subzones we could go to from ours directly
    map_directions = zone_object.get_map_directions(zone_object, main_character.current_subzone)
    '''
    alive_monsters: A Dictionary: Key: guid of monster, Value: Object of class entities.py/Monster
    guid_name_set: A Set of Tuples ((Monster GUID, Monster Name)) used to convert the engage X command to target a creature in alive_monsters
    available_quests: A Dictionary: Key: name of quest, Value: Object of class quest.py/Quest
    '''
    alive_monsters, guid_name_set, available_quests, _ = zone_object.get_live_monsters_guid_name_set_and_quest_list(
        zone_object, main_character.current_subzone)
    print_live_monsters(alive_monsters)
    while True:
        command = input()
        if command is '?':
            pac_main_ooc()  # print available commands in the main loop when out of combat
        elif command == 'go to ?':
            pac_map_directions(possible_routes=map_directions)
        elif command == 'print available quests' or command == 'paq':
            print_available_quests(available_quests, main_character.level)
        elif command == 'print quest log':
            main_character.print_quest_log()
        elif command == 'print inventory':
            main_character.print_inventory()
        elif 'engage' in command:
            target = command[7:]  # name of monster to engage

            # return a list with the guids for each monster we've targeted and get the first guid [0]
            # using the guid, target him from the alive_monsters dictionary
            target_guid_list = [guid if name == target else None for guid, name in guid_name_set]
            if target_guid_list:
                target_guid = target_guid_list[0]
            else:  # if the list is empty
                target_guid = None

            if target_guid in alive_monsters.keys():
                target = alive_monsters[target_guid]  # convert the string to a Monster object
                combat.engage_combat(main_character, target, alive_monsters, guid_name_set, target_guid)
            else:
                print("Could not find creature {}.".format(target))
        elif 'accept' in command:  # accept the quest
            quest_to_accept = command[7:]  # name of quest to accept

            if quest_to_accept in available_quests.keys():
                quest = available_quests[quest_to_accept]

                if main_character.level >= quest.level_required:
                    print("Accepted Quest - {}".format(quest.name))
                    main_character.add_quest(quest)
                    del available_quests[quest_to_accept]  # removes it from the list
                else:
                    print("You need to be level {} to accept {}".format(quest.level_required, quest.name))

            else:
                print("No such quest.")
        elif 'go to' in command:
            destination = command[6:]

            temp_alive_monsters, temp_guid_name_set, temp_available_quests, zone_is_valid = \
                zone_object.get_live_monsters_guid_name_set_and_quest_list(zone_object, destination)

            if zone_is_valid and destination in map_directions:
                # if the move has been successful

                alive_monsters, guid_name_set, available_quests = temp_alive_monsters, temp_guid_name_set, temp_available_quests

                main_character.current_subzone = destination
                # update map directions
                map_directions = zone_object.get_map_directions(zone_object, main_character.current_subzone)
                print("Moved to {0}".format(main_character.current_subzone))
                print_live_monsters(alive_monsters)
            else:
                print("No such destination as {} that is connected to your current subzone.".format(destination))

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

        if not print_all and printed_monsters == 5:  # print only five monsters at once
            break


def print_available_quests(available_quests: dict, character_level: int):
    print("Available quests: ")

    for _, quest in available_quests.items():
        if quest.level_required <= character_level:  # print quests that the character has the required level for only!
            print("{quest_name} - Requires {required_kills} {monster_name} kills. "
                  + "Rewards {xp_reward} experience.".format(quest_name=quest.name,
                                                             required_kills=quest.needed_kills,
                                                             monster_name=quest.monster_to_kill,
                                                             xp_reward=quest.xp_to_give))


def welcome_print():
    print("WELCOME TO PYTHON WOW VERSION: {0}".format(GAME_VERSION))
    print("A simple console RPG game inspired by the Warcraft universe!")
    print()
    print("Type ? to see a list of available commands.")
    print()


if __name__ == '__main__':
    main()
