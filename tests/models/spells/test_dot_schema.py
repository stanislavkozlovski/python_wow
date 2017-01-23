import unittest

from tests.delete_test_db import delete_test_db  # module that deletes the DB :)
import database.main
from tests.create_test_db import engine, session, Base


database.main.engine = engine
database.main.session = session
database.main.Base = Base

import models.main
from models.spells.spell_dots import DotSchema
from buffs import DoT
from damage import Damage


class DotSchemaTests(unittest.TestCase):
    def setUp(self):
        """
        Test that the DotSchema attributes are as expected
        Test the convert_to_dot_object function
        """
        self.entry = 1
        self.name = 'Melting'
        self.damage = Damage(magic_dmg=2)
        self.duration = 2

    def test_schema_attributes(self):
        loaded_schema: DotSchema = session.query(DotSchema).get(self.entry)

        self.assertIsNotNone(loaded_schema)

        self.assertTrue(loaded_schema.entry, int)
        self.assertTrue(loaded_schema.name, str)
        self.assertTrue(loaded_schema.damage_per_tick, int)
        self.assertTrue(loaded_schema.damage_school, str)
        self.assertTrue(loaded_schema.duration, int)
        self.assertTrue(loaded_schema.comment, str)


def tearDownModule():
    delete_test_db()

if __name__ == '__main__':
    unittest.main()
