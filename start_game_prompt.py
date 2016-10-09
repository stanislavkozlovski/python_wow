"""
This module is called on game startup and asks the user if he wants to create a new character or load an old one
"""
from termcolor import colored

from entities import Character
from classes import Paladin
from information_printer import print_available_character_classes
from loader import load_saved_character
from exceptions import NoSuchCharacterError

AVAILABLE_CLASSES = ['paladin']

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
        character = handle_create_character()

    return character


def handle_create_character() -> Character:
    """ this function handles the creation of a new character"""
    # 1. Choose class
    print("You've chosen to create a new character, please pick a class from the list of available classes: ")
    print_available_character_classes()
    class_choice = str.lower(input())

    while class_choice not in AVAILABLE_CLASSES:  # check for valid class
        print("{} is not a valid class!\n".format(class_choice))
        class_choice = str.lower(input())

    # 2. Choose name
    print("\nYou've chosen to create a {class_}! Nice going, now pick a name for our {class_}."
          .format(class_=class_choice))

    # TODO: Format name ex: NeThErBlOOD => Netherblood
    character_name = input()

    while len(character_name) > 20:  # check for valid name
        print("Your name cannot be longer than 20 characters.")
        character_name = input()

    # 3. Create the character object
    if class_choice == 'paladin':
        character = Paladin(name=character_name)

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
    new_colored = colored('new', color='magenta')
    load_colored = colored('load', color='magenta')
    print("*"*50)
    print("Would you like to create a new character or load an already existing character?")
    print("To create a new character, type {new} and to load an already existing one, type {load}"
          .format(new=new_colored, load=load_colored))

    choice = input()

    while choice not in ['load', 'new']:
        print("{} is not a valid command.".format(choice))
        choice = input()

    return choice