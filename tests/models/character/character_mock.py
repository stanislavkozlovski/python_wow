from tests.create_test_db import engine, session, Base
from constants import (CHARACTER_EQUIPMENT_BOOTS_KEY, CHARACTER_EQUIPMENT_LEGGINGS_KEY,
                       CHARACTER_EQUIPMENT_BELT_KEY, CHARACTER_EQUIPMENT_GLOVES_KEY,
                       CHARACTER_EQUIPMENT_BRACER_KEY,
                       CHARACTER_EQUIPMENT_CHESTGUARD_KEY, CHARACTER_EQUIPMENT_HEADPIECE_KEY,
                       CHARACTER_EQUIPMENT_NECKLACE_KEY,
                       CHARACTER_EQUIPMENT_SHOULDERPAD_KEY)
from models.items.item_template import ItemTemplateSchema
from classes import Paladin
from items import Potion, Item


entry = 1
name = 'Netherblood'
class_ = 'paladin'
gold = 61
level = 3
headpiece_id = 11
shoulderpad_id = 12
necklace_id = 14
chestguard_id = 13

chestguard = session.query(ItemTemplateSchema).get(chestguard_id).convert_to_item_object()
shoulderpad = session.query(ItemTemplateSchema).get(shoulderpad_id).convert_to_item_object()
necklace = session.query(ItemTemplateSchema).get(necklace_id).convert_to_item_object()
headpiece = session.query(ItemTemplateSchema).get(headpiece_id).convert_to_item_object()
# IMPORTANT: Arrange the equipment as it is arranged in the build_equipment function in the loader exactly!
char_equipment = {CHARACTER_EQUIPMENT_BOOTS_KEY: None,
                   CHARACTER_EQUIPMENT_LEGGINGS_KEY: None,
                   CHARACTER_EQUIPMENT_BELT_KEY: None,
                   CHARACTER_EQUIPMENT_GLOVES_KEY: None,
                   CHARACTER_EQUIPMENT_BRACER_KEY: None,
                   CHARACTER_EQUIPMENT_CHESTGUARD_KEY: chestguard,
                   CHARACTER_EQUIPMENT_SHOULDERPAD_KEY: shoulderpad,
                   CHARACTER_EQUIPMENT_NECKLACE_KEY: necklace,
                   CHARACTER_EQUIPMENT_HEADPIECE_KEY: headpiece}

char_inventory: {str: (Item, int)} = {
    'gold': gold,
    'Crimson Defias Bandana': (session.query(ItemTemplateSchema).get(11).convert_to_item_object(), 5),
    'Wolf Meat': (session.query(ItemTemplateSchema).get(1).convert_to_item_object(), 5),
    'Wolf Pelt': (session.query(ItemTemplateSchema).get(2).convert_to_item_object(), 3),
    'Blackened Defias Shoulderpad': (session.query(ItemTemplateSchema).get(12).convert_to_item_object(), 1),
    'Linen Cloth': (session.query(ItemTemplateSchema).get(10).convert_to_item_object(), 1),
    "Garrick's Head": (session.query(ItemTemplateSchema).get(9).convert_to_item_object(), 1),
    'Stolen Necklace': (session.query(ItemTemplateSchema).get(14).convert_to_item_object(), 1),
    'Strength Potion': (session.query(ItemTemplateSchema).get(4).convert_to_item_object(), 1)
}
# NOTE: test might fail due to the way we stack up armor in regards to agility and the formula.
# if we have two items and we first equip an item with high agility we will get more armor
# as opposed to one with less first
loaded_scripts = {'HASKEL_PAXTON_CONVERSATION'}
completed_quests = {1}
killed_monsters = {14, 15, 20}
character = Paladin(name=name, level=level, loaded_scripts=loaded_scripts, killed_monsters=killed_monsters,
                        completed_quests=completed_quests, saved_inventory=char_inventory, saved_equipment=char_equipment)