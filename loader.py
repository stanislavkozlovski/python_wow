import sqlite3

from database_info import \
    (DB_PATH, DBINDEX_CREATURES_GUID, DBINDEX_CREATURES_CREATURE_ID,

     DBINDEX_CREATURE_TEMPLATE_NAME, DBINDEX_CREATURE_TEMPLATE_LEVEL,
     DBINDEX_CREATURE_TEMPLATE_HEALTH, DBINDEX_CREATURE_TEMPLATE_MANA,
     DBINDEX_CREATURE_TEMPLATE_MIN_DMG, DBINDEX_CREATURE_TEMPLATE_MAX_DMG,
     DBINDEX_CREATURE_TEMPLATE_QUEST_RELATION_ID, DBINDEX_CREATURE_TEMPLATE_LOOT_TABLE_ID,
     DBINDEX_CREATURE_TEMPLATE_GOSSIP,

     DBINDEX_ITEM_TEMPLATE_NAME, DBINDEX_ITEM_TEMPLATE_TYPE, DBINDEX_ITEM_TEMPLATE_BUY_PRICE,
     DBINDEX_ITEM_TEMPLATE_SELL_PRICE, DBINDEX_ITEM_TEMPLATE_MIN_DMG, DBINDEX_ITEM_TEMPLATE_MAX_DMG,

     DBINDEX_QUEST_TEMPLATE_ENTRY, DBINDEX_QUEST_TEMPLATE_NAME,
     DBINDEX_QUEST_TEMPLATE_LEVEL_REQUIRED, DBINDEX_QUEST_TEMPLATE_MONSTER_REQUIRED,
     DBINDEX_QUEST_TEMPLATE_AMOUNT_REQUIRED, DBINDEX_QUEST_TEMPLATE_XP_REWARD,

     DBINDEX_CREATURE_DEFAULT_XP_REWARDS_LEVEL, DBINDEX_CREATURE_DEFAULT_XP_REWARDS_XP,

     DBINDEX_CREATURE_DEFAULT_GOLD_REWARDS_LEVEL, DBINDEX_CREATURE_DEFAULT_GOLD_REWARDS_MIN_GOLD_REWARD,
     DBINDEX_CREATURE_DEFAULT_GOLD_REWARDS_MAX_GOLD_REWARD,

     DBINDEX_LEVELUP_STATS_LEVEL, DBINDEX_LEVELUP_STATS_HEALTH, DBINDEX_LEVELUP_STATS_MANA,
     DBINDEX_LEVELUP_STATS_STRENGTH, DBINDEX_LEVELUP_STATS_ARMOR,

     DBINDEX_LEVEL_XP_REQUIREMENT_LEVEL, DBINDEX_LEVEL_XP_REQUIREMENT_XP_REQUIRED
     )
