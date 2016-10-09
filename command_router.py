"""
This module will read the user's commands and route them to the appropriate handler for the given command in
command_handler.py
"""
import command_handler as ch


def route_main_commands(main_character, zone_object):
    """
    Get a command from the player and if it's a valid command: run it.
    :param main_character: A Character class object. This is basically the player
    :param zone_object: A class object of Zone
    """
    command = input()
    if command is '?':
        ch.handle_help_command()
    elif command == 'save':
        ch.handle_save_character_command()
    elif command == 'go to ?':
        ch.handle_go_to_help_command(zone_object)
    elif command == 'print available quests' or command == 'paq':
        ch.handle_paq_command()
    elif command == 'print quest log' or command == 'pql':
        ch.handle_pql_command(zone_object, main_character)
    elif command == 'print inventory':
        ch.handle_print_inventory_command(main_character)
    elif command == "open inventory":
        ch.handle_open_inventory_command(main_character)
    elif 'talk to' in command:
        ch.handle_talk_to_command(command, main_character, zone_object)
    elif 'buy from' in command:
        ch.handle_buy_from_command(command, main_character, zone_object)
    elif 'engage' in command:
        ch.handle_engage_command(command, main_character, zone_object)
    elif 'accept' in command:  # accept the quest
        ch.handle_accept_quest_command(command, main_character, available_quests=zone_object.get_cs_quests())
    elif 'go to' in command:
        ch.handle_go_to_command(command, main_character, zone_object)
    elif command == 'print alive monsters' or command == 'pam':
        ch.handle_pam_command(zone_object)
    elif command == 'print alive npcs' or command == 'pan':
        ch.handle_pan_command(zone_object)
    elif command == 'print all alive monsters':
        ch.handle_pam_command(zone_object, print_all=True)
    elif command == 'print all alive npcs':
        ch.handle_pan_command(zone_object, print_all=True)