"""
This module will handle the player's commands
"""
from zones.zone import Zone
from models.characters.saver import save_character
from commands import pac_main_ooc, pac_map_directions, pac_in_combat, pac_vendor_dialogue, pac_opened_inventory
from information_printer import (print_live_npcs, print_live_monsters, print_quest_item_choices,
                                 print_available_quests, print_in_combat_stats, print_character_xp_bar,
                                 print_character_equipment)
from constants import ZONE_MOVE_BLOCK_SPECIAL_KEY
from information_printer import print_quest_log, print_vendor_products_for_sale
# handlers here!


def handle_talk_to_command(command: str, character, zone_object: Zone):
    alive_npcs, guid_name_set = zone_object.get_cs_npcs()

    target = command[8:]  # name of NPC

    # return the guid for the npc we want to target, or None if there is no such one
    target_guid = get_guid_by_name(target, guid_name_set)

    # using the guid, target him from the alive_monsters dictionary
    if target_guid in alive_npcs.keys():
        target = alive_npcs[target_guid]
        target.talk(character.name)
    else:
        print(f'Could not find NPC {target}.')


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
        print(f'Could not find creature {target}.')


def handle_accept_quest_command(command: str, character, available_quests: dict):
    quest_to_accept = command[7:]  # name of quest to accept

    if quest_to_accept in available_quests.keys():
        quest = available_quests[quest_to_accept]

        if character.level >= quest.required_level:
            print(f'Accepted Quest - {quest.name}')
            character.add_quest(quest)
            del available_quests[quest_to_accept]  # removes it from the dictionary
        else:
            print(f'You need to be level {quest.required_level} to accept {quest.name}')

    else:
        print("No such quest.")


def handle_buy_from_command(command: str, character, zone_object: Zone):
    """ check to see if there is such a vendor, if it is, go to the handle_vendor_sale function
        which initiates the while loop for browsing the vendor's inventory                      """
    target = command[9:]  # name of Vendor

    alive_npcs, guid_name_set = zone_object.get_cs_npcs()

    # return the guid for the npc we want to target, or None if there is no such one
    target_guid = get_guid_by_name(target, guid_name_set)

    # using the guid, target him from the alive_monsters dictionary
    if target_guid in alive_npcs.keys():
        target = alive_npcs[target_guid]
        handle_vendor_sale(character, target)
    else:
        print(f'Could not find Vendor {target}')


def handle_vendor_sale(character, vendor):
    while True:
        print_vendor_products_for_sale(vendor_name=vendor.name, vendor_inventory=vendor.inventory)

        command = input()
        if command == 'exit':
            break
        elif 'buy ' in command:
            item = command[4:]  # name of the item
            if not vendor.has_item(item):
                print(f'{vendor.name} does not have {item} in stock.')
                continue

            # check if the player has enough gold
            if not character.has_enough_gold(vendor.get_item_price(item)):
                print(f'You do not have enough gold to buy {item}!\n')
                continue

            character.buy_item(vendor.sell_item(item))
            print(f'{character.name} has bought {item} from {vendor.name}!')
        elif 'sell ' in command:
            item = command[5:]  # name of the item
            if character.has_item(item):
                character.sell_item(item)
        elif 'info' in command:
            item_name = command[:-5]  # name of item

            item = vendor.get_item_info(item_name)

            print("\t", item, "\n") if item else None
        elif command == '?':
            pac_vendor_dialogue()


def handle_open_inventory_command(character):
    """
    This command opens the inventory of the character and lets him fiddle with the items there
    """
    character.print_inventory()

    while True:
        command = input(">inventory ")
        to_print = True

        if command == "?":
            pac_opened_inventory()
            to_print = False
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
        elif "use" in command:
            """ Consumes a consumable item"""
            item_name = command[4:]

            # failsafe check if the item is in the inventory of the player. if it's not it will return a None object,
            # which will not pass the if checks in the consume_item method
            item, _ = character.inventory.get(item_name, (None, None))

            character.consume_item(item)

        if to_print:  # we've tried to modify the inventory in some way
            """ item and item_name are assigned if we manage to pass this if check """
            if item:
                # we've modified the inventory (consumed/equipped an item)
                character.print_inventory()
            else:
                # we've tried to modify the inventory but unsuccessfuly, therefore item is None
                print(f'{item_name} is not in your inventory.')


