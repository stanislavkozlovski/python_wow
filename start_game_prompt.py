"""
This module is called on game startup and asks the user if he wants to create a new character or load an old one
"""
from entities import Character


def get_player_character() -> Character:
    """
    This is the main function of this module. It lets the user choose between loading a character or creating a new one,
    after the selected option is finished, we return the Character object.
    :return: The Character object that the player is going to play as
    """
    choice = get_choice()  # type: str

    if choice == 'load':
        # load a character from the DB
        pass
    elif choice == 'new':
        # create a new character
        pass


def get_choice() -> str:
    print("*"*50)
    print("Would you like to create a new character or load an already existing character?")
    print("To create a new character, type \tnew\t and to load an already existing one, type \tload\t")

    choice = input()

    while choice not in ['load', 'new']:
        print("{} is not a valid command.".format(choice))
        choice = input()
