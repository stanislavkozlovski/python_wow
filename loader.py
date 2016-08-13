from entities import Monster
from quest import Quest
import sqlite3

DB_PATH = "./python_wowDB.db"

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
            creature_guid = int(creature_info[0])
            creature_id = int(creature_info[1])

            # This will currently run a query for every monster, meaning if there are 20 of the exact same monsters,
            # 20 queries will be run. There isn't much sense in that, so:
            # TODO: Modify so we don't run unecessary queries for monster info that we've already loaded from the DB
            creature_template_reader = cursor.execute("SELECT * FROM creature_template WHERE entry = ?", [creature_id])
            creature_template_info = creature_template_reader.fetchone() # entry is unique meaning the query will always return one monster

            # save the creature values
            # )
            creature_template_name = creature_template_info[1]
            creature_template_level = int(creature_template_info[2])
            creature_template_health = int(creature_template_info[3])
            creature_template_mana = int(creature_template_info[4])
            creature_template_min_dmg = int(creature_template_info[5])
            creature_template_max_dmg = int(creature_template_info[6])
            creature_template_quest_relation_ID = int(creature_template_info[7])

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
    :return: A list of Quest objects
    """

    quest_list = []

    # populate list
    print("Loading Quests...")
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()
        quests_reader = cursor.execute("SELECT * FROM quest_template WHERE zone = ? AND sub_zone = ?", [zone, subzone])

        for row in quests_reader.fetchall():
            # save the quest information
            quest_entry = int(row[0])
            quest_name = row[1]
            quest_level_requirement = int(row[2])
            quest_monster_required = row[3]  # monster name
            quest_monster_kill_amount_required = int(row[4])
            # row[5] = zone
            # row[6] = sub_zone
            quest_xp_reward = int(row[7])
            # row[8] = comment

            quest_list.append(Quest(quest_name= quest_name,
                                    quest_id=quest_entry,
                                    creature_name=quest_monster_required,
                                    kill_amount=quest_monster_kill_amount_required,
                                    xp_reward=quest_xp_reward,
                                    level_required=quest_level_requirement))

    return quest_list
