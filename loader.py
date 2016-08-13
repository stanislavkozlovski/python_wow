from entities import Monster
from quest import Quest
from database_info import (DB_PATH, DBINDEX_CREATURES_GUID, DBINDEX_CREATURES_CREATURE_ID, DBINDEX_CREATURE_TEMPLATE_NAME,
                           DBINDEX_CREATURE_TEMPLATE_LEVEL, DBINDEX_CREATURE_TEMPLATE_HEALTH, DBINDEX_CREATURE_TEMPLATE_MANA,
                           DBINDEX_CREATURE_TEMPLATE_MIN_DMG, DBINDEX_CREATURE_TEMPLATE_MAX_DMG,
                           DBINDEX_CREATURE_TEMPLATE_QUEST_RELATION_ID, DBINDEX_QUEST_TEMPLATE_ENTRY,
                           DBINDEX_QUEST_TEMPLATE_NAME, DBINDEX_QUEST_TEMPLATE_LEVEL_REQUIRED,
                           DBINDEX_QUEST_TEMPLATE_MONSTER_REQUIRED, DBINDEX_QUEST_TEMPLATE_AMOUNT_REQUIRED,
                           DBINDEX_QUEST_TEMPLATE_XP_REWARD
                           )
import sqlite3


# row[8] = comment
def load_creatures(zone: str, subzone:str):
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
            creature_template_info = creature_template_reader.fetchone() # entry is unique meaning the query will \
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
    entry,            name, level_required,           monster_required,  amount_required,         zone,          sub_zone, xp_reward, comment
        1, A Canine Menace,              1,      (name of monster)Wolf,               10,Elwynn Forest, Northshire Valley,       300, Our First Quest!

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
                                    kill_amount=quest_monster_kill_amount_required,
                                    xp_reward=quest_xp_reward,
                                    level_required=quest_level_requirement)

    return quest_list
