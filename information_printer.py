"""
This module will hold functions that print all kinds of information to the player
"""
from termcolor import colored
from zones.zone import Zone


def print_live_monsters(zone_object: Zone, print_all=False):
    """
    Prints the monsters that are alive in the current subzone
    :param zone_object: an object of class Zone in zones.zone.py
    :param print_all: A Boolean indicating if we want to print all the monsters in alive_monsters or by default: only 5
    """
    alive_monsters, _ = zone_object.get_cs_monsters()

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


def print_live_npcs(zone_object: Zone, print_all=False):
    """
    Prints the NPCs that are alive in the current subzone
    :param zone_object: an object of class Zone in zones.zone.py
    :param print_all: A Boolean indicating if we want to print all the npcs in alive_npcs or by default: only 5
    """
    alive_npcs, _ = zone_object.get_cs_npcs()
    print("Alive NPCs: ")
    printed_npcs = 0

    for _, npc in alive_npcs.items():
        print(npc)
        printed_npcs += 1

        if not print_all and printed_npcs == 5:
            break

    print()


def print_available_quests(available_quests: dict, players_level: int):
    """
    Prints all the quests that are available to the player in the current subzone
    :param available_quests:  A Dictionary Key: Quest Name, Value: Quest object from class Quest
    :param players_level: The player character's level. Used to check if he's eligible for given quest.
    :return:
    """
    print("Available quests: ")

    for _, quest in available_quests.items():
        if quest.required_level <= players_level:
            print(quest)
        else:
            quest_information_to_print = "{quest_name} [Requires Level {req_level}]".format(quest_name=quest.name,
                                                                                            req_level=quest.required_level)

            colored_print = colored(quest_information_to_print, "red")
            print(colored_print)


def print_in_combat_stats(player, monster):
    print("Character {0} is at {1:.2f}/{2} health | {3}/{4} mana.".format(player.name, player.health,
                                                                          player.max_health,
                                                                          player.mana,
                                                                          player.max_mana))


    print("Monster {0} is at {1:.2f}/{2} health | {3}/{4} mana.".format(monster.name, monster.health,
                                                                        monster.max_health, monster.mana,
                                                                        monster.max_mana))


def print_character_xp_bar(player):
    print("{0}/{1} Experience. {2} needed to level up!".format(player.experience,
                                                               player.xp_req_to_level,
                                                               player.xp_req_to_level - player.experience))


def print_loot_table(monster_loot: dict):
    """
    Prints the loot table
    :param monster_loot: a dictionary that holds the loot the monster has dropped
    """
    print()
    print("Loot dropped:")

    if "gold" in monster_loot.keys():
        # print the gold separately so it always comes up on top
        print(colored("\t{} gold".format(monster_loot['gold']), color="yellow"))

    for item_name, item in monster_loot.items():  # type: dict
        if item_name is not "gold":
            print("\t{}".format(item))


def print_quest_item_choices(quest_item_rewards: dict):
    """ This function prints the item rewards from a quest from which the player can only pick one """

    print("You must choose to take one of the following items:")
    for item in quest_item_rewards.values():
        if item:
            print("\t {}".format(item))
    print()

