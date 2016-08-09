# TODO: Add command that shows all available commands
# TODO: Add list with last twenty prints, clear the console and rewrite again whenever a command has been added
# TODO: A million other things
"""
current commands:
attack - attacks the creature and ends the turn
print stats - prints your health and the monster's. does not end the turn
engage - start the fight
"""
import combat
from entities import Character, Monster
from items import Weapon
GAME_VERSION = '0.0.2.1 ALPHA'

def main():
    welcome_print()
    main_character = Character(name="Netherblood",
                               health=10,
                               mana=10,
                               strength=3)
    starter_weapon = Weapon(min_damage=1, max_damage=3)
    main_character.equip_weapon(starter_weapon)
    print("Character {0} created!".format(main_character.name))
    test_creature = Monster(name="Zimbab",
                            health=5,
                            mana=0,
                            level=1,
                            min_damage=1,
                            max_damage=3)
    alive_monsters = {test_creature.name: test_creature}
    while True:
        print_live_monsters(alive_monsters)

        command = input()
        if 'engage' in command:
            target = command.split()[1] # name of monster to engage

            if target in alive_monsters.keys():
                target = alive_monsters[target] # convert the string to a Monster object
                combat.engage_combat(main_character, target, alive_monsters)


def print_live_monsters(alive_monsters: dict):
    print("Alive monsters: ")

    for _, monster in alive_monsters.items():
        print(monster)

def welcome_print():
    print("WELCOME TO PYTHON WOW VERSION: {0}".format(GAME_VERSION))
    print("A simple console RPG game inspired by the Warcraft universe!")
    print()
if __name__ == '__main__':
    main()