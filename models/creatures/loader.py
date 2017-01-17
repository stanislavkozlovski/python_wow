""" This module loads information from the associated models in its folder """
from sqlalchemy import or_, and_

from database.main import session
from models.creatures.creatures import CreaturesSchema
from entities import Monster, LivingThing, VendorNPC


def load_monsters(zone: str, subzone: str, character) -> tuple:
    """
    Loads all the creatures in the given zone

        :return: A Dictionary: Key: guid, Value: Object of class entities.py/Monster,
                 A Set of Tuples ((Monster GUID, Monster Name))
    """

    monsters_dict: {int: Monster} = {}
    guid_name_set: {(int, str)} = set()

    print("Loading Monsters...")
    creatures = session.query(CreaturesSchema).filter_by(type='monster', zone=zone, sub_zone=subzone).all()
    for creature in creatures:
        if character.has_killed_monster(creature.guid):
            # if the character has killed this monster before and has it saved, we don't want to load it
            continue

        monster = creature.convert_to_living_thing_object()

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
    loaded_npcs = session.query(CreaturesSchema).filter(((CreaturesSchema.type == 'fnpc') | (CreaturesSchema.type == 'vendor')
                                                         & (CreaturesSchema.zone == zone) & (CreaturesSchema.sub_zone == subzone)))
    for npc_info in loaded_npcs:
        guid: int = npc_info.guid
        loaded_npc = npc_info.convert_to_living_thing_object()
        guid_name_set.add((guid, loaded_npc.name))
        npcs_dict[guid] = loaded_npc

    print("Friendly NPCs loaded!")
    return npcs_dict, guid_name_set
