"""
This module will handle the player's commands
"""
from zones.zone import Zone
from combat import engage_combat
from commands import pac_main_ooc, pac_map_directions, pac_in_combat
from information_printer import (print_live_npcs, print_live_monsters,
                                 print_available_quests, print_in_combat_stats, print_character_xp_bar)



def handle_main_commands(main_character, available_quests: dict, alive_npcs: dict,
                         npc_guid_name_set: set, alive_monsters: dict, guid_name_set: set, zone_object):
    """
    Get a command from the player and if it's a valid command: run it.
    :param main_character: A Character class object. This is basically the player
    :param available_quests: A Dictionary holding the available quests in this zone
    :param map_directions: A List holding the name of the zones we can access from our current sub zone
    :param alive_npcs: A Dictionary key: NPC_GUID, value: FriendlyNPC class object
    :param npc_guid_name_set: A Set of Tuples { (NPC_GUID, FriendlyNPC class object) }
    :param alive_monsters: A Dictionary key: Monster_GUID, value: Monster class object
    :param guid_name_set: A Set of Tuples { (Monster_GUID, Monster class object) }
    :param zone_object: A class object of Zone(not implemented yet, currently: ElwynnForest)
    """
    command = input()
    if command is '?':
        pac_main_ooc()  # print available commands in the main loop when out of combat
    elif command == 'go to ?':
        map_directions = zone_object.get_cs_map()

        pac_map_directions(possible_routes=map_directions)
    elif command == 'print available quests' or command == 'paq':
        print_available_quests(available_quests, main_character.level)
    elif command == 'print quest log':
        main_character.print_quest_log()
    elif command == 'print inventory':
        main_character.print_inventory()
    elif 'talk to' in command:
        handle_talk_to_command(command, main_character, alive_npcs, npc_guid_name_set)
    elif 'engage' in command:
        handle_engage_command(command, main_character, alive_monsters, guid_name_set)
    elif 'accept' in command:  # accept the quest
        handle_accept_quest_command(command, main_character, available_quests)
    elif 'go to' in command:
        handle_go_to_command(command, main_character, zone_object)
    elif command == 'print alive monsters' or command == 'pam':
        print_live_monsters(alive_monsters)
    elif command == 'print alive npcs' or command == 'pan':
        print_live_npcs(alive_npcs)
    elif command == 'print all alive monsters':
        print_live_monsters(alive_monsters, print_all=True)
    elif command == 'print all alive npcs':
        print_live_npcs(alive_npcs, print_all=True)


def handle_talk_to_command(command:str, character, alive_npcs: dict, guid_name_set: set):
    target = command[8:]  # name of NPC

    # return a list with the guids for each monster we've targeted and get the first guid [0]
    # using the guid, target him from the alive_monsters dictionary
    target_guid_list = [guid if name == target else None for guid, name in guid_name_set]
    if target_guid_list:
        target_guid = target_guid_list[0]
    else:  # if the list is empty
        target_guid = None

    if target_guid in alive_npcs.keys():
        target = alive_npcs[target_guid]
        target.talk(character.name)
    else:
        print("Could not find NPC {}.".format(target))


def handle_engage_command(command: str, character, alive_monsters: dict, guid_name_set: set):
    target = command[7:]  # name of monster to engage

    # return a list with the guids for each monster we've targeted and get the first guid [0]
    # using the guid, target him from the alive_monsters dictionary
    target_guid_list = [guid if name == target else None for guid, name in guid_name_set]
    if target_guid_list:
        target_guid = target_guid_list[0]
    else:  # if the list is empty
        target_guid = None

    if target_guid in alive_monsters.keys():
        target = alive_monsters[target_guid]  # convert the string to a Monster object
        engage_combat(character, target, alive_monsters, guid_name_set, target_guid)
    else:
        print("Could not find creature {}.".format(target))


def handle_accept_quest_command(command: str, character, available_quests: dict):
    quest_to_accept = command[7:]  # name of quest to accept

    if quest_to_accept in available_quests.keys():
        quest = available_quests[quest_to_accept]

        if character.level >= quest.required_level:
            print("Accepted Quest - {}".format(quest.name))
            character.add_quest(quest)
            del available_quests[quest_to_accept]  # removes it from the dictionary
        else:
            print("You need to be level {} to accept {}".format(quest.required_level, quest.name))

    else:
        print("No such quest.")


def handle_go_to_command(command: str,  main_character, zone_object: Zone):
    destination = command[6:]

    valid_move = zone_object.move_player(main_character.current_subzone, destination)

    if valid_move:
        # if the move has been successful
        alive_monsters, guid_name_set = zone_object.get_cs_monsters()
        alive_npcs, npc_guid_name_set = zone_object.get_cs_npcs()
        available_quests = zone_object.get_cs_quests()

        main_character.current_subzone = destination
        # update _map directions
        map_directions = zone_object.get_cs_map()
        print("Moved to {0}".format(main_character.current_subzone))
        print_live_npcs(alive_npcs, print_all=True)
        print_live_monsters(alive_monsters)
    else:
        print("No such destination as {} that is connected to your current subzone.".format(destination))

# IN COMBAT COMMANDS
# COMMANDS THAT DO NOT END THE TURN
def handle_in_combat_non_ending_turn_commands(command: str, character, monster) -> str:
    while True:  # for commands that do not end the turn, like printing the stats or the possible commands
        if command == '?':
            pac_in_combat(character)  # print available commands
        elif command == 'print stats':
            print_in_combat_stats(character, monster)
        elif command == 'print xp':
            print_character_xp_bar(character)
        else:
            return command
        command = input()





