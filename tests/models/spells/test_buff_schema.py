import unittest

from tests.delete_test_db import delete_test_db  # module that deletes the DB :)
import database.main
from tests.create_test_db import engine, session, Base


database.main.engine = engine
database.main.session = session
database.main.Base = Base

import models.main
from models.spells.spell_buffs import BuffSchema
from buffs import BeneficialBuff
from damage import Damage


class BuffSchemaTests(unittest.TestCase):
    def setUp(self):
        """
        Test that the BuffSchema's values are as expected
        Test that the convert_to_beneficial_buff_object function works as expected
        """
        self.buff_entry = 1
        self.name = 'Heart of a Lion'
        self.duration = 5
        self.expected_buff = BeneficialBuff(name="Heart of a Lion",
                                            buff_stats_and_amounts=[('strength', 15)],
                                            duration=5)

    def test_schema_values(self):
        loaded_schema: BuffSchema = session.query(BuffSchema).get(self.buff_entry)
        self.assertTrue(isinstance(loaded_schema, BuffSchema))
        self.assertTrue(isinstance(loaded_schema.entry, int))
        self.assertTrue(isinstance(loaded_schema.name, str))
        self.assertTrue(isinstance(loaded_schema.duration, int))
        self.assertTrue(isinstance(loaded_schema.stat1, str))
        self.assertTrue(isinstance(loaded_schema.amount1, int))
        self.assertIsNone(loaded_schema.stat2)
        self.assertIsNone(loaded_schema.amount2)
        self.assertIsNone(loaded_schema.stat3)
        self.assertIsNone(loaded_schema.amount3)
        self.assertTrue(isinstance(loaded_schema.comment, str))

    def test_convert_to_beneficial_buff_object(self):
        loaded_buff: BeneficialBuff = session.query(BuffSchema).get(self.buff_entry).convert_to_beneficial_buff_object()
        self.assertEqual(vars(loaded_buff), vars(self.expected_buff))


def tearDownModule():
    delete_test_db()

if __name__ == '__main__':
    unittest.main()
