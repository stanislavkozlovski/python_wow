import unittest

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
from models.characters.saver import save_character


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


def tearDownModule():
    import tests.delete_test_db  # module that deletes the DB :)

if __name__ == '__main__':
    unittest.main()
