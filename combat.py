from main import Character, Monster


def engage_combat(character: Character, monster: Monster, alive_monsters: list):

    character.enter_combat()
    monster.enter_combat()

    while character.in_combat:
        # we start off the combat with the monster dealing the first blow
        monster_attack(monster, character)

        command = input()

        while True:  # for commands that do not end the turn, like printing the stats or the possible commands
            if command == 'print stats':
                print("Character {0} is at {1}/{2} health.".format(character.name, character.health, character.max_health))
                print("Monster {0} is at {1}/{2} health".format(monster.name, monster.health, monster.max_health))
                command = input()
            else:
                break

        if command == 'attack':
            character_attack(character, monster)

        if not monster.alive:
            character.leave_combat()  # will exit the loop
            alive_monsters.remove(monster)
            print("{0} has slain {1}".format(character.name, monster.name))


def monster_attack(attacker: Monster, victim: Character):
    attacker_swing = attacker.deal_damage()  # an integer representing the damage

    victim.take_attack(attacker_swing)

    print("{0} attacks {1} for {2} damage!".format(attacker.name, victim.name, attacker_swing))


def character_attack(attacker: Character, victim: Monster):
    attacker_swing = attacker.deal_damage()

    victim.take_attack(attacker_swing)

    print("{0} attacks {1} for {2} damage!".format(attacker.name, victim.name, attacker_swing))