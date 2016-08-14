import sqlite3

from quest import Quest
from database_info import \
       (DB_PATH, DBINDEX_CREATURES_GUID, DBINDEX_CREATURES_CREATURE_ID,

        DBINDEX_CREATURE_TEMPLATE_NAME, DBINDEX_CREATURE_TEMPLATE_LEVEL,
        DBINDEX_CREATURE_TEMPLATE_HEALTH, DBINDEX_CREATURE_TEMPLATE_MANA,
        DBINDEX_CREATURE_TEMPLATE_MIN_DMG, DBINDEX_CREATURE_TEMPLATE_MAX_DMG,
        DBINDEX_CREATURE_TEMPLATE_QUEST_RELATION_ID,
        DBINDEX_QUEST_TEMPLATE_ENTRY, DBINDEX_QUEST_TEMPLATE_NAME,
        DBINDEX_QUEST_TEMPLATE_LEVEL_REQUIRED, DBINDEX_QUEST_TEMPLATE_MONSTER_REQUIRED,
        DBINDEX_QUEST_TEMPLATE_AMOUNT_REQUIRED, DBINDEX_QUEST_TEMPLATE_XP_REWARD,

        DBINDEX_CREATURE_DEFAULT_XP_REWARDS_LEVEL, DBINDEX_CREATURE_DEFAULT_XP_REWARDS_XP,

        DBINDEX_LEVELUP_STATS_LEVEL, DBINDEX_LEVELUP_STATS_HEALTH, DBINDEX_LEVELUP_STATS_MANA,
        DBINDEX_LEVELUP_STATS_STRENGTH,

        DBINDEX_LEVEL_XP_REQUIREMENT_LEVEL, DBINDEX_LEVEL_XP_REQUIREMENT_XP_REQUIRED
        )


def load_creatures(zone: str, subzone:str) -> tuple:
    """
        Gets a query from the creatures table to load all the creatures in our current zone

        guid, creature_id,         zone,          subzone
           1,          11,Elwynn Forest, Northshire Abbey

        Then, with each guid queries up the creature information from creatures_template and
         creates a Monster object in a dictionary has GUID as a key and the monster as the value
        Key: 1, Value: Monster(....)

        creature_template table is as follows:

        creature entry, creature name, level, hp, mana, min_dmg, max_dmg
                    1, Zimbab       ,     1, 10,   10,       2,       4
        Creature Level: 1 Zimbab, HP: 10, MANA: 10, Damage: 2-4

        :return: A Dictionary: Key: guid, Value: Object of class entities.py/Monster,
                 A Set of Tuples ((Monster GUID, Monster Name))
    """
    from entities import Monster  # needed to be imported here otherwise we end up in an import loop

    monsters_dict = {}
    guid_name_set = set()

    print("Loading Monsters...")
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()
        creatures_reader = cursor.execute("SELECT * FROM creatures WHERE zone = ? AND sub_zone = ?"
                                                  , [zone, subzone])  # query all the creatures in our location :)

        for creature_info in creatures_reader.fetchall():
            creature_guid = int(creature_info[DBINDEX_CREATURES_GUID])
            creature_id = int(creature_info[DBINDEX_CREATURES_CREATURE_ID])

            # This will currently run a query for every monster, meaning if there are 20 of the exact same monsters,
            # 20 queries will be run. There isn't much sense in that, so:
            # TODO: Modify so we don't run unecessary queries for monster info that we've already loaded from the DB
            creature_template_reader = cursor.execute("SELECT * FROM creature_template WHERE entry = ?", [creature_id])
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
            creature_template_quest_relation_ID = (int(creature_template_info[DBINDEX_CREATURE_TEMPLATE_QUEST_RELATION_ID])
                if not creature_template_info[7] is None else -1)

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
                                                   quest_relation_id=creature_template_quest_relation_ID)



    print("Monsters loaded!")
    return monsters_dict, guid_name_set


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

            quest_list[quest_name] = Quest(quest_name= quest_name,
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


def load_character_level_stats() -> dict:
    """
    Read the table file holding information about the amount of stats you should get according to the level you've attained
    1 - level; 2 - hp; 3 - mana; 4 - strength;
    :returns A dictionary of dictionaries. Key: level(int), Value: dictionary holding values for hp,mana,etc
    """
    key_level_stats_health = 'health'
    key_level_stats_mana = 'mana'
    key_level_stats_strength = 'strength'

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

            level_dict[key_level_stats_health] = hp
            level_dict[key_level_stats_mana] = mana
            level_dict[key_level_stats_strength] = strength

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
