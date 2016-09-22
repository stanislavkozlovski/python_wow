import sqlite3

from database_info import \
    (DB_PATH,

     DBINDEX_SAVED_CHARACTER_NAME, DBINDEX_SAVED_CHARACTER_CLASS, DBINDEX_SAVED_CHARACTER_LEVEL,
     DBINDEX_SAVED_CHARACTER_LOADED_SCRIPTS_TABLE_ID, DBINDEX_SAVED_CHARACTER_KILLED_MONSTERS_ID,
     DBINDEX_SAVED_CHARACTER_COMPLETED_QUESTS_ID,

     DBINDEX_SC_LOADED_SCRIPTS_SCRIPT_NAME,

     DBINDEX_SC_KILLED_MONSTERS_GUID,

     DBINDEX_SC_COMPLETED_QUESTS_NAME,


     DBINDEX_CREATURES_GUID, DBINDEX_CREATURES_CREATURE_ID,

     DBINDEX_CREATURE_TEMPLATE_NAME, DBINDEX_CREATURE_TEMPLATE_LEVEL,
     DBINDEX_CREATURE_TEMPLATE_HEALTH, DBINDEX_CREATURE_TEMPLATE_MANA,
     DBINDEX_CREATURE_TEMPLATE_MIN_DMG, DBINDEX_CREATURE_TEMPLATE_MAX_DMG,
     DBINDEX_CREATURE_TEMPLATE_QUEST_RELATION_ID, DBINDEX_CREATURE_TEMPLATE_LOOT_TABLE_ID,
     DBINDEX_CREATURE_TEMPLATE_GOSSIP, DBINDEX_CREATURE_TEMPLATE_ENTRY, DBINDEX_CREATURE_TEMPLATE_TYPE,
     DBINDEX_CREATURE_TEMPLATE_ARMOR, DBINDEX_CREATURE_TEMPLATE_RESPAWNABLE,

     DBINDEX_NPC_VENDOR_ITEM_COUNT, DBINDEX_NPC_VENDOR_ITEM_ID, DBINDEX_NPC_VENDOR_PRICE,

     DBINDEX_ITEM_TEMPLATE_NAME, DBINDEX_ITEM_TEMPLATE_TYPE, DBINDEX_ITEM_TEMPLATE_BUY_PRICE,
     DBINDEX_ITEM_TEMPLATE_SELL_PRICE, DBINDEX_ITEM_TEMPLATE_MIN_DMG, DBINDEX_ITEM_TEMPLATE_MAX_DMG,
     DBINDEX_ITEM_TEMPLATE_QUEST_ID, DBINDEX_ITEM_TEMPLATE_EFFECT,

     DBINDEX_QUEST_TEMPLATE_ENTRY, DBINDEX_QUEST_TEMPLATE_NAME, DBINDEX_QUEST_TEMPLATE_TYPE,
     DBINDEX_QUEST_TEMPLATE_LEVEL_REQUIRED, DBINDEX_QUEST_TEMPLATE_MONSTER_REQUIRED,
     DBINDEX_QUEST_TEMPLATE_AMOUNT_REQUIRED, DBINDEX_QUEST_TEMPLATE_XP_REWARD, DBINDEX_QUEST_TEMPLATE_ITEM_REQUIRED,
     DBINDEX_QUEST_TEMPLATE_ITEM_REWARD1, DBINDEX_QUEST_TEMPLATE_ITEM_REWARD2, DBINDEX_QUEST_TEMPLATE_ITEM_REWARD3,
     DBINDEX_QUEST_TEMPLATE_ITEM_CHOICE_ENABLED,

     DBINDEX_CREATURE_DEFAULT_XP_REWARDS_LEVEL, DBINDEX_CREATURE_DEFAULT_XP_REWARDS_XP,

     DBINDEX_CREATURE_DEFAULT_GOLD_REWARDS_LEVEL, DBINDEX_CREATURE_DEFAULT_GOLD_REWARDS_MIN_GOLD_REWARD,
     DBINDEX_CREATURE_DEFAULT_GOLD_REWARDS_MAX_GOLD_REWARD, DBINDEX_CREATURE_DEFAULT_ARMOR_LEVEL,
     DBINDEX_CREATURE_DEFAULT_ARMOR_ARMOR,

     DBINDEX_SPELL_BUFFS_NAME, DBINDEX_SPELL_BUFFS_DURATION, DBINDEX_SPELL_BUFFS_STAT1, DBINDEX_SPELL_BUFFS_AMOUNT1,
     DBINDEX_SPELL_BUFFS_STAT2, DBINDEX_SPELL_BUFFS_AMOUNT2, DBINDEX_SPELL_BUFFS_STAT3, DBINDEX_SPELL_BUFFS_AMOUNT3,


     DBINDEX_SPELL_DOTS_NAME, DBINDEX_SPELL_DOTS_DAMAGE_PER_TICK, DBINDEX_SPELL_DOTS_DURATION,
     DBINDEX_SPELL_DOTS_DAMAGE_SCHOOL,

     DBINDEX_LEVELUP_STATS_LEVEL, DBINDEX_LEVELUP_STATS_HEALTH, DBINDEX_LEVELUP_STATS_MANA,
     DBINDEX_LEVELUP_STATS_STRENGTH, DBINDEX_LEVELUP_STATS_AGILITY, DBINDEX_LEVELUP_STATS_ARMOR,

     DBINDEX_LEVEL_XP_REQUIREMENT_LEVEL, DBINDEX_LEVEL_XP_REQUIREMENT_XP_REQUIRED
     )
