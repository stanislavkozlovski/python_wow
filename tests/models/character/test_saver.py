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
        self.expected_character.name = 'Tester'

    def test_save_character(self):
        save_character(self.expected_character)
        received_character = session.query(SavedCharacterSchema).filter_by(name=self.expected_character.name).first()
        self.assertIsNotNone(received_character)
        received_character = received_character.convert_to_character_object()

        # assert they're the same
        self.assertEqual(vars(received_character), vars(self.expected_character))


def tearDownModule():
    import tests.delete_test_db  # module that deletes the DB :)

if __name__ == '__main__':
    unittest.main()
