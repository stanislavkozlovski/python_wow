from entities import Character, Monster
from commands import pac_in_combat, get_available_paladin_abilities


def engage_combat(character: Character, monster: Monster, alive_monsters: dict, guid_name_set: set, monster_GUID: int):
    AVAILABLE_SPELLS = get_available_spells(character)  # Load all of the currently available spells for our character
    to_skip_attack = False  # Used when we don't want the monster to attack on the next turn
    character.enter_combat()
    monster.enter_combat()

    while character.in_combat:
        # we start off the combat with the monster dealing the first blow
        if not to_skip_attack:
            monster_attack(monster, character)
        else:
            to_skip_attack = False

        if not character.alive:
            alive_monsters[monster_GUID].leave_combat()
            print("{0} has slain character {1}".format(monster.name, character.name))

            character.prompt_revive()
            break

        command = input()

        while True:  # for commands that do not end the turn, like printing the stats or the possible commands
            if command == '?':
                pac_in_combat(character)  # print available commands
            elif command == 'print stats':
                print("Character {0} is at {1:.2f}/{2} health | {3}/{4} mana.".format(character.name, character.health, character.max_health, character.mana, character.max_mana))
                print("Monster {0} is at {1:.2f}/{2} health | {3}/{4} mana.".format(monster.name, monster.health, monster.max_health, monster.mana, monster.max_mana))
            elif command == 'print xp':
                print("{0}/{1} Experience. {2} needed to level up!".format(character.experience,
                                                                           character.xp_req_to_level,
                                                                           character.xp_req_to_level-character.experience))
            else:
                break
            command = input()

        if command == 'attack':
            character.attack(monster)
        elif command in AVAILABLE_SPELLS:
            if not character.spell_handler(command):
                # Unsuccessful cast
                to_skip_attack = True  # skip the next attack and load a command again

        if not monster.alive:
            print("{0} has slain {1}!".format(character.name, monster.name))
            character.award_monster_kill(monster=monster)
            character.leave_combat()  # will exit the loop
            del alive_monsters[monster_GUID]  # removes the monster from the dictionary
            guid_name_set.remove((monster_GUID, monster.name))  # remove it from the set used for looking up


def monster_attack(attacker: Monster, victim: Character):
    attacker_swing = attacker.deal_damage(victim.level)  # an integer representing the damage

    print("{0} attacks {1} for {2:.2f} damage!".format(attacker.name, victim.name, attacker_swing))

    victim.take_attack(attacker_swing)


#  returns a hashset with a list of allowed commands (you can't cast a spell you haven't learned yet)
def get_available_spells(character: Character):
    chr_class = character.get_class()
    available_spells = set()

    if chr_class == 'paladin':
        available_spells = get_available_paladin_abilities(character)  # this function is from commands.py

    return available_spells

