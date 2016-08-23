import sqlite3

from database_info import \
    (DB_PATH, DBINDEX_CREATURES_GUID, DBINDEX_CREATURES_CREATURE_ID,

     DBINDEX_CREATURE_TEMPLATE_NAME, DBINDEX_CREATURE_TEMPLATE_LEVEL,
     DBINDEX_CREATURE_TEMPLATE_HEALTH, DBINDEX_CREATURE_TEMPLATE_MANA,
     DBINDEX_CREATURE_TEMPLATE_MIN_DMG, DBINDEX_CREATURE_TEMPLATE_MAX_DMG,
     DBINDEX_CREATURE_TEMPLATE_QUEST_RELATION_ID, DBINDEX_CREATURE_TEMPLATE_LOOT_TABLE_ID,
     DBINDEX_CREATURE_TEMPLATE_GOSSIP, DBINDEX_CREATURE_TEMPLATE_ENTRY, DBINDEX_CREATURE_TEMPLATE_TYPE,

     DBINDEX_NPC_VENDOR_ITEM_COUNT, DBINDEX_NPC_VENDOR_ITEM_ID, DBINDEX_NPC_VENDOR_PRICE,

     DBINDEX_ITEM_TEMPLATE_NAME, DBINDEX_ITEM_TEMPLATE_TYPE, DBINDEX_ITEM_TEMPLATE_BUY_PRICE,
     DBINDEX_ITEM_TEMPLATE_SELL_PRICE, DBINDEX_ITEM_TEMPLATE_MIN_DMG, DBINDEX_ITEM_TEMPLATE_MAX_DMG,

     DBINDEX_QUEST_TEMPLATE_ENTRY, DBINDEX_QUEST_TEMPLATE_NAME, DBINDEX_QUEST_TEMPLATE_TYPE,
     DBINDEX_QUEST_TEMPLATE_LEVEL_REQUIRED, DBINDEX_QUEST_TEMPLATE_MONSTER_REQUIRED,
     DBINDEX_QUEST_TEMPLATE_AMOUNT_REQUIRED, DBINDEX_QUEST_TEMPLATE_XP_REWARD,

     DBINDEX_CREATURE_DEFAULT_XP_REWARDS_LEVEL, DBINDEX_CREATURE_DEFAULT_XP_REWARDS_XP,

     DBINDEX_CREATURE_DEFAULT_GOLD_REWARDS_LEVEL, DBINDEX_CREATURE_DEFAULT_GOLD_REWARDS_MIN_GOLD_REWARD,
     DBINDEX_CREATURE_DEFAULT_GOLD_REWARDS_MAX_GOLD_REWARD,

     DBINDEX_LEVELUP_STATS_LEVEL, DBINDEX_LEVELUP_STATS_HEALTH, DBINDEX_LEVELUP_STATS_MANA,
     DBINDEX_LEVELUP_STATS_STRENGTH, DBINDEX_LEVELUP_STATS_ARMOR,

     DBINDEX_LEVEL_XP_REQUIREMENT_LEVEL, DBINDEX_LEVEL_XP_REQUIREMENT_XP_REQUIRED
     )
from quest import KillQuest
import items


