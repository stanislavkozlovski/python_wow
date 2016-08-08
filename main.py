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
GAME_VERSION = '0.0.1 ALPHA'

def main():
    welcome_print()
    main_character = Character(name="Netherblood",
                               health=10,
                               mana=10,
                               strength=3)
    print("Character {0} created!".format(main_character.name))
    test_creature = Monster(name="Zimbab",
                            health=5,
                            mana=0,
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


class LivingThing:
    """
    This is the base class for all things alive - characters, monsters and etc.
    """
    def __init__(self, name: str, health: int=1, mana: int=1):
        self.name = name
        self.health = health
        self.max_health = health
        self.mana = mana
        self.max_mana = mana
        self.alive = True
        self.in_combat = False

    def is_alive(self):
        return self.alive

    def enter_combat(self):
        self.in_combat = True

    def leave_combat(self):
        self.in_combat = False

    def check_if_dead(self):
        if self.health <= 0:
            self.alive = False
            self.die()

    def die(self):
        pass


class Monster(LivingThing):
    def __init__(self, name: str, health: int=1, mana: int=1, min_damage: int=0, max_damage: int=1):
        super().__init__(name, health, mana)
        self.min_damage = min_damage
        self.max_damage = max_damage

    def __str__(self):
        return "Creature {0} - {1}/{2} HP | {3}/{4} Mana".format(self.name, self.health, self.max_health, self.mana, self.max_mana)

    def deal_damage(self):
        import random
        damage_to_deal = random.randint(self.min_damage, self.max_damage + 1)
        return damage_to_deal

    def take_attack(self, damage: int):
        self.health -= damage
        self.check_if_dead()

    def die(self):
        print("Creature {} has been slain!".format(self.name))

    def leave_combat(self):
        super().leave_combat()
        self.health = self.max_health # reset the health


class Weapon:
    def __init__(self, min_damage: int=0, max_damage: int=1):
        self.min_damage = min_damage
        self.max_damage = max_damage


class Character(LivingThing):
    def __init__(self, name: str, health: int=1, mana: int=1, strength: int=1):
        super().__init__(name, health, mana)
        self.strength = strength
        self.min_damage = 0
        self.max_damage = 1
        self.equipped_weapon = Weapon()

    def equip_weapon(self, weapon: Weapon):
        self.equipped_weapon = weapon
        self._calculate_damage(self.equipped_weapon)

    def _calculate_damage(self, weapon: Weapon):
        # current formula for damage is: wep_dmg * 0.1 * strength
        self.min_damage = weapon.min_damage * 0.1 * self.strength
        self.max_damage = weapon.max_damage * 0.1 * self.strength

    def deal_damage(self):
        import random
        damage_to_deal = random.randint(self.min_damage, self.max_damage + 1)
        return damage_to_deal

    def take_attack(self, damage: int):
        self.health -= damage
        self.check_if_dead()

    def die(self):
        print("Character {} has been slain!".format(self.name))


    def prompt_revive(self):
        print("Do you want to restart? Y/N")
        if input() in 'Yy':
            self.revive()
        else:
            exit()

    def revive(self):
        self.health = self.max_health
        self.alive = True


def welcome_print():
    print("WELCOME TO PYTHON WOW VERSION: {0}".format(GAME_VERSION))
    print("A simple console RPG game inspired by the Warcraft universe!")
    print()
if __name__ == '__main__':
    main()