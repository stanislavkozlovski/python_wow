import unittest

import database.main
from tests.create_test_db import engine, session, Base
database.main.engine = engine
database.main.session = session
database.main.Base = Base
import models.main
from classes import Paladin
from constants import (CHARACTER_EQUIPMENT_BOOTS_KEY, CHARACTER_EQUIPMENT_LEGGINGS_KEY,
                       CHARACTER_EQUIPMENT_BELT_KEY, CHARACTER_EQUIPMENT_GLOVES_KEY,
                       CHARACTER_EQUIPMENT_BRACER_KEY,
                       CHARACTER_EQUIPMENT_CHESTGUARD_KEY, CHARACTER_EQUIPMENT_HEADPIECE_KEY,
                       CHARACTER_EQUIPMENT_NECKLACE_KEY,
                       CHARACTER_EQUIPMENT_SHOULDERPAD_KEY)
from models.characters.saved_character import SavedCharacterSchema
from models.items.item_template import ItemTemplateSchema
from items import Equipment, Item


class SavedCharacterTests(unittest.TestCase):
    """
    These tests rely on the ItemTemplateSchema correctly querying and converting item objects.
    """
    def setUp(self):
        """
        The saved character is Netherblood
        """
        self.entry = 1
        self.name = 'Netherblood'
        self.class_ = 'paladin'
        self.gold = 61
        self.level = 3
        self.headpiece_id = 11
        self.shoulderpad_id = 12
        self.necklace_id = 14
        self.chestguard_id = 13

        self.chestguard = session.query(ItemTemplateSchema).get(self.chestguard_id).convert_to_item_object()
        self.shoulderpad = session.query(ItemTemplateSchema).get(self.shoulderpad_id).convert_to_item_object()
        self.necklace = session.query(ItemTemplateSchema).get(self.necklace_id).convert_to_item_object()
        self.headpiece = session.query(ItemTemplateSchema).get(self.headpiece_id).convert_to_item_object()
        # IMPORTANT: Arrange the equipment as it is arranged in the build_equipment function in the loader exactly!
        self.char_equipment = {CHARACTER_EQUIPMENT_BOOTS_KEY: None,
                               CHARACTER_EQUIPMENT_LEGGINGS_KEY: None,
                               CHARACTER_EQUIPMENT_BELT_KEY: None,
                               CHARACTER_EQUIPMENT_GLOVES_KEY: None,
                               CHARACTER_EQUIPMENT_BRACER_KEY: None,
                               CHARACTER_EQUIPMENT_CHESTGUARD_KEY: self.chestguard,
                               CHARACTER_EQUIPMENT_SHOULDERPAD_KEY: self.shoulderpad,
                               CHARACTER_EQUIPMENT_NECKLACE_KEY: self.necklace,
                               CHARACTER_EQUIPMENT_HEADPIECE_KEY: self.headpiece}

        self.char_inventory: {str: (Item, int)} = {
            'gold': self.gold,
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
        self.loaded_scripts = {'HASKEL_PAXTON_CONVERSATION'}
        self.completed_quests = set()
        self.killed_monsters = {14, 15, 20}
        self.character = Paladin(name=self.name, level=self.level, loaded_scripts=self.loaded_scripts, killed_monsters=self.killed_monsters,
                            completed_quests=self.completed_quests, saved_inventory=self.char_inventory, saved_equipment=self.char_equipment)

    def test_convert_to_character_object(self):
        received_char = session.query(SavedCharacterSchema).get(self.entry).convert_to_character_object()
        self.assertIsNotNone(received_char)
        self.maxDiff = None
        self.assertTrue(isinstance(received_char, Paladin))

        # Separately test out the inventory and equipment, because they do not compare well in the
        # overall vars() assert equal, even though the Item object has an __eq__ method
        received_eq = received_char.equipment
        char_eq = self.character.equipment
        self.assertCountEqual(received_eq, char_eq)
        received_char.equipment = None
        self.character.equipment = None

        received_inv = received_char.inventory
        char_inv = self.character.inventory
        self.assertCountEqual(received_inv, char_inv)
        received_char.inventory = None
        self.character.inventory = None

        self.assertEqual(vars(received_char), vars(self.character))


def tearDownModule():
    import tests.delete_test_db  # module that deletes the DB :)

if __name__ == '__main__':
    unittest.main()
