import unittest

import database.main
from tests.create_test_db import engine, session, Base, connection, cursor

database.main.engine = engine
database.main.session = session
database.main.Base = Base

import models.main
from models.creatures.creature_defaults.loader import load_creature_defaults


class LoaderTests(unittest.TestCase):
    """
    Tests for the loader of creature default variables
    """
    def test_loader_valid_results(self):
        """
        Load the creature defaults and assert they're as expected.
        """
        expected_defaults = cursor.execute("SELECT * FROM creature_defaults").fetchall()

        received_defaults = load_creature_defaults()
        self.assertIsNotNone(received_defaults)
        # order the keys so that we can test them one by one
        ordered_expected_defaults = sorted(expected_defaults, key=lambda x: x['creature_level'])
        ordered_level_keys = sorted(received_defaults.keys())

        self.assertEqual(len(ordered_expected_defaults), len(ordered_level_keys))
        for idx, received_key in enumerate(ordered_level_keys):
            received_default = received_defaults[received_key]
            expected_default = dict(ordered_expected_defaults[idx])

            del expected_default['creature_level']  # the received default does not have this intentionally

            self.assertCountEqual(received_default, expected_default)


def tearDownModule():
    import tests.delete_test_db

if __name__ == '__main__':
    unittest.main()