def load_monsters(zone: str, subzone: str) -> tuple:
    """
        Gets a query from the creatures table to load all hostile creatures in our current zone

        guid, creature_id,       type,             zone,          subzone
           1,          11,  'monster',    Elwynn Forest, Northshire Abbey

        Then, with each guid queries up the creature information from creatures_template and
         creates a Monster object in a dictionary has GUID as a key and the monster as the value
        Key: 1, Value: Monster(....)

        creature_template table is as follows:

        creature entry, creature name,      type,   level, hp, mana, min_dmg, max_dmg, quest_relation_ID, loot_table,ID,      gossip
                    1, Zimbab       ,   "monster"       1, 10,   10,       2,       4                  1,             1, "Hey there"

        type is "monster" meaning this is a hostile NPC
        Creature Level: 1 Zimbab, HP: 10, MANA: 10, Damage: 2-4.
        He is needed to complete quest with ID 1 and the loot he drops is from the row in the loot_table DB table with
        entry 1. If talking to him is enabled, he would say "Hey there".


        :return: A Dictionary: Key: guid, Value: Object of class entities.py/Monster,
                 A Set of Tuples ((Monster GUID, Monster Name))
    """
    from entities import Monster  # needed to be imported here otherwise we end up in an import loop

    monsters_dict = {}
    guid_name_set = set()

    print("Loading Monsters...")
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()
        creatures_reader = cursor.execute("SELECT * FROM creatures WHERE type = ? AND zone = ? AND sub_zone = ?"
                                          , ["monster", zone, subzone])  # query all the creatures in our location :)

        for creature_info in creatures_reader.fetchall():
            creature_guid = creature_info[DBINDEX_CREATURES_GUID]  # type: int
            creature_id = creature_info[DBINDEX_CREATURES_CREATURE_ID]  # type: int

            # This will currently run a query for every monster, meaning if there are 20 of the exact same monsters,
            # 20 queries will be run. There isn't much sense in that, so:
            # TODO: Modify so we don't run unecessary queries for monster info that we've already loaded from the DB
            creature_template_reader = cursor.execute("SELECT * FROM creature_template WHERE type = ? AND entry = ?",
                                                      ["monster",creature_id])
            creature_template_info = creature_template_reader.fetchone()  # entry is unique meaning the query will-
            # always return one monster

            # save the creature values
            # )
            creature_template_name = creature_template_info[DBINDEX_CREATURE_TEMPLATE_NAME]
            creature_template_level = creature_template_info[DBINDEX_CREATURE_TEMPLATE_LEVEL]  # type: int
            creature_template_health = creature_template_info[DBINDEX_CREATURE_TEMPLATE_HEALTH]  # type: int
            creature_template_mana = creature_template_info[DBINDEX_CREATURE_TEMPLATE_MANA]  # type: int
            creature_template_min_dmg = creature_template_info[DBINDEX_CREATURE_TEMPLATE_MIN_DMG]  # type: int
            creature_template_max_dmg = creature_template_info[DBINDEX_CREATURE_TEMPLATE_MAX_DMG]  # type: int

            creature_template_quest_relation_ID = (
            creature_template_info[DBINDEX_CREATURE_TEMPLATE_QUEST_RELATION_ID]  # type: int
            if not creature_template_info[DBINDEX_CREATURE_TEMPLATE_QUEST_RELATION_ID] is None else -1)

            creature_template_loot_table_ID = (
            creature_template_info[DBINDEX_CREATURE_TEMPLATE_LOOT_TABLE_ID]  # type: int
            if not creature_template_info[DBINDEX_CREATURE_TEMPLATE_LOOT_TABLE_ID] is None else -1)

            # save into the set
            guid_name_set.add((creature_guid, creature_template_name))
            # save into the dict
            monsters_dict[creature_guid] = Monster(monster_id=creature_id,
                                                   name=creature_template_name,
                                                   health=creature_template_health,
                                                   mana=creature_template_mana,
                                                   level=creature_template_level,
                                                   min_damage=creature_template_min_dmg,
                                                   max_damage=creature_template_max_dmg,
                                                   quest_relation_id=creature_template_quest_relation_ID,
                                                   loot_table_ID=creature_template_loot_table_ID)



    print("Monsters loaded!")
    return monsters_dict, guid_name_set


