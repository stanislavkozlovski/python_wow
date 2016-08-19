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


def print_in_combat_stats(character, monster):
    print("Character {0} is at {1:.2f}/{2} health | {3}/{4} mana.".format(character.name, character.health,
                                                                          character.max_health,
                                                                          character.mana,
                                                                          character.max_mana))


    print("Monster {0} is at {1:.2f}/{2} health | {3}/{4} mana.".format(monster.name, monster.health,
                                                                        monster.max_health, monster.mana,
                                                                        monster.max_mana))


def print_character_xp_bar(character):
    print("{0}/{1} Experience. {2} needed to level up!".format(character.experience,
                                                               character.xp_req_to_level,
                                                               character.xp_req_to_level - character.experience))

def print_loot_table(monster):
    """
    Prints the loot table
    :param monster: A monster object of class Monster
    """
    print()
    print("Loot dropped:")

    if "gold" in monster.loot.keys():
        # print the gold separately so it always comes up on top
        print("\t{} gold".format(monster.loot['gold']))

    for item_name, item in monster.loot.items():  # type: dict
        if item_name is not "gold":
            print("\t{}".format(item))
