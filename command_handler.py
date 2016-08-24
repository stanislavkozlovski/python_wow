"""
This module will handle the player's commands
"""
from zones.zone import Zone
from commands import pac_main_ooc, pac_map_directions, pac_in_combat, pac_vendor_dialogue, pac_opened_inventory
from information_printer import (print_live_npcs, print_live_monsters,
                                 print_available_quests, print_in_combat_stats, print_character_xp_bar)



def handle_main_commands(main_character, zone_object):
    """
    Get a command from the player and if it's a valid command: run it.
    :param main_character: A Character class object. This is basically the player
    :param zone_object: A class object of Zone
    """
    command = input()
    if command is '?':
        pac_main_ooc()  # print available commands in the main loop when out of combat
    elif command == 'go to ?':
        pac_map_directions(possible_routes=zone_object.get_cs_map())
    elif command == 'print available quests' or command == 'paq':
        print_available_quests(available_quests=zone_object.get_cs_quests(), players_level=main_character.level)
    elif command == 'print quest log':
        main_character.print_quest_log()
    elif command == 'print inventory':
        main_character.print_inventory()
    elif command == "open inventory":
        handle_open_inventory_command(main_character)
    elif 'talk to' in command:
        handle_talk_to_command(command, main_character, zone_object)
    elif 'buy from' in command:
        handle_buy_from_command(command, main_character, zone_object)
    elif 'engage' in command:
        handle_engage_command(command, main_character, zone_object)
    elif 'accept' in command:  # accept the quest
        handle_accept_quest_command(command, main_character, available_quests=zone_object.get_cs_quests())
    elif 'go to' in command:
        handle_go_to_command(command, main_character, zone_object)
    elif command == 'print alive monsters' or command == 'pam':
        print_live_monsters(zone_object)
    elif command == 'print alive npcs' or command == 'pan':
        print_live_npcs(zone_object)
    elif command == 'print all alive monsters':
        print_live_monsters(zone_object, print_all=True)
    elif command == 'print all alive npcs':
        print_live_npcs(zone_object, print_all=True)


def handle_talk_to_command(command:str, character, zone_object: Zone):
    alive_npcs, guid_name_set = zone_object.get_cs_npcs()

    target = command[8:]  # name of NPC

    # return the guid for the npc we want to target, or None if there is no such one
    target_guid = get_guid_by_name(target, guid_name_set)


    # using the guid, target him from the alive_monsters dictionary
    if target_guid in alive_npcs.keys():
        target = alive_npcs[target_guid]
        target.talk(character.name)
    else:
        print("Could not find NPC {}.".format(target))


def handle_engage_command(command: str, character, zone_object: Zone):
    """
    This checks if there is a hostile monster with the name provided in the command.
    If there is, we engage in combat with him by going into the engage_combat function in the
    combat.py module.
    :param command: the player's command
    :param character: The player's character, a Character object
    :param zone_object: a Zone object from which we will get the monsters
    :return:
    """
    from combat import engage_combat

    alive_monsters, guid_name_set = zone_object.get_cs_monsters()
    target = command[7:]  # name of monster to engage

    # return the guid for the monster we want to target, or None if there is no such one
    target_guid = get_guid_by_name(target, guid_name_set)

    # using the guid, target him from the alive_monsters dictionary
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


def handle_buy_from_command(command: str, character, zone_object: Zone):
    """ check to see if there is such a vendor, if it is, go to the handle_vendor_sale function
        which initiates the while loop for browsing the vendor's inventory                      """
    target = command[9:]  # name of Vendor

    alive_npcs, guid_name_set  = zone_object.get_cs_npcs()

    # return the guid for the npc we want to target, or None if there is no such one
    target_guid = get_guid_by_name(target, guid_name_set)

    # using the guid, target him from the alive_monsters dictionary
    if target_guid in alive_npcs.keys():
        target = alive_npcs[target_guid]
        handle_vendor_sale(character, target)
    else:
        print("Could not find Vendor {}".format(target))


def handle_vendor_sale(character, vendor):
    while True:
        vendor.print_inventory()

        command = input()
        if command == 'exit':
            break
        elif 'buy ' in command:
            item = command[4:]  # name of the item
            if vendor.has_item(item):
                # check if the player has enough gold
                if character.has_enough_gold(vendor.get_item_price(item)):
                    character.buy_item(vendor.sell_item(item))
                    print("{character_name} has bought {item_name} from {vendor_name}!".format(
                        character_name=character.name, item_name=item, vendor_name=vendor.name
                    ))
                else:
                    print("You do not have enough gold to buy {}!\n".format(item))
            else:
                print("{} does not have {} in stock.".format(vendor.name, item))
        elif command == '?':
            pac_vendor_dialogue()


def handle_open_inventory_command(character):
    """
    This command opens the inventory of the character and lets him fiddle with the items there
    """
    character.print_inventory()

    while True:
        print(">inventory ", end='')
        command = input()
        if command == "?":
            pac_opened_inventory()
        elif command == "exit":
            print("-" * 40)
            break
        elif "equip" in command:
            """ Equips the item """
            item_name = command[6:]

            # failsafe check if the item is in the inventory of the player. if it's not it will return a None object,
            # which will not pass the if checks in the equip_item method
            item, _ = character.inventory.get(item_name, (None, None))

            character.equip_item(item)


def handle_go_to_command(command: str, character, zone_object: Zone):
    destination = command[6:]

    valid_move = zone_object.move_player(character.current_subzone, destination)

    if valid_move:
        # if the move has been successful
        character.current_subzone = destination

        # update _map directions
        print("Moved to {0}".format(character.current_subzone))
        print_live_npcs(zone_object, print_all=True)
        print_live_monsters(zone_object)
    else:
        print("No such destination as {} that is connected to your current subzone.".format(destination))


# IN COMBAT COMMANDS
# COMMANDS THAT DO NOT END THE TURN
def handle_in_combat_non_ending_turn_commands(command: str, character, monster) -> str:
    """
    This function is called whenever the player sends a command while in combat.
    We go through this while loop to check if the command is any of the ones supported below.
    If it is, we iterate through the loop and get a new command. We do the same check.
    If it is not one of the commands, we simply return the command as is.

    :param command: player's command
    :param character: Character object
    :param monster: Monster object
    :return:
    """
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


def get_guid_by_name(name: str, guid_name_set: set):
    """
    A function that returns a GUID which is associated with the given name,
    if there is no such one, return None
    :param name: The name of the creature you want to get a GUID of
    :return: the GUID you're searching for
    """
    # TODO: Move
    for guid, _name in guid_name_set:
        if _name == name:
            return guid

    return None