def load_npcs(zone: str, subzone: str) -> tuple:
    """
        Gets a query from the creatures table to load all friendly creatures in our current zone
        Supported types are: "fnpc" - just a normal gossip npc and "vendor" - a vendor of items

        guid, creature_id,       type,             zone,          subzone
           1,          11,  'fnpc',    Elwynn Forest, Northshire Abbey

        Then, with each guid queries up the creature information from creatures_template and
         creates a Monster object in a dictionary has GUID as a key and the monster as the value
        Key: 1, Value: Monster(....)

        creature_template table is as follows:

        creature entry, creature name,      type,   level, hp, mana, min_dmg, max_dmg, quest_relation_ID, loot_table,ID,      gossip
                    1, Zimbab       ,    "fnpc" ,      1, 10,   10,       2,       4                  0,             0, "Hey there $N"

        type is "fnpc" meaning this is a Friendly NPC
        Creature Level: 1 Zimbab, HP: 10, MANA: 10, Damage: 2-4.
        If the player talks to him, he would say "Hey there (player_name" ($N is placeholder for the player's name)


        :return: A Dictionary: Key: guid, Value: Object of class entities.py/FriendlyNPC,
                 A Set of Tuples ((npc GUID, npc Name))
    """
    from entities import FriendlyNPC  # needed to be imported here otherwise we end up in an import loop
    from entities import VendorNPC

    npcs_dict = {}
    guid_name_set = set()

    print("Loading Friendly NPCs...")
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()
        fnpc_reader = cursor.execute("SELECT * FROM creatures WHERE (type = ? OR type = ?) AND zone = ? AND sub_zone = ?"
                                          , ["fnpc", "vendor", zone, subzone])  # query all the creatures in our location :)

        for creature_info in fnpc_reader.fetchall():
            creature_guid = creature_info[DBINDEX_CREATURES_GUID]  # type: int
            creature_id = creature_info[DBINDEX_CREATURES_CREATURE_ID]  # type: int

            # This will currently run a query for every fnpc, meaning if there are 20 of the exact same npcs,
            # 20 queries will be run. There isn't much sense in that, so:
            # TODO: Modify so we don't run unecessary queries for fnpc info that we've already loaded from the DB
            creature_template_reader = cursor.execute("SELECT * FROM creature_template WHERE (type = ? OR type = ?) AND entry = ?",
                                                      ["fnpc", "vendor", creature_id])
            creature_template_info = creature_template_reader.fetchone()  # entry is unique meaning the query will-
            # always return one npc

            # save the creature values
            creature_template_entry = creature_template_info[DBINDEX_CREATURE_TEMPLATE_ENTRY]  # type: int
            creature_template_name = creature_template_info[DBINDEX_CREATURE_TEMPLATE_NAME]
            creature_template_type = creature_template_info[DBINDEX_CREATURE_TEMPLATE_TYPE]
            creature_template_level = creature_template_info[DBINDEX_CREATURE_TEMPLATE_LEVEL]  # type: int
            creature_template_health = creature_template_info[DBINDEX_CREATURE_TEMPLATE_HEALTH]  # type: int
            creature_template_mana = creature_template_info[DBINDEX_CREATURE_TEMPLATE_MANA]  # type: int
            creature_template_min_dmg = creature_template_info[DBINDEX_CREATURE_TEMPLATE_MIN_DMG]  # type: int
            creature_template_max_dmg = creature_template_info[DBINDEX_CREATURE_TEMPLATE_MAX_DMG]  # type: int

            creature_template_quest_relation_ID = (
            creature_template_info[DBINDEX_CREATURE_TEMPLATE_QUEST_RELATION_ID]  # type: int
            if not creature_template_info[DBINDEX_CREATURE_TEMPLATE_QUEST_RELATION_ID] is None else -1)

            creature_template_loot_table_ID = (
            creature_template_info[DBINDEX_CREATURE_TEMPLATE_LOOT_TABLE_ID]  # type: int
            if not creature_template_info[DBINDEX_CREATURE_TEMPLATE_LOOT_TABLE_ID] is None else -1)

            creature_template_gossip = creature_template_info[DBINDEX_CREATURE_TEMPLATE_GOSSIP]

            # save into the set
            guid_name_set.add((creature_guid, creature_template_name))
            # save into the dict
            if creature_template_type == "fnpc":
                npcs_dict[creature_guid] = FriendlyNPC(name=creature_template_name, health=creature_template_health,
                                                       mana=creature_template_mana, level=creature_template_level,
                                                       min_damage=creature_template_min_dmg,
                                                       max_damage=creature_template_max_dmg,
                                                       quest_relation_id=creature_template_quest_relation_ID,
                                                       loot_table_ID=creature_template_loot_table_ID,
                                                       gossip=creature_template_gossip)

            elif creature_template_type == "vendor":
                npcs_dict[creature_guid] = VendorNPC(name=creature_template_name, entry=creature_template_entry,
                                                     health=creature_template_health,
                                                     mana=creature_template_mana, level=creature_template_level,
                                                     min_damage=creature_template_min_dmg,
                                                     max_damage=creature_template_max_dmg,
                                                     quest_relation_id=creature_template_quest_relation_ID,
                                                     loot_table_ID=creature_template_loot_table_ID,
                                                     gossip=creature_template_gossip
                                                     )
    print("Friendly NPCs loaded!")
    return npcs_dict, guid_name_set


