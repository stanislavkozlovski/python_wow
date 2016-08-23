"""
This is the class that will print and return the available commands when the user asks for them

abbreviation PAC means Print Available Commands
"""
from classes import Paladin
from entities import Character


def pac_main_ooc():
    """
    Prints all the possible commands you can use while out of combat.
    """
    print()
    print("Available commands:")
    print("\tengage [Monster Name]")
    print("\t\tEngages in combat with the monster whose name you've entered.\n")
    print("\ttalk to [NPC Name]")
    print("\t\tTalks to the NPC.\n")
    print("\tbuy from [NPC Name]")
    print("\t\tOpens a dialogue with the vendor where you can see and buy the items he has for sale.\n")
    print("\topen inventory")
    print("\t\tGives you access to your inventory.\n")
    print("\tprint alive monsters")
    print("\tpam")
    print("\t\tPrints 5 monsters that are alive.\n")
    print("\tprint alive npcs")
    print("\tpan")
    print("\t\tPrints 5 NPCs that are alive.\n")
    print("\tprint all alive monsters")
    print("\t\tPrints all monsters that are alive.\n")
    print("\tprint all alive npcs")
    print("\t\tPrints all NPCs that are alive.\n")
    print("\tprint available quests")
    print("\tpaq")
    print("\t\tPrints all quests that are available in the current zone/subzone.\n")
    print("\tprint quest log")
    print("\t\tPrints the quests you are currently on.\n")
    print("\tprint inventory")
    print("\t\tPrints every item in your inventory.\n")
    print("\tgo to [Sub Zone]")
    print("\t\tMoves the character to the selected sub zone.\n")
    print("\tgo to ?")
    print("\t\tShows a list of the reachable sub zones from the one the character is in.\n")
    print("\t?")
    print("\t\tShows a list of available commands.\n")


def pac_in_combat(character):
    """
    Prints all possible commands that can be used in combat
    :param character: A Character object from class entities.py/Character
    :return:
    """
    print()
    print("Available commands that do not end the turn:")
    print("\tprint stats")
    print("\t\tPrints information about the character and monster\n")
    print("\tprint xp")
    print("\t\tPrints the experience points of the character and the amount needed to level up\n")
    print("\t?")
    print("\t\tShows a list of available commands.\n")
    print()
    print("Available commands that end the turn:")
    print("\tattack")
    print("\t\tAttacks the monster you are in combat with a meele swing.\n")
    print_class_abilities_in_combat(character)


def pac_vendor_dialogue():
    print("\tbuy [Item Name]")
    print("\t\tBuys the item from the vendor.\n")
    print("\texit")
    print("\t\tCloses the vendor window..\n")
    print("\t?")
    print("\t\tShows a list of available commands.\n")


def pac_looting():
    """Prints all possible commands the player can use while looting a creature"""
    print()
    print("Available commands:")
    print("\ttake gold")
    print("\t\tLoots the gold dropped from the monster.\n")
    print("\ttake [item_name]")
    print("\t\tLoots the specified item.\n")
    print("\texit")
    print("\t\tExits the loot window")
    print("\t?")
    print("\t\tShows a list of available commands.\n")


def pac_opened_inventory():
    """Prints all possible commands that the player can use while his inventory is opened"""
    print("\tequip [Item Name]")
    print("\t\tEquips the item\n")
    print("\texit")
    print("\t\tCloses the inventory\n")
    print("\t?")
    print("\t\tShows a list of available commands.\n")

def pac_map_directions(possible_routes: list):
    """
    Prints all possible subzones you can go in from your current subzone
    :param possible_routes: A list holding the name of each subzone you have access to
    """
    print("Possible directions:")
    for route in possible_routes:
        print("\t\t{route}".format(route=route))


def print_class_abilities_in_combat(character: Character):
    if character.get_class() == 'paladin':
        print_paladin_abilities_in_combat(character)


######### PALADIN #########
def print_paladin_abilities_in_combat(character: Paladin):
    print("\tsor")
    print("\t\tCasts Seal of Righteousness")
    print("\t\t\tMana Cost: {}".format(character.learned_spells['Seal of Righteousness']['mana_cost']))
    print("'\t\t\tLasts three turns and adds {0} damage to each of your auto attacks\n".format(
        character.learned_spells['Seal of Righteousness'][
            'damage_on_swing']))  # TODO: rename damage_on_swing to damage_1
    if "Flash of Light" in character.learned_spells.keys():
        print("\tfol")
        print("\t\tCasts Flash of Light")
        print("\t\t\tMana Cost: {}".format(character.learned_spells['Flash of Light']['mana_cost']))
        print("\t\t\tHeals the paladin for {0} damage.".format(character.learned_spells['Flash of Light'][
                                                                   'heal_1']))  # TODO: Move to a method in paladin that gives heal amount of spell name


def get_available_paladin_abilities(character: Paladin):
    """
    Returns a set holding the COMMANDS for all of the available paladin spells to use
    :param character:
    :return:
    """
    available_spells = set()
    available_spells.add('sor')

    if "Flash of Light" in character.learned_spells.keys():
        available_spells.add('fol')

    # TODO: Add a method in paladin that returns this set
    return available_spells
######### PALADIN #########