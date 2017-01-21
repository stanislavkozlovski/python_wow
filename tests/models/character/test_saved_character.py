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


class SavedCharacterTests(unittest.TestCase):
    """
    These tests rely on the ItemTemplateSchema correctly querying and converting item objects.
    """
    def setUp(self):
        """
        The saved character is Netherblood
        """
        self.entry = entry
        self.char_equipment = char_equipment
        self.character = character

    def test_build_equipment(self):
        received_eq = session.query(SavedCharacterSchema).get(self.entry).build_equipment()
        self.assertCountEqual(received_eq, self.char_equipment)

    def test_convert_to_character_object(self):
        received_char = session.query(SavedCharacterSchema).get(self.entry).convert_to_character_object()
        self.assertIsNotNone(received_char)
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