def load_quests(zone: str, subzone:str) -> list:
    """
    Gets a query from the quest_template table to load all the quests in our current zone.
    Table is as follows:
entry,            name,    type, required_level,           monster_required,  amount_required,         zone,
    1, A Canine Menace,killquest              1,      (name of monster)Wolf,               10,Elwynn Forest,
          sub_zone,xp_reward, comment
 Northshire Valley,      300, Our First Quest!

    Type decides what kind of quests it is.
    Using the parameters, we run a query through quest_template to get all the quests that are for our zone

    :param zone: The zone that the query will use
    :param subzone: The subzone that the query will use
    :return: A Dctionary Key: Quest Name Value: Quest Object
    """

    quest_list = {}

    # populate list
    print("Loading Quests...")
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()
        quests_reader = cursor.execute("SELECT * FROM quest_template WHERE zone = ? AND sub_zone = ?", [zone, subzone])

        for row in quests_reader.fetchall():
            # save the quest information we'll need
            quest_entry = row[DBINDEX_QUEST_TEMPLATE_ENTRY]  # type: int
            quest_name = row[DBINDEX_QUEST_TEMPLATE_NAME]
            quest_type = row[DBINDEX_QUEST_TEMPLATE_TYPE]  #  type: str
            quest_level_requirement = row[DBINDEX_QUEST_TEMPLATE_LEVEL_REQUIRED]  # type: int
            quest_monster_required = row[DBINDEX_QUEST_TEMPLATE_MONSTER_REQUIRED]  # monster name
            quest_monster_kill_amount_required = row[DBINDEX_QUEST_TEMPLATE_AMOUNT_REQUIRED]  # type: int
            quest_xp_reward = row[DBINDEX_QUEST_TEMPLATE_XP_REWARD]  # type: int

            #  create the quest object according to it's type
            if quest_type == "killquest":
                quest_list[quest_name] = KillQuest(quest_name=quest_name,
                                                   quest_id=quest_entry,
                                                   required_monster=quest_monster_required,
                                                   required_kills=quest_monster_kill_amount_required,
                                                   xp_reward=quest_xp_reward,
                                                   level_required=quest_level_requirement)

    return quest_list


def load_creature_xp_rewards() -> dict:
    """
    Load the default XP that is to be given from the creature.
    The table's contents are as follows:
    Entry, Level, Experience to give
    1,         1,     50 Meaning a creature that is level 1 will give 50 XP
    2,         2,     75 Gives 75 XP
    etc...

    :return: A dictionary as follows: Key: Level, Value: XP Reward
                                               1,               50
    """

    xp_reward_dict = {}

    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()
        def_xp_rewards_reader = cursor.execute("SELECT * FROM creature_default_xp_rewards")

        for line in def_xp_rewards_reader:
            level = line[DBINDEX_CREATURE_DEFAULT_XP_REWARDS_LEVEL]  # type: int
            xp_reward = line[DBINDEX_CREATURE_DEFAULT_XP_REWARDS_XP]  # type: int

            xp_reward_dict[level] = xp_reward

    return xp_reward_dict


