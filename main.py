# TODO: Add command that shows all available commands
# TODO: Add talents system and Class classes
# TODO: Add abilities to said classes
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
import sqlite3
import combat
from entities import Character, Monster
from commands import pac_main_ooc
from items import Weapon
DB_PATH = './python_wowDB.db'
GAME_VERSION = '0.0.2.55 ALPHA'


def main():
    alive_monsters = load_monsters()

    welcome_print()
    main_character = Character(name="Netherblood",
                               health=10,
                               mana=10,
                               strength=3)
    starter_weapon = Weapon(min_damage=1, max_damage=3)
    main_character.equip_weapon(starter_weapon)
    print("Character {0} created!".format(main_character.name))

    print_live_monsters(alive_monsters)
    while True:
        command = input()

        if command is '?':
            pac_main_ooc()  # print available commands in the main loop when out of combat
        elif 'engage' in command:
            target = command[7:] # name of monster to engage

            if target in alive_monsters.keys():
                target = alive_monsters[target] # convert the string to a Monster object
                combat.engage_combat(main_character, target, alive_monsters)
        elif command == 'print alive monsters' or command == 'pav':
            print_live_monsters(alive_monsters)
        elif command == 'print all alive monsters':
            print_live_monsters(alive_monsters, print_all=True)


def load_monsters():
    """
    Reads the creature_template table to get information about all of the creatures in the game
    creature_template is of format:

    creature entry, creature name, level, hp, mana, min_dmg, max_dmg
                1, Zimbab       ,     1, 10,   10,       2,       4
    Creature Level: 1 Zimbab, HP: 10, MANA: 10, Damage: 2-4

    :return: A Dictionary: Key: Monster Name, Value: Object of class entities.py/Monster
    """
    # TODO: Move this somewhere else
    # TODO: Think of another approach rather than loading them all at once!
    # Maybe use a generator and read enough to fill the list with five monsters

    monsters_dict = {}
    print("Loading Monsters...")
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()
        creature_template_reader = cursor.execute("SELECT * FROM creature_template")
        for creature_info in creature_template_reader:
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
    print("Monsters loaded!")
    return monsters_dict


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