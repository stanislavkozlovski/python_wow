import unittest

from tests.delete_test_db import delete_test_db  # module that deletes the DB :)
import database.main
from tests.create_test_db import engine, session, Base
database.main.engine = engine
database.main.session = session
database.main.Base = Base
import models.main
from models.creatures.npc_vendor import NpcVendorSchema
from models.items.item_template import ItemTemplateSchema


class NpcVendorTests(unittest.TestCase):
    def setUp(self):
        """ There is only one entry in this table """
        self.dummy_creature_entry = 14
        self.dummy_item_id = 1
        self.dummy_item_count = 10
        self.dummy_price = 1
        self.expected_tablename = 'npc_vendor'

    def test_npc_vendor_values(self):
        received_dummy = session.query(NpcVendorSchema).get(self.dummy_creature_entry)
        self.assertEqual(received_dummy.__tablename__, self.expected_tablename)
        self.assertEqual(received_dummy.item_id, self.dummy_item_id)
        self.assertEqual(received_dummy.item_count, self.dummy_item_count)
        self.assertEqual(received_dummy.price, self.dummy_price)

        self.assertIsNotNone(received_dummy.item)
        self.assertTrue(isinstance(received_dummy.item, ItemTemplateSchema))

        vendor_item_in_db = session.query(ItemTemplateSchema).get(self.dummy_item_id)
        self.assertEqual(received_dummy.item, vendor_item_in_db)


def tearDownModule():
    delete_test_db()

if __name__ == '__main__':
    unittest.main()
