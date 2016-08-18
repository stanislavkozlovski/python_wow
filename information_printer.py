"""
This module will hold functions that print all kinds of information to the player
"""
from termcolor import colored

def print_live_monsters(alive_monsters: dict, print_all=False):
    """
    Prints the monsters that are alive in the current subzone
    :param alive_monsters: A Dictionary key: Monster_GUID, value: Monster class object
    :param print_all: A Boolean indicating if we want to print all the monsters in alive_monsters or by default: only 5
    """

    print("Alive monsters: ")
    # sort them by level and print the five that are the lowest level
    sorted_list = sorted(alive_monsters.items(), key=lambda x: x[1].level)
    printed_monsters = 0
    for _, monster in sorted_list:
        print(monster)
        printed_monsters += 1

        if not print_all and printed_monsters == 5:  # print only five monsters at once
            break

    print()


def print_live_npcs(alive_npcs: dict, print_all=False):
    """
    Prints the NPCs that are alive in the current subzone
    :param alive_npcs: A Dictionary key: NPC_GUID, value: FriendlyNPC class object
    :param print_all: A Boolean indicating if we want to print all the npcs in alive_npcs or by default: only 5
    """
    print("Alive NPCs: ")
    printed_npcs = 0

    for _, npc in alive_npcs.items():
        print(npc)
        printed_npcs += 1

        if not print_all and printed_npcs == 5:
            break

    print()


def print_available_quests(available_quests: dict, character_level: int):
    """
    Prints all the quests that are available to the player in the current subzone
    :param available_quests:  A Dictionary Key: Quest Name, Value: Quest object from class Quest
    :param character_level: The player character's level. Used to check if he's eligible for given quest.
    :return:
    """
    print("Available quests: ")

    for _, quest in available_quests.items():
        if quest.required_level <= character_level:
            print("{quest_name} - Requires {required_kills} {monster_name} kills. Rewards {xp_reward} experience."
                  .format(quest_name=quest.name, required_kills=quest.required_kills,
                          monster_name=quest.monster_to_kill, xp_reward=quest.xp_reward))
        else:
            quest_information_to_print = "{quest_name} [Requires Level {req_level}]".format(quest_name=quest.name,
                                                                                            req_level=quest.required_level)

            colored_print = colored(quest_information_to_print, "red")
            print(colored_print)