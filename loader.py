import sqlite3
import items
from buffs import BeneficialBuff, DoT
from damage import Damage
from decorators import db_connection
from database.database_info import \
    (DB_PATH,

     DBINDEX_SAVED_CHARACTER_NAME, DBINDEX_SAVED_CHARACTER_CLASS, DBINDEX_SAVED_CHARACTER_LEVEL,
     DBINDEX_SAVED_CHARACTER_LOADED_SCRIPTS_TABLE_ID, DBINDEX_SAVED_CHARACTER_KILLED_MONSTERS_ID,
     DBINDEX_SAVED_CHARACTER_COMPLETED_QUESTS_ID, DBINDEX_SAVED_CHARACTER_EQUIPMENT_ID,
     DBINDEX_SAVED_CHARACTER_INVENTORY_ID, DBINDEX_SAVED_CHARACTER_GOLD,

     DBINDEX_SC_EQUIPMENT_BOOTS_ID, DBINDEX_SC_EQUIPMENT_LEGGINGS_ID, DBINDEX_SC_EQUIPMENT_BELT_ID,
     DBINDEX_SC_EQUIPMENT_GLOVES_ID, DBINDEX_SC_EQUIPMENT_BRACER_ID, DBINDEX_SC_EQUIPMENT_CHESTGUARD_ID,
     DBINDEX_SC_EQUIPMENT_SHOULDERPAD_ID, DBINDEX_SC_EQUIPMENT_NECKLACE_ID, DBINDEX_SC_EQUIPMENT_HEADPIECE_ID,

     DBINDEX_SC_LOADED_SCRIPTS_SCRIPT_NAME,

     DBINDEX_SC_KILLED_MONSTERS_GUID,

     DBINDEX_SC_COMPLETED_QUESTS_NAME,

     DBINDEX_SC_INVENTORY_ITEM_ID, DBINDEX_SC_INVENTORY_ITEM_COUNT,


     DBINDEX_CREATURES_GUID, DBINDEX_CREATURES_CREATURE_ID,

     DBINDEX_CREATURE_TEMPLATE_NAME, DBINDEX_CREATURE_TEMPLATE_LEVEL,
     DBINDEX_CREATURE_TEMPLATE_HEALTH, DBINDEX_CREATURE_TEMPLATE_MANA,
     DBINDEX_CREATURE_TEMPLATE_MIN_DMG, DBINDEX_CREATURE_TEMPLATE_MAX_DMG,
     DBINDEX_CREATURE_TEMPLATE_QUEST_RELATION_ID, DBINDEX_CREATURE_TEMPLATE_LOOT_TABLE_ID,
     DBINDEX_CREATURE_TEMPLATE_GOSSIP, DBINDEX_CREATURE_TEMPLATE_ENTRY, DBINDEX_CREATURE_TEMPLATE_TYPE,
     DBINDEX_CREATURE_TEMPLATE_ARMOR, DBINDEX_CREATURE_TEMPLATE_RESPAWNABLE,

     DBINDEX_NPC_VENDOR_ITEM_COUNT, DBINDEX_NPC_VENDOR_ITEM_ID, DBINDEX_NPC_VENDOR_PRICE,

     DBINDEX_ITEM_TEMPLATE_ENTRY,
     DBINDEX_ITEM_TEMPLATE_NAME, DBINDEX_ITEM_TEMPLATE_TYPE, DBINDEX_ITEM_TEMPLATE_BUY_PRICE,
     DBINDEX_ITEM_TEMPLATE_SELL_PRICE, DBINDEX_ITEM_TEMPLATE_MIN_DMG, DBINDEX_ITEM_TEMPLATE_MAX_DMG,
     DBINDEX_ITEM_TEMPLATE_QUEST_ID, DBINDEX_ITEM_TEMPLATE_EFFECT, DBINDEX_ITEM_TEMPLATE_HEALTH,
     DBINDEX_ITEM_TEMPLATE_MANA, DBINDEX_ITEM_TEMPLATE_ARMOR, DBINDEX_ITEM_TEMPLATE_AGILITY,
     DBINDEX_ITEM_TEMPLATE_STRENGTH, DBINDEX_ITEM_TEMPLATE_SUB_TYPE,

     DBINDEX_QUEST_TEMPLATE_ENTRY, DBINDEX_QUEST_TEMPLATE_NAME, DBINDEX_QUEST_TEMPLATE_TYPE,
     DBINDEX_QUEST_TEMPLATE_LEVEL_REQUIRED, DBINDEX_QUEST_TEMPLATE_MONSTER_REQUIRED,
     DBINDEX_QUEST_TEMPLATE_AMOUNT_REQUIRED, DBINDEX_QUEST_TEMPLATE_XP_REWARD, DBINDEX_QUEST_TEMPLATE_ITEM_REQUIRED,
     DBINDEX_QUEST_TEMPLATE_ITEM_REWARD1, DBINDEX_QUEST_TEMPLATE_ITEM_REWARD2, DBINDEX_QUEST_TEMPLATE_ITEM_REWARD3,
     DBINDEX_QUEST_TEMPLATE_ITEM_CHOICE_ENABLED,

     DBINDEX_CREATURE_DEFAULTS_ARMOR,
     DBINDEX_CREATURE_DEFAULTS_CREATURE_LEVEL, DBINDEX_CREATURE_DEFAULTS_XP_REWARD,
     DBINDEX_CREATURE_DEFAULTS_MIN_GOLD_REWARD, DBINDEX_CREATURE_DEFAULTS_MAX_GOLD_REWARD,

     DBINDEX_SPELL_BUFFS_NAME, DBINDEX_SPELL_BUFFS_DURATION, DBINDEX_SPELL_BUFFS_STAT1, DBINDEX_SPELL_BUFFS_AMOUNT1,
     DBINDEX_SPELL_BUFFS_STAT2, DBINDEX_SPELL_BUFFS_AMOUNT2, DBINDEX_SPELL_BUFFS_STAT3, DBINDEX_SPELL_BUFFS_AMOUNT3,


     DBINDEX_SPELL_DOTS_NAME, DBINDEX_SPELL_DOTS_DAMAGE_PER_TICK, DBINDEX_SPELL_DOTS_DURATION,
     DBINDEX_SPELL_DOTS_DAMAGE_SCHOOL,

     DBINDEX_LEVELUP_STATS_LEVEL, DBINDEX_LEVELUP_STATS_HEALTH, DBINDEX_LEVELUP_STATS_MANA,
     DBINDEX_LEVELUP_STATS_STRENGTH, DBINDEX_LEVELUP_STATS_AGILITY, DBINDEX_LEVELUP_STATS_ARMOR,

     DBINDEX_LEVEL_XP_REQUIREMENT_LEVEL, DBINDEX_LEVEL_XP_REQUIREMENT_XP_REQUIRED
     )