def load_creature_gold_reward() -> dict:
    """
    Load the default gold amount that is to be given from the creature according to it's level.
    The creature_default_gold_reward table's contents are as follows:
    creature_level, min_gold_reward, max_gold_reward
                 1,               2,              5 Meaning a creature of level 1 will drop from 2 to 5 gold

    :return: A dictionary - Key: Level(int), Value: Tuple(min_gold(int), max_gold(int))
                                     1,                 (2,5)
    """

    gold_rewards_dict = {}

    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()
        gold_rewards_reader = cursor.execute("SELECT * FROM creature_default_gold_rewards")

        for line in gold_rewards_reader:
            level = line[DBINDEX_CREATURE_DEFAULT_GOLD_REWARDS_LEVEL]  # type: int
            min_gold_reward = line[DBINDEX_CREATURE_DEFAULT_GOLD_REWARDS_MIN_GOLD_REWARD]  # type: int
            max_gold_reward = line[DBINDEX_CREATURE_DEFAULT_GOLD_REWARDS_MAX_GOLD_REWARD]  # type: int

            gold_rewards_dict[level] = (min_gold_reward, max_gold_reward)

    return gold_rewards_dict

def load_vendor_inventory(creature_entry: int) -> dict:
    """
    This function loads all the items that a certain vendor should sell.
    We take them from the npc_vendor DB table, whose contents are as follows:

    creature_entry - the entry of the vendor in creature_template
    item_id - the ID of the item that he's supposed to sell
    item_count - the count of items he sell at once
    price - The price in gold. By default we use the Item's item.buy_price variable in it's class.
    However, if this is set to something we override the price. Example:
        creature_entry, item_id, item_count, price
                13,       1,          5,    10
    The NPC whose entry is 13, sells the item with ID 1, 5 at a time for 10 gold.
    He sells the whole 5 items for 10 gold. He cannot sell 1,2,3 or 4 items, only 5.

    :param creature_entry: The DB entry of the npc in the creature_template table
    :return: A dictionary of Key: "Item Name", Value: Tuple(1,2)
                                                            1 - Item object of class Item from items.py
                                                            2 - The count of the item
    """
    vendor_inventory = {}

    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()

        npc_vendor_reader = cursor.execute("SELECT * FROM npc_vendor WHERE creature_entry = ?", [creature_entry])

        for npc_vendor_info in npc_vendor_reader:
            item_id = npc_vendor_info[DBINDEX_NPC_VENDOR_ITEM_ID]
            item_count = npc_vendor_info[DBINDEX_NPC_VENDOR_ITEM_COUNT]
            price = npc_vendor_info[DBINDEX_NPC_VENDOR_PRICE]

            item = load_item(item_id)  # type: Item

            if price: # check if there is anything set to price that'll make us override
                item.buy_price = price

            vendor_inventory[item.name] = (item, item_count)

    return vendor_inventory


def load_loot_table(monster_loot_table_ID: int):
    """
    Load the loot table of a specific monster
    entry, item1_ID, item1_chance, item2_ID, item2_chance, item3_ID, item3_chance, ... item20_ID, item20_chance
        1,       4,            55,        3,         30,          0,            0,             0,            0
    Meaning a creature whose col loot_table_ID from creature_template is equal to 1 has:
    55% chance to drop Item with ID 4
    30% chance to drop Item with ID 3
    Does not drop any more items, because the rest of the rows are 0s.

    :return: A List of Tuples, holding each item's ID and drop chance.
    Example: [ (4,55), (3,30) ] would be the list for our table row up there
    """
    # TODO: Maybe load all of the loot table into a dictionary and store it in memory, or at least store the ones already
    # TODO: loaded, since sending a query to the DB on each separate monster is inefficient

    loot_list = [] # type: list[tuple]

    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM loot_table WHERE entry = ?", [monster_loot_table_ID])

        loot_table_info = list(cursor.fetchone())  # load the loot_table row into a list
        # get an index at which we stop at because there are no further items beyond said index
        stop_at_idx = loot_table_info.index(0)  # TODO: Try/Catch because this will crash if the loot_table row is full

        if stop_at_idx % 2 == 0:
            """
            if we stop at an even index, that means that we're stopping at a itemX_chance row, which means that we
            have an item with a 0% drop chance and that is against our interests.
            """
            raise Exception("loot_table row is invalid!")

        # pack each drop into a tuple containing the item_ID and the chance to drop
        for idx in range(1, stop_at_idx, 2):
            item_ID = loot_table_info[idx]
            item_drop_chance = loot_table_info[idx+1]

            loot_list.append((item_ID, item_drop_chance))

    return loot_list

