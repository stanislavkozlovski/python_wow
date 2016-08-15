from commands import pac_in_combat, pac_looting,get_available_paladin_abilities
from entities import Character, Monster


def engage_combat(character: Character, monster: Monster, alive_monsters: dict, guid_name_set: set, monster_GUID: int):
    """
    This is where we handle the turn based combat of the game
    available_spells - set of string commands that enable our character to use the spells he has available.

    First we get both parties to enter combat. We start the loop and have the monster attack and
    immediately check if the character is not dead from the blow.
    If not, we take his command and if said command is one that does not end the turn (ie. wants to print some
    information about the fight) we enter an inner loop handling such commands and
    which continues to take commands until it gets one that does end the turn.
    We handle the command (which is most likely a spell or auto attack) and check if the monster is dead.
    :param character: the player
    :param monster: the monster that the player has attacked
    Parameters below are used solely to delete the monster from the dict & set once he's dead
    :param alive_monsters: Dictionary with the alive monsters in the subzone the player is in
    :param guid_name_set: Set which holds the name of each monster_GUID
    :param monster_GUID: The monster GUID
    """
    available_spells = get_available_spells(character)  # Load all of the currently available spells for our character
    to_skip_attack = False  # Used when we don't want the monster to attack on the next turn

    character.enter_combat()
    monster.enter_combat()

    while character.is_in_combat():
        # We start off the combat with the monster dealing the first blow
        if to_skip_attack:
            to_skip_attack = False
        else:
            monster.attack(character)

        if not character.is_alive():
            monster.leave_combat()
            print("{0} has slain character {1}".format(monster.name, character.name))

            character.prompt_revive()
            break

        command = input()

        while True:  # for commands that do not end the turn, like printing the stats or the possible commands
            if command == '?':
                pac_in_combat(character)  # print available commands
            elif command == 'print stats':
                print("Character {0} is at {1:.2f}/{2} health | {3}/{4} mana.".format(character.name, character.health,
                                                                                      character.max_health,
                                                                                      character.mana,
                                                                                      character.max_mana))
                print("Monster {0} is at {1:.2f}/{2} health | {3}/{4} mana.".format(monster.name, monster.health,
                                                                                    monster.max_health, monster.mana,
                                                                                    monster.max_mana))
            elif command == 'print xp':
                print("{0}/{1} Experience. {2} needed to level up!".format(character.experience,
                                                                           character.xp_req_to_level,
                                                                           character.xp_req_to_level - character.experience))
            else:
                break
            command = input()

        if command == 'attack':
            character.attack(monster)
        elif command in available_spells:
            if not character.spell_handler(command):
                # Unsuccessful cast
                to_skip_attack = True  # skip the next attack and load a command again

        if not monster.is_alive():
            print("{0} has slain {1}!".format(character.name, monster.name))

            character.award_monster_kill(monster=monster)
            character.leave_combat()  # will exit the loop

            del alive_monsters[monster_GUID]  # removes the monster from the dictionary
            guid_name_set.remove((monster_GUID, monster.name))  # remove it from the set used for looking up

            # handle loot
            handle_loot(character, monster)



def handle_loot(character: Character, monster: Monster):
    """ Display the loot dropped from the monster and listen for input if the player wants to take any"""
    # TODO: Make this work using a dictionary of items dropped and remove an item once it's taken, add the gold to it as well
    # TODO: Auto-exit the loot window once there is no more loot to be taken
    print()
    print("Loot dropped:")
    print("{} gold".format(monster.gold_to_give))
    gold_is_taken = False
    while True:
        command = input()

        if command == "take gold" and not gold_is_taken:
            print("{char_name} has looted {gold_amount} gold.".format(char_name=character.name,
                                                                      gold_amount=monster.gold_to_give))
            character.award_gold(gold=monster.gold_to_give)
            gold_is_taken = True
        elif command == "?":
            pac_looting()
        elif command == "exit":  # end the looting process
            break
        else:
            print("Invalid command.")


# returns a set with a list of allowed commands (you can't cast a spell you haven't learned yet)
def get_available_spells(character: Character):
    chr_class = character.get_class()
    available_spells = set()

    if chr_class == 'paladin':
        available_spells = get_available_paladin_abilities(character)  # this function is from commands.py

    return available_spells