from exceptions import NoSuchCharacterError
from quest import KillQuest, FetchQuest


def parse_int(value) -> int:
    """
    this function is used to parse data from the DB into an integer.
    because a lot of the cells can be empty, we get None as the return type. This function makes sure we
    get 0 if the value is None or empty

    !!! IMPORTANT !!!
    This is to be added to values where we would not want to cause an exception if they were None(Null), like
    the amount of gold a character has or the amount of armor an item gives.
    On other cases, like cells pointing to certain other database IDs, a missing number there makes the row
    invalid, thus we want to create an exception.
    """
    return int(value or 0)


@db_connection
def load_creature_defaults(cursor) -> dict:
    """
        Load the default values that a creature should have/give at a certain level.
        The table's contents are as follows:
        creature_level, armor, min_gold_reward, max_gold_reward, xp_reward
                    1,     50,              2,                5,        50
                    2,     65,              4,                6,        75
                    etc...

        :return: A dictionary as follows: Key: Level(ex: 1), Value: Dictionary{'armor': 50,
                                                                        'min_gold_reward': 2,
                                                                        'max_gold_reward': 5,
                                                                        'xp_reward': 50}
        """

    creature_defaults = {}

    creature_defaults_reader = cursor.execute("SELECT * FROM creature_defaults")

    for line in creature_defaults_reader:
        level = line[DBINDEX_CREATURE_DEFAULTS_CREATURE_LEVEL]  # type: int
        armor = line[DBINDEX_CREATURE_DEFAULTS_ARMOR]  # type: int
        min_gold_reward = line[DBINDEX_CREATURE_DEFAULTS_MIN_GOLD_REWARD]  # type: int
        max_gold_reward = line[DBINDEX_CREATURE_DEFAULTS_MAX_GOLD_REWARD]  # type: int
        xp_reward = line[DBINDEX_CREATURE_DEFAULTS_XP_REWARD]  # type: int

        creature_defaults[level] = {'armor': armor,
                                    'min_gold_reward': min_gold_reward, 'max_gold_reward':max_gold_reward,
                                    'xp_reward': xp_reward}

    return creature_defaults