from quest import KillQuest, FetchQuest
import items
from buffs import BeneficialBuff, DoT
from damage import Damage


def load_monsters(zone: str, subzone: str, character) -> tuple:
    """
        Gets a query from the creatures table to load all hostile creatures in our current zone

        guid, creature_id,       type,             zone,          subzone
           1,          11,  'monster',    Elwynn Forest, Northshire Abbey

        Then, with each guid queries up the creature information from creatures_template and
         creates a Monster object in a dictionary has GUID as a key and the monster as the value
        Key: 1, Value: Monster(....)

        creature_template table is as follows:

        creature entry, creature name,      type,   level, hp, mana, armor, min_dmg, max_dmg, quest_relation_ID, loot_table,ID,      gossip
                    1, Zimbab       ,   "monster"       1, 10,   10,   50,       2,       4                  1,             1, "Hey there"

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

            if character.has_killed_monster(creature_guid):
                continue  # do not add the monster to the list if the character has killed him!

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
            creature_template_armor = creature_template_info[DBINDEX_CREATURE_TEMPLATE_ARMOR]
            creature_template_max_dmg = creature_template_info[DBINDEX_CREATURE_TEMPLATE_MAX_DMG]  # type: int

            creature_template_quest_relation_ID = (
            creature_template_info[DBINDEX_CREATURE_TEMPLATE_QUEST_RELATION_ID]  # type: int
            if not creature_template_info[DBINDEX_CREATURE_TEMPLATE_QUEST_RELATION_ID] is None else 0)

            creature_template_loot_table_ID = (
            creature_template_info[DBINDEX_CREATURE_TEMPLATE_LOOT_TABLE_ID]  # type: int
            if not creature_template_info[DBINDEX_CREATURE_TEMPLATE_LOOT_TABLE_ID] is None else 0)

            creature_template_gossip = creature_template_info[DBINDEX_CREATURE_TEMPLATE_GOSSIP]  # type: str
            creature_template_respawnable = bool(creature_template_info[DBINDEX_CREATURE_TEMPLATE_RESPAWNABLE])

            # save into the set
            guid_name_set.add((creature_guid, creature_template_name))
            # save into the dict
            monsters_dict[creature_guid] = Monster(monster_id=creature_id,
                                                   name=creature_template_name,
                                                   health=creature_template_health,
                                                   mana=creature_template_mana,
                                                   armor=creature_template_armor,
                                                   level=creature_template_level,
                                                   min_damage=creature_template_min_dmg,
                                                   max_damage=creature_template_max_dmg,
                                                   quest_relation_id=creature_template_quest_relation_ID,
                                                   loot_table_ID=creature_template_loot_table_ID,
                                                   gossip=creature_template_gossip,
                                                   respawnable=creature_template_respawnable)



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


def load_quests(zone: str, subzone:str, character) -> list:
    """
    Gets a query from the quest_template table to load all the quests in our current zone.
    Table is as follows:
entry,            name,    type, required_level,           monster_required,  item_required, amount_required,
    1, A Canine Menace,killquest              1,      (name of monster)Wolf,      Wolf Meat,              10,

                zone,           sub_zone,   xp_reward, comment
       Elwynn Forest,   Northshire Valley,        300, Our First Quest!

       item_reward1, item_reward2, item_reward3, item_choice_enabled
                  1,            2,         Null,                0

    item_rewardX is the item's entry in the item_template table. We can have up to 3 (three) rewards from a quest.
    item_choice_enabled is a boolean (1=true, 0=false) which indicates if we get all the items or have to choose one particular item
    from the ones available

    Type decides what kind of quests it is.
    killquest = kill X amount of monster_required
    fetchquest = obtain X amount of item_required.
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

            if character.has_completed_quest(quest_name):
                continue  # do not load the quest into the game if the character has completed it

            quest_type = row[DBINDEX_QUEST_TEMPLATE_TYPE]  #  type: str
            quest_level_requirement = row[DBINDEX_QUEST_TEMPLATE_LEVEL_REQUIRED]  # type: int
            quest_monster_required = row[DBINDEX_QUEST_TEMPLATE_MONSTER_REQUIRED]  # type: str
            quest_item_required = row[DBINDEX_QUEST_TEMPLATE_ITEM_REQUIRED]  # type: str
            quest_amount_required = row[DBINDEX_QUEST_TEMPLATE_AMOUNT_REQUIRED]  # type: int
            quest_xp_reward = row[DBINDEX_QUEST_TEMPLATE_XP_REWARD]  # type: int
            quest_item_reward1_id = row[DBINDEX_QUEST_TEMPLATE_ITEM_REWARD1]  # type: int
            quest_item_reward2_id = row[DBINDEX_QUEST_TEMPLATE_ITEM_REWARD2]  # type: int
            quest_item_reward3_id = row[DBINDEX_QUEST_TEMPLATE_ITEM_REWARD3]  # type: int
            quest_item_choice_enabled = bool(row[DBINDEX_QUEST_TEMPLATE_ITEM_CHOICE_ENABLED])  # type: bool

            item_rewards = load_quest_item_rewards(qitem1_id=quest_item_reward1_id,
                                                   qitem2_id=quest_item_reward2_id,
                                                   qitem3_id=quest_item_reward3_id)  # type: dict

            #  create the quest object according to it's type
            if quest_type == "killquest":
                quest_list[quest_name] = KillQuest(quest_name=quest_name,
                                                   quest_id=quest_entry,
                                                   required_monster=quest_monster_required,
                                                   required_kills=quest_amount_required,
                                                   xp_reward=quest_xp_reward,
                                                   item_reward_dict=item_rewards,
                                                   reward_choice_enabled=quest_item_choice_enabled,
                                                   level_required=quest_level_requirement)
            elif quest_type == "fetchquest":
                quest_list[quest_name] = FetchQuest(quest_name=quest_name,
                                                   quest_id=quest_entry,
                                                   required_item=quest_item_required,
                                                   required_item_count=quest_amount_required,
                                                   xp_reward=quest_xp_reward,
                                                   item_reward_dict=item_rewards,
                                                   reward_choice_enabled=quest_item_choice_enabled,
                                                   level_required=quest_level_requirement)

    return quest_list


