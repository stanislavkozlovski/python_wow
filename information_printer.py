"""
This module will hold functions that print all kinds of information to the player
"""
from termcolor import colored
from zones.zone import Zone
from constants import (CHARACTER_EQUIPMENT_BOOTS_KEY, CHARACTER_EQUIPMENT_BRACER_KEY,
                       CHARACTER_EQUIPMENT_HEADPIECE_KEY, CHARACTER_EQUIPMENT_CHESTGUARD_KEY,
                       CHARACTER_EQUIPMENT_NECKLACE_KEY, CHARACTER_EQUIPMENT_LEGGINGS_KEY,
                       CHARACTER_EQUIPMENT_GLOVES_KEY, CHARACTER_EQUIPMENT_SHOULDERPAD_KEY,
                       CHARACTER_EQUIPMENT_BELT_KEY)


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
            quest_information_to_print = f'{quest.name} [Requires Level {quest.required_level}]'

            colored_print = colored(quest_information_to_print, "red")
            print(colored_print)


def print_character_equipment(equipment: dict):
    """
    Prints the character's equipped in a nice, pretty ordered manner.
    :param equipment: a strictly-structured dictionary holding the character's equipment
    """
    gap_space = 200
    head_str = get_equipment_slot_string(equipment[CHARACTER_EQUIPMENT_HEADPIECE_KEY])
    shoulder_str = get_equipment_slot_string(equipment[CHARACTER_EQUIPMENT_SHOULDERPAD_KEY])
    necklace_str = get_equipment_slot_string(equipment[CHARACTER_EQUIPMENT_NECKLACE_KEY])
    chest_str = get_equipment_slot_string(equipment[CHARACTER_EQUIPMENT_CHESTGUARD_KEY])
    bracer_str = get_equipment_slot_string(equipment[CHARACTER_EQUIPMENT_BRACER_KEY])
    gloves_str = get_equipment_slot_string(equipment[CHARACTER_EQUIPMENT_GLOVES_KEY])
    belt_str = get_equipment_slot_string(equipment[CHARACTER_EQUIPMENT_BELT_KEY])
    legs_str = get_equipment_slot_string(equipment[CHARACTER_EQUIPMENT_LEGGINGS_KEY])
    boots_str = get_equipment_slot_string(equipment[CHARACTER_EQUIPMENT_BOOTS_KEY])

    print("-" * gap_space)
    print(create_fill_row_string(slot1='Head', slot2='Hands', gap_space=gap_space))
    print(head_str + get_gap_between_two_equipment_items(head_str, gloves_str, gap_space) + gloves_str)
    print(create_fill_row_string(slot1='Neck', slot2='', gap_space=gap_space))
    print(necklace_str + get_gap_between_two_equipment_items(necklace_str, '|', gap_space) + '|')
    print(create_fill_row_string(slot1='Shoulder', slot2='Waist', gap_space=gap_space))
    print(shoulder_str + get_gap_between_two_equipment_items(shoulder_str, belt_str, gap_space) + belt_str)
    print(create_fill_row_string(slot1='Chest', slot2='Legs', gap_space=gap_space))
    print(chest_str + get_gap_between_two_equipment_items(chest_str, legs_str, gap_space) + legs_str)
    print(create_fill_row_string(slot1='Wrist', slot2='Feet', gap_space=gap_space))
    print(bracer_str + get_gap_between_two_equipment_items(bracer_str, boots_str, gap_space) + boots_str)
    print("-" * gap_space)


def create_fill_row_string(slot1: str, slot2: str, gap_space: int):
    """ creates a gap with variable spaces according to the length of the slot string """
    return '|' + slot1 + (' ' * (gap_space-(2 + len(slot1) + len(slot2)))) + slot2 + '|'


def get_gap_between_two_equipment_items(first_item_str, second_item_str, gap_length) -> str:
    """ Specifically made for the print_character_equipment function, because we want to have an
    even gap between every printed items, we need to do this calculation to get the appropriate
    amount of whitespace characters in between two items"""
    empty_values = ['|empty|', '', ' ', '|']
    extra_colored_len = 0
    if first_item_str not in empty_values:
        extra_colored_len += 9  # extra length of the termcolor colored function on the str
    if second_item_str not in empty_values:
        extra_colored_len += 9

    return ' ' * (extra_colored_len + gap_length - (len(first_item_str) + len(second_item_str)))


def get_equipment_slot_string(equipment_item) -> str:
    """
    This function is called specifically for the print_character_equipment function in information_printer.py
    Returns the string representation of an Equipment object or returns empty if there is no such item.
    """
    if equipment_item:
        return str(equipment_item)

    return '|empty|'


def print_in_combat_stats(player, monster):
    p_shield_annexation = "."  # serves as a dot if there is not a shield
    if player.absorption_shield:
        p_shield_annexation = f' | {player.absorption_shield:.2f} shield.'

    print(f'Character {player.name} is at {player.health:.2f}/{player.max_health} health '
          f'| {player.mana}/{player.max_mana} mana{p_shield_annexation}')

    m_shield_annexation = "."  # server as a dot if there is not a shield
    if monster.absorption_shield:
        m_shield_annexation = f' | {monster.absorption_shield:.2f} shield.'
    print(f'Monster {monster.name} is at {monster.health:.2f}/{monster.max_health} health '
          f'| {monster.mana}/{monster.max_mana} mana{m_shield_annexation}')


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
            print(f'\t {item}')
    print()


def print_available_character_classes():
    """
    this function is called when the player is creating a new character. It displays the available classes to pick from
    and some information about the class
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
            print(f"\t| {character['name']} - {character['level']} {character['class']}")
    else:
        print("No available characters to laod from the DB, enter something to exit this prompt.")


def welcome_print(game_version: str):
    game_version = colored(game_version, attrs=['bold'])
    print("*"*80)
    print(f"WELCOME TO PYTHON WOW VERSION: {game_version}".center(80, ' '))
    print('{0}\n{1}'.format("A simple console RPG game".center(70, ' '),
                            "inspired by the {warcraft} universe!".format(warcraft=colored("Warcraft", 'red')).center(
                                80, ' ')))
    print()
    print(colored("Type ? to see a list of available commands.".center(80, ' '), 'yellow'))
    print("*" * 80)
    print()