@db_connection
def load_vendor_inventory(creature_entry: int, cursor) -> dict:
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

    npc_vendor_reader = cursor.execute("SELECT * FROM npc_vendor WHERE creature_entry = ?", [creature_entry])

    for npc_vendor_info in npc_vendor_reader:
        item_id = npc_vendor_info[DBINDEX_NPC_VENDOR_ITEM_ID]
        item_count = npc_vendor_info[DBINDEX_NPC_VENDOR_ITEM_COUNT]
        price = npc_vendor_info[DBINDEX_NPC_VENDOR_PRICE]

        item = load_item(item_id, cursor)  # type: Item

        if price: # check if there is anything set to price that'll make us override
            item.buy_price = price

        vendor_inventory[item.name] = (item, item_count)

    return vendor_inventory



@db_connection
def load_item(item_ID: int, cursor):
    """
    Load an item from item_template, convert it to a object of Class Item and return it
    The item_template table is as follows:
    entry,      name, type,  subtype, armor, health, mana, strength, agility, buy_price, sell_price, min_dmg, max_dmg, quest_ID, effect
        1,'Wolf Pelt','misc', Null, Null,   Null, Null,     Null,    Null,         1,          1,     Null, Null  ,        1,      0
    The item is of type misc, making us use the default class Item. It is also collected for the quest with ID 1

    entry,             name,    type, subtype,  armor, health, mana, strength, agility,  buy_price, sell_price, min_dmg, max_dmg, quest_ID, effect
      100, 'Arcanite Reaper', 'weapon',   Null,  0,     0,    0,        0,       0,        125,          100,     56,      128,        0,      0
    This item is of type weapon, making us use the class Weapon to create it

    entry,             name,    type,   subtype, armor, health, mana, strength, agility, buy_price, sell_price, min_dmg, max_dmg, quest_ID, effect
        4,'Strength Potion', 'potion',    Null, Null,   Null, Null,    Null,    Null,         1,           1,    Null,    Null,        0,      1
    This item is of type Potion and when consumed gives off the effect (spell_buffs table entry) 1
    :returns a class object, depending on what the type is
    """
    if item_ID <= 0 or item_ID is None:
        raise Exception("There is no such item with an ID that's 0 or negative!")

    cursor.execute("SELECT * FROM item_template WHERE entry = ?", [item_ID])
    item_template_info = cursor.fetchone()

    item_id = item_template_info[DBINDEX_ITEM_TEMPLATE_ENTRY]  # type: int
    item_name = item_template_info[DBINDEX_ITEM_TEMPLATE_NAME]
    item_type = item_template_info[DBINDEX_ITEM_TEMPLATE_TYPE]
    item_buy_price = parse_int(item_template_info[DBINDEX_ITEM_TEMPLATE_BUY_PRICE])  # type: int
    item_sell_price = parse_int(item_template_info[DBINDEX_ITEM_TEMPLATE_SELL_PRICE])  # type: int

    if item_type == 'misc':
        item_quest_ID = item_template_info[DBINDEX_ITEM_TEMPLATE_QUEST_ID]
        return items.Item(name=item_name, item_id=item_id, buy_price=item_buy_price, sell_price=item_sell_price,
                          quest_ID=item_quest_ID)
    elif item_type == 'weapon':
        item_health = parse_int(item_template_info[DBINDEX_ITEM_TEMPLATE_HEALTH])  # type: int
        item_mana = parse_int(item_template_info[DBINDEX_ITEM_TEMPLATE_MANA])  # type: int
        item_armor = parse_int(item_template_info[DBINDEX_ITEM_TEMPLATE_ARMOR])  # type: int
        item_strength = parse_int(item_template_info[DBINDEX_ITEM_TEMPLATE_STRENGTH])  # type: int
        item_agility = parse_int(item_template_info[DBINDEX_ITEM_TEMPLATE_AGILITY])  # type: int
        attributes = items.create_attributes_dict(bonus_health=item_health, bonus_mana=item_mana,
                                                  armor=item_armor, strength=item_strength, agility=item_agility)

        item_min_dmg = item_template_info[DBINDEX_ITEM_TEMPLATE_MIN_DMG]  # type: int
        item_max_dmg = item_template_info[DBINDEX_ITEM_TEMPLATE_MAX_DMG]  # type: int

        return items.Weapon(name=item_name, item_id=item_id, attributes_dict=attributes,
                            buy_price=item_buy_price, sell_price=item_sell_price,
                            min_damage=item_min_dmg, max_damage=item_max_dmg)
    elif item_type == 'equipment':
        item_health = parse_int(item_template_info[DBINDEX_ITEM_TEMPLATE_HEALTH])  # type: int
        item_mana = parse_int(item_template_info[DBINDEX_ITEM_TEMPLATE_MANA])  # type: int
        item_armor = parse_int(item_template_info[DBINDEX_ITEM_TEMPLATE_ARMOR])  # type: int
        item_strength = parse_int(item_template_info[DBINDEX_ITEM_TEMPLATE_STRENGTH])  # type: int
        item_agility = parse_int(item_template_info[DBINDEX_ITEM_TEMPLATE_AGILITY])  # type: int
        attributes = items.create_attributes_dict(bonus_health=item_health, bonus_mana=item_mana,
                                                  armor=item_armor, strength=item_strength, agility=item_agility)
        item_slot = item_template_info[DBINDEX_ITEM_TEMPLATE_SUB_TYPE]

        return items.Equipment(name=item_name, item_id=item_id, slot=item_slot, attributes_dict=attributes,
                               buy_price=item_buy_price, sell_price=item_sell_price)
    elif item_type == 'potion':
        buff_id = item_template_info[DBINDEX_ITEM_TEMPLATE_EFFECT]  # type: int
        item_buff_effect = load_buff(buff_id, cursor)  # type: BeneficialBuff

        return items.Potion(name=item_name, item_id=item_id, buy_price=item_buy_price, sell_price=item_sell_price,
                            buff=item_buff_effect)
    else:
        raise Exception(f'Unsupported item type {item_type}')