def load_quest_item_rewards(qitem1_id: int, qitem2_id: int, qitem3_id: int) -> dict:
    """ This function loads all the items that the quest rewards and returns a
        Dictionary: Key: Item Name, Value: instance of class Item"""
    item_rewards_dict = {}  # type: dict
    if qitem1_id:
        qitem1 = load_item(qitem1_id)  # type: Item
        item_rewards_dict[qitem1.name] = qitem1  # add to the dictionary

        if qitem2_id:
            qitem2 = load_item(qitem2_id)  # type: Item
            item_rewards_dict[qitem2.name] = qitem2

            if qitem3_id:
                qitem3 = load_item(qitem3_id)  #type: Item
                item_rewards_dict[qitem3.name] = qitem3

    return item_rewards_dict


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


def load_creature_default_armor() -> dict:
    """
        Load the default armor that a creature should have at a certain level.
        The table's contents are as follows:
        Level, Armor
            1,     50
            2,     65
            etc...

        :return: A dictionary as follows: Key: Level, Value: Armor
                                                   1,         50
        """

    default_armor_dict = {}

    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()
        default_armor_reader = cursor.execute("SELECT * FROM creature_default_armor")

        for line in default_armor_reader:
            level = line[DBINDEX_CREATURE_DEFAULT_ARMOR_LEVEL]
            armor = line[DBINDEX_CREATURE_DEFAULT_ARMOR_ARMOR]

            default_armor_dict[level] = armor

    return default_armor_dict


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
    entry,      name, type, buy_price, sell_price, min_dmg, max_dmg, quest_ID, effect
        1,'Wolf Pelt','misc',       1,          1,     Null, Null  ,        1,      0
    The item is of type misc, making us use the default class Item. It is also collected for the quest with ID 1

    entry,             name,    type, buy_price, sell_price, min_dmg, max_dmg, quest_ID, effect
      100, 'Arcanite Reaper', 'weapon',   125,          100,     56,      128,        0,      0
    This item is of type weapon, making us use the class Weapon to create it

    entry,             name,    type, buy_price, sell_price, min_dmg, max_dmg, quest_ID, effect
        4,'Strength Potion', 'potion',       1,           1,    Null,    Null,        0,      1
    This item is of type Potion and when consumed gives off the effect (spell_buffs table entry) 1
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
            item_quest_ID = item_template_info[DBINDEX_ITEM_TEMPLATE_QUEST_ID]
            return items.Item(name=item_name, buy_price=item_buy_price, sell_price=item_sell_price, quest_ID=item_quest_ID)
        elif item_type == 'weapon':
            item_min_dmg = item_template_info[DBINDEX_ITEM_TEMPLATE_MIN_DMG]  # type: int
            item_max_dmg = item_template_info[DBINDEX_ITEM_TEMPLATE_MAX_DMG]  # type: int

            return items.Weapon(name=item_name, buy_price=item_buy_price, sell_price=item_sell_price,
                                min_damage=item_min_dmg, max_damage=item_max_dmg)
        elif item_type == 'potion':
            buff_id = item_template_info[DBINDEX_ITEM_TEMPLATE_EFFECT]  # type: int
            item_buff_effect = load_buff(buff_id)  # type: BeneficialBuff

            return items.Potion(name=item_name, buy_price=item_buy_price, sell_price=item_sell_price,
                                buff=item_buff_effect)
        else:
            raise Exception("Unsupported item type {}".format(item_type))


