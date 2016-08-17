"""
This module will handle the player's commands
"""
from combat import engage_combat
from commands import pac_main_ooc, pac_map_directions


def handle_main_commands(main_character, available_quests: dict, map_directions, alive_npcs: dict,
                         npc_guid_name_set: set, alive_monsters: dict, guid_name_set: set, zone_object):
    command = input()
    if command is '?':
        pac_main_ooc()  # print available commands in the main loop when out of combat
    elif command == 'go to ?':
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
        map_directions = handle_go_to_command(command, main_character, zone_object, map_directions)
    elif command == 'print alive monsters' or command == 'pam':
        print_live_monsters(alive_monsters)
    elif command == 'print alive npcs' or command == 'pan':
        print_live_npcs(alive_npcs)
    elif command == 'print all alive monsters':
        print_live_monsters(alive_monsters, print_all=True)
    elif command == 'print all alive npcs':
        print_live_npcs(alive_npcs, print_all=True)

    return map_directions

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


def handle_go_to_command(command: str,  main_character, zone_object, map_directions: dict):
    destination = command[6:]

    temp_alive_monsters, temp_guid_name_set, temp_alive_npcs, temp_npc_guid_name_set, temp_available_quests, zone_is_valid = \
        zone_object.get_live_monsters_guid_name_set_and_quest_list(zone_object, destination)

    if zone_is_valid and destination in map_directions:
        # if the move has been successful

        alive_monsters, guid_name_set, alive_npcs, npc_guid_name_set, available_quests = (
            temp_alive_monsters, temp_guid_name_set, temp_alive_npcs, temp_npc_guid_name_set,
            temp_available_quests)

        main_character.current_subzone = destination
        # update map directions
        map_directions = zone_object.get_map_directions(zone_object, main_character.current_subzone)
        print("Moved to {0}".format(main_character.current_subzone))
        print_live_npcs(alive_npcs, print_all=True)
        print_live_monsters(alive_monsters)
    else:
        print("No such destination as {} that is connected to your current subzone.".format(destination))

    return map_directions  # return the new map directions

def print_live_monsters(alive_monsters: dict, print_all=False):
    print("Alive monsters: ")
    # sort them by level and print the five that are the lowest level
    sorted_list = sorted(alive_monsters.items(), key=lambda x: x[1].level)
    printed_monsters = 0
    for _, monster in sorted_list:
        print(monster)
        printed_monsters += 1

        if not print_all and printed_monsters == 5:  # print only five monsters at once
            break

    print()


def print_live_npcs(alive_npcs: dict, print_all=False):
    print("Alive NPCs: ")
    printed_npcs = 0

    for _, npc in alive_npcs.items():
        print(npc)
        printed_npcs += 1

        if not print_all and printed_npcs == 5:
            break

    print()


def print_available_quests(available_quests: dict, character_level: int):
    print("Available quests: ")

    for _, quest in available_quests.items():
        if quest.required_level <= character_level:  # print quests that the character has the required level for only!
            print("{quest_name} - Requires {required_kills} {monster_name} kills. Rewards {xp_reward} experience."
                  .format(quest_name=quest.name, required_kills=quest.required_kills,
                          monster_name=quest.monster_to_kill, xp_reward=quest.xp_reward))
