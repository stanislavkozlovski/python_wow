import unittest

import database.main
from tests.create_test_db import engine, session, Base
database.main.engine = engine
database.main.session = session
database.main.Base = Base

import models.main
from classes import Paladin
from exceptions import NoSuchCharacterError
from models.characters.loader import load_saved_character
from tests.models.character.character_mock import character


class LoaderTests(unittest.TestCase):
    def setUp(self):
        self.character = character

    def test_load_valid_character(self):
        loaded_char = load_saved_character(character.name)
        self.assertIsNotNone(loaded_char)
        self.assertTrue(isinstance(loaded_char, Paladin))

        # Separately test out the inventory and equipment, because they do not compare well in the
        # overall vars() assert equal, even though the Item object has an __eq__ method
        received_eq = loaded_char.equipment
        char_eq = self.character.equipment
        self.assertCountEqual(received_eq, char_eq)
        loaded_char.equipment = None
        self.character.equipment = None

        received_inv = loaded_char.inventory
        char_inv = self.character.inventory
        self.assertCountEqual(received_inv, char_inv)
        loaded_char.inventory = None
        self.character.inventory = None

        self.assertEqual(vars(loaded_char), vars(self.character))

    def test_load_invalid_character(self):
        invalid_name = 'AaAa'
        expected_message = f'There is no saved character by the name of {invalid_name}!'
        try:
            load_saved_character(invalid_name)
            self.fail('The test should have raised a NoSuchCharacterError!')
        except NoSuchCharacterError as e:
            self.assertEqual(str(e), expected_message)


def tearDownModule():
    import tests.delete_test_db  # module that deletes the DB :)

if __name__ == '__main__':
    unittest.main()