def load_buff(buff_id: int) -> BeneficialBuff:
    """
    Loads a buff from the DB table spells_buffs, whose contents are the following:
    entry,             name, duration,    stat,   amount,   stat2,   amount2,stat3,   amount3, comment
        1,  Heart of a Lion,        5,strength,       10,                                      Increases strength by 10 for 5 turns
        stat - the stat this buff increases
        amount - the amount it increases the stat by
        duration - the amount of turns this buff lasts for
    This buff increases your strength by 10 for 5 turns.

    Load the information about the buff, convert it to an class Buff object and return it
    :param buff_id: the buff entry in spells_buffs
    :return: A instance of class Buff
    """
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM spell_buffs WHERE entry = ?", [buff_id])
        buff_information = cursor.fetchone()

        buff_name = buff_information[DBINDEX_SPELL_BUFFS_NAME]  # type: str
        buff_stat1 = buff_information[DBINDEX_SPELL_BUFFS_STAT1]  # type: str
        buff_amount1 = buff_information[DBINDEX_SPELL_BUFFS_AMOUNT1]  # type: int
        buff_stat2 = buff_information[DBINDEX_SPELL_BUFFS_STAT2]  # type: str
        buff_amount2 = buff_information[DBINDEX_SPELL_BUFFS_AMOUNT2]  # type: int
        buff_stat3 = buff_information[DBINDEX_SPELL_BUFFS_STAT3]  # type: str
        buff_amount3 = buff_information[DBINDEX_SPELL_BUFFS_AMOUNT3]  # type: int
        buff_duration = buff_information[DBINDEX_SPELL_BUFFS_DURATION]  # type: int


        #  Create a list of tuples with each buff
        buff_stats_and_amounts = [(buff_stat1, buff_amount1), (buff_stat2, buff_amount2), (buff_stat3, buff_amount3)]

    return BeneficialBuff(name=buff_name, buff_stats_and_amounts=buff_stats_and_amounts,
                          duration=buff_duration)

def load_dot(dot_id: int, level: int) -> DoT:
    """ Loads a DoT from the spell_dots table, whose contents are the following:
    entry,      name,    damage_per_tick, damage_school, duration, comment
        1,   Melting,                 2,          magic,        2,  For the Paladin spell Melting Strike
    A DoT that does 2 magic damage each tick and lasts for two turns.

    load the information about the DoT, convert it to an instance of class DoT and return it.

    :param dot_id: the entry of the DoT in the spell_dots table
    :param level: the level of the caster
    """
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM spell_dots WHERE entry = ?", [dot_id])
        dot_info = cursor.fetchone()

        dot_name = dot_info[DBINDEX_SPELL_DOTS_NAME]
        dot_damage_per_tick = dot_info[DBINDEX_SPELL_DOTS_DAMAGE_PER_TICK]
        dot_damage_school = dot_info[DBINDEX_SPELL_DOTS_DAMAGE_SCHOOL]
        dot_duration = dot_info[DBINDEX_SPELL_DOTS_DURATION]

        dot_damage = Damage(0,0)  # type: Damage

        if dot_damage_school == "magic":
            dot_damage = Damage(magic_dmg=dot_damage_per_tick)
        elif dot_damage_school == "physical":
            dot_damage = Damage(phys_dmg=dot_damage_per_tick)

    return DoT(name=dot_name, damage_tick=dot_damage, duration=dot_duration, caster_lvl=level)

def load_saved_character(name: str):
    """
    This function loads the information about a saved chacacter in the saved_character DB table.
    """
    # TODO: Create character
    from classes import Paladin
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()
        sv_char_reader = cursor.execute("SELECT * FROM saved_character WHERE name = ?", [name]).fetchone()

        char_name = sv_char_reader[DBINDEX_SAVED_CHARACTER_NAME]
        char_class = sv_char_reader[DBINDEX_SAVED_CHARACTER_CLASS]
        char_level = sv_char_reader[DBINDEX_SAVED_CHARACTER_LEVEL]
        char_loaded_scripts_ID = sv_char_reader[DBINDEX_SAVED_CHARACTER_LOADED_SCRIPTS_TABLE_ID]
        char_killed_monsters_ID = sv_char_reader[DBINDEX_SAVED_CHARACTER_KILLED_MONSTERS_ID]
        char_completed_quests_ID = sv_char_reader[DBINDEX_SAVED_CHARACTER_COMPLETED_QUESTS_ID]

        if char_class == 'Paladin':
            return Paladin(name=name, level=char_level,
                           loaded_scripts=load_saved_character_loaded_scripts(char_loaded_scripts_ID),
                           killed_monsters=load_saved_character_killed_monsters(char_killed_monsters_ID),
                           completed_quests=load_saved_character_completed_quests(char_completed_quests_ID))
        else:
            raise Exception("Unsupported class - {}".format(char_class))


