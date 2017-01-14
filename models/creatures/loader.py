""" This module loads information from the associated models in its folder """
from sqlalchemy import or_, and_

from database.main import session
from models.creatures.creatures import Creatures
from entities import Monster, LivingThing, VendorNPC


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


def load_npcs(zone: str, subzone: str) -> tuple:
    """
    Load all the friendly NPCs in the given zone/subzone


        :return: A Dictionary: Key: guid, Value: Object of class entities.py/FriendlyNPC,
                 A Set of Tuples ((npc GUID, npc Name))
    """

    npcs_dict: {str: 'FriendlyNPC' or 'VendorNPC'} = {}
    guid_name_set: {(int, str)} = set()

    print("Loading Friendly NPCs...")
    loaded_npcs = session.query(Creatures).filter(((Creatures.type == 'fnpc') | (Creatures.type == 'vendor')
                                                   & (Creatures.zone == zone) & (Creatures.sub_zone == subzone)))
    for npc_info in loaded_npcs:
        guid: int = npc_info.guid
        loaded_npc = npc_info.convert_to_living_thing_object()
        guid_name_set.add((guid, loaded_npc.name))
        npcs_dict[guid] = loaded_npc

    print("Friendly NPCs loaded!")
    return npcs_dict, guid_name_set
