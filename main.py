# TODO: Add command that shows all available commands
# TODO: Add talents system and Class classes
# TODO: Add abilities to said classes
# TODO: Move the csvs to a /data folder
# TODO: Modify Monster __str__ method to print damage
# TODO: Figure out a way to have multiple creatures with the same name
# TODO: Add list with last twenty prints, clear the console and rewrite again whenever a command has been added
# TODO: A million other things
"""
current commands:
attack - attacks the creature and ends the turn
print stats - prints your health and the monster's. does not end the turn
print xp - prints the XP you have and the necessary amount to reach the next level
engage - start the fight
"""
import combat
import csv
from entities import Character, Monster
from items import Weapon
GAME_VERSION = '0.0.2.4 ALPHA'

def main():
    welcome_print()
    main_character = Character(name="Netherblood",
                               health=10,
                               mana=10,
                               strength=3)
    starter_weapon = Weapon(min_damage=1, max_damage=3)
    main_character.equip_weapon(starter_weapon)
    print("Character {0} created!".format(main_character.name))
    alive_monsters = load_monsters()
    while True:
        # TODO: Add info commands here
        print_live_monsters(alive_monsters)

        command = input()
        if 'engage' in command:
            target = command[7:] # name of monster to engage

            if target in alive_monsters.keys():
                target = alive_monsters[target] # convert the string to a Monster object
                combat.engage_combat(main_character, target, alive_monsters)


def load_monsters():
    """
    Reads the creature_template.csv to get information about all of the creatures in the game
    creature_template.csv is of format:

    creature ID, creature name, level, hp, mana, min_dmg, max_dmg
              1, Zimbab       ,     1, 10,   10,       2,       4
    Creature Level: 1 Zimbab, HP: 10, MANA: 10, Damage: 2-4

    :return: A Dictionary: Key: Monster Name, Value: Object of class entities.py/Monster
    """
    # TODO: Move this somewhere else
    # TODO: Think of another approach rather than loading them all at once!
    # Maybe use a generator and read enough to fill the list with five monsters

    monsters_dict = {}

    with open('creature_template.csv') as _:
        monster_reader = csv.reader(_)
        for creature_info in monster_reader:
            creature_id = int(creature_info[0])
            name = creature_info[1]
            level = int(creature_info[2])
            health = int(creature_info[3])
            mana = int(creature_info[4])
            min_dmg = int(creature_info[5])
            max_dmg = int(creature_info[6])

            monsters_dict[name] = Monster(monster_id=creature_id,
                                          name=name,
                                          level=level,
                                          health=health,
                                          mana=mana,
                                          min_damage=min_dmg,
                                          max_damage=max_dmg)

    return monsters_dict


def print_live_monsters(alive_monsters: dict):
    print("Alive monsters: ")
    # sort them by level and print the five that are the lowest level
    sorted_list = sorted(alive_monsters.items(), key=lambda x: x[1].level)
    printed_monsters = 0
    for _, monster in sorted_list:
        print(monster)
        printed_monsters += 1

        if printed_monsters == 5: # print only five monsters at once
            break


def welcome_print():
    print("WELCOME TO PYTHON WOW VERSION: {0}".format(GAME_VERSION))
    print("A simple console RPG game inspired by the Warcraft universe!")
    print()
if __name__ == '__main__':
    main()