def load_item(item_ID: int):
    """
    Load an item from item_template, convert it to a object of Class Item and return it
    The item_template table is as follows:
    entry,      name, type, buy_price, sell_price, min_dmg, max_dmg
        1,'Wolf Pelt','misc',       1,          1,     Null, Null
    The item is of type misc, making us use the default class Item

    entry,             name,    type, buy_price, sell_price, min_dmg, max_dmg
      100, 'Arcanite Reaper', 'weapon',   125,          100,     56,      128
    This item is of type weapon, making us use the class Weapon to create it

    :returns a class object, depending on what the type is
    """
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM item_template WHERE entry = ?", [item_ID])
        item_template_info = cursor.fetchone()

        item_name = item_template_info[DBINDEX_ITEM_TEMPLATE_NAME]
        item_type = item_template_info[DBINDEX_ITEM_TEMPLATE_TYPE]
        item_buy_price = item_template_info[DBINDEX_ITEM_TEMPLATE_BUY_PRICE]  # type: int
        item_sell_price = item_template_info[DBINDEX_ITEM_TEMPLATE_SELL_PRICE]  # type: int

        if item_type == 'misc':
            return items.Item(name=item_name, buy_price=item_buy_price, sell_price=item_sell_price)
        elif item_type == 'weapon':
            item_min_dmg = item_template_info[DBINDEX_ITEM_TEMPLATE_MIN_DMG]  # type: int
            item_max_dmg = item_template_info[DBINDEX_ITEM_TEMPLATE_MAX_DMG]  # type: int

            return items.Weapon(name=item_name, buy_price=item_buy_price, sell_price=item_sell_price,
                                min_damage=item_min_dmg, max_damage=item_max_dmg)
        else:
            raise Exception("Unsupported item type {}".format(item_type))

def load_character_level_stats() -> dict:
    """
    Read the table file holding information about the amount of stats you should get according to the level you've attained
    1 - level; 2 - hp; 3 - mana; 4 - strength; 5 - armor;
    :returns A dictionary of dictionaries. Key: level(int), Value: dictionary holding values for hp,mana,etc
    """
    key_level_stats_health = 'health'
    key_level_stats_mana = 'mana'
    key_level_stats_strength = 'strength'
    key_level_stats_armor = 'armor'

    level_stats = {}
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()
        lvl_stats_reader = cursor.execute("SELECT * FROM levelup_stats")

        for line in lvl_stats_reader:
            level_dict = {}

            level = line[DBINDEX_LEVELUP_STATS_LEVEL]  # type: int
            hp = line[DBINDEX_LEVELUP_STATS_HEALTH]   # type: int
            mana = line[DBINDEX_LEVELUP_STATS_MANA]  # type: int
            strength = line[DBINDEX_LEVELUP_STATS_STRENGTH]  # type: int
            armor = line[DBINDEX_LEVELUP_STATS_ARMOR]  # type: int

            level_dict[key_level_stats_health] = hp
            level_dict[key_level_stats_mana] = mana
            level_dict[key_level_stats_strength] = strength
            level_dict[key_level_stats_armor] = armor

            level_stats[level] = level_dict

    return level_stats

def load_character_xp_requirements() -> dict:
    """
    Load the information about the necessary XP needed to reach a certain level.
    The table's contents is like this:
    level, xp needed to reach the next one
    1,     400 meaning you need to have 400XP to reach level 2
    2,     800 800XP needed to reach level 3
    :return: A dictionary - Key: Level, Value: XP Needed
                                    1,  400
    """
    xp_req_dict = {}

    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()
        xp_req_reader = cursor.execute("SELECT * FROM level_xp_requirement")

        for line in xp_req_reader:
            level = line[DBINDEX_LEVEL_XP_REQUIREMENT_LEVEL]  # type: int
            xp_required = line[DBINDEX_LEVEL_XP_REQUIREMENT_XP_REQUIRED]  # type: int

            xp_req_dict[level] = xp_required

    return xp_req_dict
