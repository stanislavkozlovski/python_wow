from commands import pac_looting,get_available_paladin_abilities
from entities import Character, Monster
from command_handler import handle_in_combat_non_ending_turn_commands
from information_printer import print_loot_table


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
    will_end_turn = True  # Dictates if we are going to count the iteration of the loop as a turn

    character.enter_combat()
    monster.enter_combat()

    while character.is_in_combat():
        # We start off the combat with the monster dealing the first blow
        if not will_end_turn:  # skip attack if the turn has not ended
            # skip turn based things
            will_end_turn = True
        else:
            monster.start_turn_update()
            character.start_turn_update()

            if monster.is_alive():
                monster.attack(character)

        if not character.is_alive():
            monster.leave_combat()
            print("{0} has slain character {1}".format(monster.name, character.name))

            character.prompt_revive()
            break

        command = input()
        # check if the command does not end the turn, if it doesn't the same command gets returned
        command = handle_in_combat_non_ending_turn_commands(command, character, monster)

        if command == 'attack':
            character.attack(monster)
        elif command in available_spells:
            if not character.spell_handler(command):
                # Unsuccessful cast
                will_end_turn = False  # skip the next attack, don't count this iteration as a turn and load a command again

        if will_end_turn:
            monster.end_turn_update()
            character.end_turn_update()

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
    print_loot_table(monster.loot)
    while True:
        command = input()

        if "take" in command:
            item_name = command[5:]

            if item_name == "gold":
                gold = monster.give_loot("gold")

                if gold:  # if it's successful
                    character.award_gold(gold)
                    print("{char_name} has looted {gold_amount} gold.".format(char_name=character.name,
                                                                              gold_amount=gold))
            else:  # if we want to take an item
                item = monster.give_loot(item_name = item_name)

                if item:  # if the loot is successful
                    character.award_item(item=item)
                    print("{char_name} has looted {item_name}.".format(char_name=character.name,
                                                                       item_name=item_name))

            if not monster.loot:  # if the loot is empty, exit the loot window
                print('-' * 40)
                break

            print_loot_table(monster.loot)  # print the updated table each time we take something
        elif command == "?":
            pac_looting()
        elif command == "exit":  # end the looting process
            print('-' * 40)
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