from quest import Quest
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
            creature_guid = int(creature_info[DBINDEX_CREATURES_GUID])
            creature_id = int(creature_info[DBINDEX_CREATURES_CREATURE_ID])

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
            creature_template_level = int(creature_template_info[DBINDEX_CREATURE_TEMPLATE_LEVEL])
            creature_template_health = int(creature_template_info[DBINDEX_CREATURE_TEMPLATE_HEALTH])
            creature_template_mana = int(creature_template_info[DBINDEX_CREATURE_TEMPLATE_MANA])
            creature_template_min_dmg = int(creature_template_info[DBINDEX_CREATURE_TEMPLATE_MIN_DMG])
            creature_template_max_dmg = int(creature_template_info[DBINDEX_CREATURE_TEMPLATE_MAX_DMG])

            creature_template_quest_relation_ID = (
            int(creature_template_info[DBINDEX_CREATURE_TEMPLATE_QUEST_RELATION_ID])
            if not creature_template_info[DBINDEX_CREATURE_TEMPLATE_QUEST_RELATION_ID] is None else -1)

            creature_template_loot_table_ID = (
            int(creature_template_info[DBINDEX_CREATURE_TEMPLATE_LOOT_TABLE_ID])
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

    npcs_dict = {}
    guid_name_set = set()

    print("Loading Friendly NPCs...")
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()
        fnpc_reader = cursor.execute("SELECT * FROM creatures WHERE type = ? AND zone = ? AND sub_zone = ?"
                                          , ["fnpc", zone, subzone])  # query all the creatures in our location :)

        for creature_info in fnpc_reader.fetchall():
            creature_guid = int(creature_info[DBINDEX_CREATURES_GUID])
            creature_id = int(creature_info[DBINDEX_CREATURES_CREATURE_ID])

            # This will currently run a query for every fnpc, meaning if there are 20 of the exact same npcs,
            # 20 queries will be run. There isn't much sense in that, so:
            # TODO: Modify so we don't run unecessary queries for fnpc info that we've already loaded from the DB
            creature_template_reader = cursor.execute("SELECT * FROM creature_template WHERE type = ? AND entry = ?",
                                                      ["fnpc",creature_id])
            creature_template_info = creature_template_reader.fetchone()  # entry is unique meaning the query will-
            # always return one npc

            # save the creature values

            creature_template_name = creature_template_info[DBINDEX_CREATURE_TEMPLATE_NAME]
            creature_template_level = int(creature_template_info[DBINDEX_CREATURE_TEMPLATE_LEVEL])
            creature_template_health = int(creature_template_info[DBINDEX_CREATURE_TEMPLATE_HEALTH])
            creature_template_mana = int(creature_template_info[DBINDEX_CREATURE_TEMPLATE_MANA])
            creature_template_min_dmg = int(creature_template_info[DBINDEX_CREATURE_TEMPLATE_MIN_DMG])
            creature_template_max_dmg = int(creature_template_info[DBINDEX_CREATURE_TEMPLATE_MAX_DMG])

            creature_template_quest_relation_ID = (
            int(creature_template_info[DBINDEX_CREATURE_TEMPLATE_QUEST_RELATION_ID])
            if not creature_template_info[DBINDEX_CREATURE_TEMPLATE_QUEST_RELATION_ID] is None else -1)

            creature_template_loot_table_ID = (
            int(creature_template_info[DBINDEX_CREATURE_TEMPLATE_LOOT_TABLE_ID])
            if not creature_template_info[DBINDEX_CREATURE_TEMPLATE_LOOT_TABLE_ID] is None else -1)

            creature_template_gossip = creature_template_info[DBINDEX_CREATURE_TEMPLATE_GOSSIP]

            # save into the set
            guid_name_set.add((creature_guid, creature_template_name))
            # save into the dict
            npcs_dict[creature_guid] = FriendlyNPC(name=creature_template_name, health=creature_template_health,
                                                   mana=creature_template_mana, level=creature_template_level,
                                                   min_damage=creature_template_min_dmg,
                                                   max_damage=creature_template_max_dmg,
                                                   quest_relation_id=creature_template_quest_relation_ID,
                                                   loot_table_ID=creature_template_loot_table_ID,
                                                   gossip=creature_template_gossip)

    print("Friendly NPCs loaded!")
    return npcs_dict, guid_name_set


def load_quests(zone: str, subzone:str) -> list:
    """
    Gets a query from the quest_template table to load all the quests in our current zone.
    Table is as follows:
entry,            name, required_level,           monster_required,  amount_required,         zone,          sub_zone,
    1, A Canine Menace,              1,      (name of monster)Wolf,               10,Elwynn Forest, Northshire Valley,
xp_reward, comment
    300, Our First Quest!

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
            quest_entry = int(row[DBINDEX_QUEST_TEMPLATE_ENTRY])
            quest_name = row[DBINDEX_QUEST_TEMPLATE_NAME]
            quest_level_requirement = int(row[DBINDEX_QUEST_TEMPLATE_LEVEL_REQUIRED])
            quest_monster_required = row[DBINDEX_QUEST_TEMPLATE_MONSTER_REQUIRED]  # monster name
            quest_monster_kill_amount_required = int(row[DBINDEX_QUEST_TEMPLATE_AMOUNT_REQUIRED])
            quest_xp_reward = int(row[DBINDEX_QUEST_TEMPLATE_XP_REWARD])

            quest_list[quest_name] = Quest(quest_name=quest_name,
                                           quest_id=quest_entry,
                                           creature_name=quest_monster_required,
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
            level = int(line[DBINDEX_CREATURE_DEFAULT_XP_REWARDS_LEVEL])
            xp_reward = int(line[DBINDEX_CREATURE_DEFAULT_XP_REWARDS_XP])

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
            level = int(line[DBINDEX_CREATURE_DEFAULT_GOLD_REWARDS_LEVEL])
            min_gold_reward = int(line[DBINDEX_CREATURE_DEFAULT_GOLD_REWARDS_MIN_GOLD_REWARD])
            max_gold_reward = int(line[DBINDEX_CREATURE_DEFAULT_GOLD_REWARDS_MAX_GOLD_REWARD])

            gold_rewards_dict[level] = (min_gold_reward, max_gold_reward)

    return gold_rewards_dict


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
        item_buy_price = int(item_template_info[DBINDEX_ITEM_TEMPLATE_BUY_PRICE])
        item_sell_price = int(item_template_info[DBINDEX_ITEM_TEMPLATE_SELL_PRICE])

        if item_type == 'misc':
            return items.Item(name=item_name, buy_price=item_buy_price, sell_price=item_sell_price)
        elif item_type == 'weapon':
            item_min_dmg = int(item_template_info[DBINDEX_ITEM_TEMPLATE_MIN_DMG])
            item_max_dmg = int(item_template_info[DBINDEX_ITEM_TEMPLATE_MAX_DMG])

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

            level = int(line[DBINDEX_LEVELUP_STATS_LEVEL])
            hp = int(line[DBINDEX_LEVELUP_STATS_HEALTH])
            mana = int(line[DBINDEX_LEVELUP_STATS_MANA])
            strength = int(line[DBINDEX_LEVELUP_STATS_STRENGTH])
            armor = int(line[DBINDEX_LEVELUP_STATS_ARMOR])

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
            level = int(line[DBINDEX_LEVEL_XP_REQUIREMENT_LEVEL])
            xp_required = int(line[DBINDEX_LEVEL_XP_REQUIREMENT_XP_REQUIRED])

            xp_req_dict[level] = xp_required

    return xp_req_dict