def handle_go_to_command(command: str, character, zone_object: Zone):
    destination = command[6:]

    """
    move_player will usually return a boolean if we can initiate the move or not.
    However, there's a special case: If it returns SPECIAL_ZONE_BLOCK_KEY,
    it means that we cannot initiate the move and that the printing is handled by the method itself.
    """
    valid_move = zone_object.move_player(character.current_subzone, destination, character)

    if valid_move == ZONE_MOVE_BLOCK_SPECIAL_KEY:
        return
    if valid_move:
        # if the move has been successful
        character.current_subzone = destination

        # update _map directions
        print(f'Moved to {character.current_subzone}')

        zone_object.engage_zone_entered_script(character)  # engage a script if there is one

        print_live_npcs(zone_object, print_all=True)
        print_live_monsters(zone_object)
    else:
        print(f'No such destination as {destination} that is connected to your current subzone.')


def handle_quest_item_choice(item_rewards: dict):
    """
    This function opens a window where the player selects which item he wants to take from the quest
    :param item_rewards: a dictionary key: item name, value: instance of class Item
    :return: an instance of Item (the item object the player selected)
    """
    print_quest_item_choices(item_rewards)

    while True:
        command = input()

        if "choose" in command:
            """ Takes the item the player chooses """
            item_name = command[7:]

            if item_name in item_rewards.keys():
                return item_rewards[item_name]
            else:
                print("No such item as ", item_name)
        elif command == "?":
            print("Available commands:")
            print("\tchoose [Item Name]")
            print("\t\tTakes the item\n")


def handle_save_character_command(main_character):
    """ this function handles the 'save' command"""
    save_character(main_character)


def handle_help_command():
    """ this function handles the '?' command, displaying the user with all his possible commands"""
    pac_main_ooc()  # print available commands in the main loop when out of combat


def handle_go_to_help_command(zone_object):
    """ this function handles the 'go to ?' command, displaying the user with all the possible routes he can take"""
    pac_map_directions(possible_routes=zone_object.get_cs_map())


def handle_paq_command(zone_object, main_character):
    """ this function handles the 'print available quests' or 'paq' command, showing the player all the quests
    he is eligible to take """
    print_available_quests(available_quests=zone_object.get_cs_quests(), players_level=main_character.level)


def handle_pql_command(main_character):
    """ this function handles the 'print quest log' or 'pql' command, showing the player all the quests he is
    currently on """
    print_quest_log(main_character.quest_log)


def handle_print_inventory_command(main_character):
    """ this function handles the 'print inventory' command, showing the player's inventory """
    main_character.print_inventory()


def handle_print_equipment_command(main_character):
    """ this function handles the 'print equipment' command, showing the player's equipment """
    print_character_equipment(main_character.equipment)


def handle_pam_command(zone_object, print_all: bool=False):
    """
    this function handles the 'print alive monsters' or 'pam' command, showing the player all the
    live creatures in his current zone
    :param print_all: on a default print, we print only 5 alive monsters. If we want to print all of the live monsters
    in the current zone, this boolean muut be set to True
    """
    print_live_monsters(zone_object, print_all)


def handle_pan_command(zone_object, print_all: bool=False):
    """
    this function handles the 'print alive npcs' or 'pan' command, showing the player all the live NPCs
    in his current zone
    :param print_all: on a default print, we print only 5 alive NPCs. If we want to print all of the live monsters
    in the current zone, this boolean must be set to True
    """
    print_live_npcs(zone_object, print_all)


# IN COMBAT COMMANDS
# COMMANDS THAT DO NOT END THE TURN
def handle_combat_help_command(character):
    """ this function handles the '?' command when it is entered in combat, displaying the player's
    available commands """
    pac_in_combat(character)  # print available commands


def handle_combat_print_stats_command(character, monster):
    """
    this function handles the 'print stats' command, showing the stats of the player and the monster he's fighting
    while in combat.
    """
    print_in_combat_stats(character, monster)


def handle_combat_print_xp_command(character):
    """ this function handles the 'print xp' command, showing the player's current experience bar while in combat """
    print_character_xp_bar(character)


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