@db_connection
def load_buff(buff_id: int, cursor) -> BeneficialBuff:
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
    cursor.execute("SELECT * FROM spell_buffs WHERE entry = ?", [buff_id])
    buff_information = cursor.fetchone()

    buff_name = buff_information[DBINDEX_SPELL_BUFFS_NAME]  # type: str
    buff_stat1 = buff_information[DBINDEX_SPELL_BUFFS_STAT1]  # type: str
    buff_amount1 = parse_int(buff_information[DBINDEX_SPELL_BUFFS_AMOUNT1])  # type: int
    buff_stat2 = buff_information[DBINDEX_SPELL_BUFFS_STAT2]  # type: str
    buff_amount2 = parse_int(buff_information[DBINDEX_SPELL_BUFFS_AMOUNT2])  # type: int
    buff_stat3 = buff_information[DBINDEX_SPELL_BUFFS_STAT3]  # type: str
    buff_amount3 = parse_int(buff_information[DBINDEX_SPELL_BUFFS_AMOUNT3])  # type: int
    buff_duration = parse_int(buff_information[DBINDEX_SPELL_BUFFS_DURATION])  # type: int

    #  Create a list of tuples with each buff
    buff_stats_and_amounts = [(buff_stat1, buff_amount1), (buff_stat2, buff_amount2), (buff_stat3, buff_amount3)]

    return BeneficialBuff(name=buff_name, buff_stats_and_amounts=buff_stats_and_amounts,
                          duration=buff_duration)


