import sqlite3
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