def load_saved_character_loaded_scripts(id: int) -> set:
    """
    This function loads all the scripts that a character has loaded, which correspond to the ID of
     saved_character_loaded_scripts table, which looks like this:

     id,    script_name
      1,     HASKELL_PRAXTON_CONVERSATION

    :param id: ID identificaton in saved_character_loaded_scripts
    :return: a set containing all the names -> {HASKEL_PRAXTON_CONVERSATION} in this case
    """
    loaded_scripts_set = set()

    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()

        loaded_scripts_reader = cursor.execute("SELECT * FROM saved_character_loaded_scripts WHERE id = ?", [id])

        for loaded_script_info in loaded_scripts_reader:
            loaded_script_name = loaded_script_info[DBINDEX_SC_LOADED_SCRIPTS_SCRIPT_NAME]
            loaded_scripts_set.add(loaded_script_name)

    return loaded_scripts_set


def load_saved_character_killed_monsters(id: int) -> set:
    """
        This function loads all the monsters that a character has killed's GUIDs, which correspond to the ID of
         saved_character_killed_monsters table, which looks like this:

         id,    GUID(of monster)
          1,     14
          1,      7
        IMPORTANT: This works only for monsters that by design should not be killed twice if the player restarts the game

        :param id: ID identificaton in saved_character_killed_monsters
        :return: a set containing all the GUIs -> {14, 7} in this case
        """

    killed_monsters_set = set()

    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()
        sc_killed_monsters_reader = cursor.execute("SELECT * FROM saved_character_killed_monsters WHERE id = ?", [id])

        for killed_monster_info in sc_killed_monsters_reader:
            sc_killed_monster_GUID = killed_monster_info[DBINDEX_SC_KILLED_MONSTERS_GUID]
            killed_monsters_set.add(sc_killed_monster_GUID)

    return killed_monsters_set


def load_saved_character_completed_quests(id: int) -> set:
    """
    This functions loads all the quests, which correspond to the ID of the saved_character_completed_quests table and
     that a character has completed. The table looks like this:

     id,  quest_name
      1,   A Canine Menace
      1,   Canine-Like Hunger

    :param id: ID identification in the saved_character_completed_quests table
    :return: a set containing all the names of the completed quests -> {"A Canine Menace", "Canine-Like Hunger"} in this case
    """

    completed_quests_set = set()

    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()
        sc_completed_quests_reader = cursor.execute("SELECT * FROM saved_character_completed_quests WHERE id = ?", [id])

        for completed_quest_info in sc_completed_quests_reader:
            sc_completed_quest_name = completed_quest_info[DBINDEX_SC_COMPLETED_QUESTS_NAME]  # type: str
            completed_quests_set.add(sc_completed_quest_name)

    return completed_quests_set

def load_character_level_stats() -> dict:
    """
    Read the table file holding information about the amount of stats you should get according to the level you've attained
    1 - level; 2 - hp; 3 - mana; 4 - strength; 5 - agility, 6 - armor;
    :returns A dictionary of dictionaries. Key: level(int), Value: dictionary holding values for hp,mana,etc
    """
    key_level_stats_health = 'health'
    key_level_stats_mana = 'mana'
    key_level_stats_strength = 'strength'
    key_level_stats_armor = 'armor'
    key_level_stats_agility = 'agility'

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
            agility = line[DBINDEX_LEVELUP_STATS_AGILITY]
            armor = line[DBINDEX_LEVELUP_STATS_ARMOR]  # type: int

            level_dict[key_level_stats_health] = hp
            level_dict[key_level_stats_mana] = mana
            level_dict[key_level_stats_strength] = strength
            level_dict[key_level_stats_agility] = agility
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
