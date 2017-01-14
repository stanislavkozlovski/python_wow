""" This module loads information from the associated models in its folder """
from database.main import session
from models.creatures.creatures import Creatures
from entities import Monster


def load_monsters(zone: str, subzone: str, character) -> tuple:
    """
    Loads all the creatures in the given zone

        :return: A Dictionary: Key: guid, Value: Object of class entities.py/Monster,
                 A Set of Tuples ((Monster GUID, Monster Name))
    """
    from entities import Monster  # needed to be imported here otherwise we end up in an import loop

    monsters_dict = {}
    guid_name_set = set()

    print("Loading Monsters...")
    creatures = session.query(Creatures).filter_by(type='monster', zone=zone, sub_zone=subzone).all()
    for creature in creatures:
        if character.has_killed_monster(creature.guid):
            # if the character has killed this monster before and has it saved, we don't want to load it
            continue

        creature_info = creature.creature
        monster = Monster(monster_id=creature_info.entry,
                          name=creature_info.name,
                          health=creature_info.health,
                          mana=creature_info.mana,
                          level=creature_info.level,
                          min_damage=creature_info.min_dmg,
                          max_damage=creature_info.max_dmg,
                          quest_relation_id=creature_info.quest_relation_id,
                          loot_table_ID=creature_info.loot_table_id,
                          gossip=creature_info.gossip,
                          respawnable=creature_info.respawnable)

        guid_name_set.add((creature.guid, monster.name))
        monsters_dict[creature.guid] = monster

    print("Monsters loaded!")
    return monsters_dict, guid_name_set
