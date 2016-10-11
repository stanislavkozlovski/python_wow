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
    player_shield = "."  # serves as a dot if there is not a shield
    if player.absorption_shield:
        player_shield = " | {:.2f} shield.".format(player.absorption_shield)

    print("Character {0} is at {1:.2f}/{2} health | {3}/{4} mana{5}".format(player.name, player.health,
                                                                            player.max_health,
                                                                            player.mana,
                                                                            player.max_mana,
                                                                            player_shield))

    monster_shield = "."  # server as a dot if there is not a shield
    if monster.absorption_shield:
        monster_shield = " | {:.2f} shield.".format(monster.absorption_shield)
    print("Monster {0} is at {1:.2f}/{2} health | {3}/{4} mana{5}".format(monster.name, monster.health,
                                                                          monster.max_health, monster.mana,
                                                                          monster.max_mana,
                                                                          monster_shield))


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


def print_available_character_classes():
    """
    this function is called when the player is creating a new character. It displays the available classes to pick from and
    some information about the class
    """
    print("| "*20)
    print("Available classes: \n")
    print("\tPaladin:")
    print("\t\tDeals moderate damage")
    print("\t\tIs hard to kill")
    print("\t\tCan heal damage")
    print("| "*20)


def print_available_characters_to_load(characters_list: list):
    """
    This function prints all the saved characters in the database that the player can choose to load
    :param characters_list: A list of dictionaries for each character, holding the keys 'name','class' and 'level'.
    """
    if characters_list:
        print("Available characters to load:")
        for character in characters_list:
            print("\t| {name} - {level} {class_}".format(name=character['name'],
                                                        level=character['level'],
                                                        class_=character['class']))
    else:
        print("No available characters to laod from the DB, enter something to exit this prompt.")


def welcome_print(game_version: str):
    game_version = colored(game_version, attrs=['bold'])
    print("*"*80)
    print("WELCOME TO PYTHON WOW VERSION: {0}".format(game_version).center(80, ' '))
    print("A simple console RPG game".center(70, ' ') + '\n' + "inspired by the {warcraft} universe!".format(warcraft=colored("Warcraft", 'red')).center(80, ' '))
    print()
    print(colored("Type ? to see a list of available commands.".center(80, ' '), 'yellow'))
    print("*" * 80)
    print()
