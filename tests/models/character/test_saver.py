import unittest
from unittest import mock

import database.main
from tests.create_test_db import engine, session, Base
database.main.engine = engine
database.main.session = session
database.main.Base = Base
import models.main

from classes import Paladin
from models.characters.saved_character import SavedCharacterSchema
from models.items.item_template import ItemTemplateSchema
from tests.models.character.character_mock import character, char_equipment, entry
from models.characters.saver import save_character, save_loaded_scripts, save_killed_monsters, save_completed_quests, save_inventory
from models.characters.saved_character import LoadedScriptsSchema, KilledMonstersSchema, CompletedQuestsSchema, InventorySchema

class SavedCharacterSaverTests(unittest.TestCase):
    """
    Get the Mock character, change his name and try to save him in the DB
    """
    def setUp(self):
        self.expected_character = character
        # Expected Character has no completed quests, so add some
        self.expected_character.completed_quests.add(2)
        self.expected_character.name = 'Tester'

    def test_save_character(self):
        save_character(self.expected_character)
        received_character = session.query(SavedCharacterSchema).filter_by(name=self.expected_character.name).first()
        self.assertIsNotNone(received_character)
        received_character = received_character.convert_to_character_object()

        self.assertIsNotNone(received_character)
        self.assertTrue(isinstance(received_character, Paladin))

        # Separately test out the inventory and equipment, because they do not compare well in the
        # overall vars() assert equal, even though the Item object has an __eq__ method
        received_eq = received_character.equipment
        char_eq = self.expected_character.equipment
        self.assertCountEqual(received_eq, char_eq)
        received_character.equipment = None
        self.expected_character.equipment = None

        received_inv = received_character.inventory
        char_inv = self.expected_character.inventory
        self.assertCountEqual(received_inv, char_inv)
        received_character.inventory = None
        self.expected_character.inventory = None

        received_wep = received_character.equipped_weapon
        expected_wep = self.expected_character.equipped_weapon
        self.assertEqual(received_wep.name, expected_wep.name)
        received_character.equipped_weapon = None
        self.expected_character.equipped_weapon = None

        # assert they're the same
        self.assertEqual(vars(received_character), vars(self.expected_character))

    def test_save_loaded_scripts(self):
        test_char_id = 133
        loaded_scripts = {'The Beat is too low', 'and the vocals too loud'}
        save_loaded_scripts(test_char_id, loaded_scripts)

        loaded_scripts_count = session.query(LoadedScriptsSchema).filter_by(saved_character_id=test_char_id).count()
        self.assertEqual(loaded_scripts_count, len(loaded_scripts))

    def test_save_killed_monsters(self):
        test_char_id = 147
        killed_monsters_guids = {109, 111, 131, 149, 13141}
        save_killed_monsters(test_char_id, killed_monsters_guids)

        killed_monsters_count = session.query(KilledMonstersSchema).filter_by(saved_character_id=test_char_id).count()
        self.assertEqual(killed_monsters_count, len(killed_monsters_guids))

    def test_save_completed_quests(self):
        test_char_id = 94
        completed_quests_ids = {9, 10, 12, 13}
        save_completed_quests(test_char_id, completed_quests_ids)

        completed_quests_count = session.query(CompletedQuestsSchema).filter_by(saved_character_id=test_char_id).count()
        self.assertEqual(completed_quests_count, len(completed_quests_ids))

    def test_save_inventory(self):
        item1_mock = mock.Mock(id=1)
        item2_mock = mock.Mock(id=2)
        item3_mock = mock.Mock(id=3)
        inventory_mock = {
            "Digital": (item1_mock, 1),
            "GetRid": (item2_mock, 2),
            "Bra": (item3_mock, 1)
        }
        test_char_id = 94
        save_inventory(test_char_id, inventory_mock)

        saved_inventory_count = session.query(InventorySchema).filter_by(saved_character_id=test_char_id).count()
        self.assertEqual(saved_inventory_count, len(inventory_mock.keys()))


def tearDownModule():
    import tests.delete_test_db  # module that deletes the DB :)

if __name__ == '__main__':
    unittest.main()