@db_connection
def load_dot(dot_id: int, level: int, cursor) -> DoT:
    """ Loads a DoT from the spell_dots table, whose contents are the following:
    entry,      name,    damage_per_tick, damage_school, duration, comment
        1,   Melting,                 2,          magic,        2,  For the Paladin spell Melting Strike
    A DoT that does 2 magic damage each tick and lasts for two turns.

    load the information about the DoT, convert it to an instance of class DoT and return it.

    :param dot_id: the entry of the DoT in the spell_dots table
    :param level: the level of the caster
    """
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

"""///////////////////// SAVED_CHARACTER /////////////////////"""


@db_connection
def load_all_saved_characters_general_info(cursor) -> list:
    """
    This function loads general information about the saved characters in the DB and returns it as a list of
    dictionaries to  be easily printable.
    """
    saved_characters = []
    gi_char_reader = cursor.execute("SELECT name, class, level FROM saved_character")

    for char_info in gi_char_reader:
        char_name = char_info[DBINDEX_SAVED_CHARACTER_NAME]
        char_class = char_info[DBINDEX_SAVED_CHARACTER_CLASS]
        char_level = char_info[DBINDEX_SAVED_CHARACTER_LEVEL]

        saved_characters.append({'name': char_name, 'class': char_class, 'level': char_level})

    return saved_characters


"""///////////////////// SAVED_CHARACTER /////////////////////"""


@db_connection
def load_character_level_stats(cursor) -> dict:
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
    lvl_stats_reader = cursor.execute("SELECT * FROM levelup_stats")

    for line in lvl_stats_reader:
        level_dict = {}

        level = line[DBINDEX_LEVELUP_STATS_LEVEL]  # type: int
        hp = parse_int(line[DBINDEX_LEVELUP_STATS_HEALTH])   # type: int
        mana = parse_int(line[DBINDEX_LEVELUP_STATS_MANA])  # type: int
        strength = parse_int(line[DBINDEX_LEVELUP_STATS_STRENGTH])  # type: int
        agility = parse_int(line[DBINDEX_LEVELUP_STATS_AGILITY]) # type: int
        armor = parse_int(line[DBINDEX_LEVELUP_STATS_ARMOR])  # type: int

        level_dict[key_level_stats_health] = hp
        level_dict[key_level_stats_mana] = mana
        level_dict[key_level_stats_strength] = strength
        level_dict[key_level_stats_agility] = agility
        level_dict[key_level_stats_armor] = armor

        level_stats[level] = level_dict

    return level_stats


@db_connection
def load_character_xp_requirements(cursor) -> dict:
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

    xp_req_reader = cursor.execute("SELECT * FROM level_xp_requirement")

    for line in xp_req_reader:
        level = line[DBINDEX_LEVEL_XP_REQUIREMENT_LEVEL]  # type: int
        xp_required = line[DBINDEX_LEVEL_XP_REQUIREMENT_XP_REQUIRED]  # type: int

        xp_req_dict[level] = xp_required

    return xp_req_dict
