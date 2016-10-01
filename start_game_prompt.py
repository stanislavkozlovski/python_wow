"""
This module is called on game startup and asks the user if he wants to create a new character or load an old one
"""
from termcolor import colored

from entities import Character
from loader import load_saved_character
from exceptions import NoSuchCharacterError


def get_player_character() -> Character:
    """
    This is the main function of this module. It lets the user choose between loading a character or creating a new one,
    after the selected option is finished, we return the Character object.
    :return: The Character object that the player is going to play as
    """
    character = None  # the variable that will hold the character
    choice = get_choice()  # type: str

    if choice == 'load':
        # load a character from the DB
        character = handle_load_character()
    elif choice == 'new':
        # create a new character
        pass

    return character


def handle_load_character() -> Character:
    """ this function loads a character from the DB """
    print("You've chosen to load an existing character, please enter the name of the character you want to load: ")
    character_name = input()

    try:
        character = load_saved_character(character_name)
    except NoSuchCharacterError:
        print(colored("!" * 50, 'red'))
        print(colored("A character with the name {} does not exist in the database!", 'red'))
        print(colored("!" * 50, 'red'))

        character = get_player_character()  # go back and read input again

    return character


def get_choice() -> str:
    print("*"*50)
    print("Would you like to create a new character or load an already existing character?")
    print("To create a new character, type \tnew\t and to load an already existing one, type \tload\t")

    choice = input()

    while choice not in ['load', 'new']:
        print("{} is not a valid command.".format(choice))
        choice = input()

    return choice