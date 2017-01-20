import unittest

import database.main
from tests.create_test_db import engine, session, Base
database.main.engine = engine
database.main.session = session
database.main.Base = Base

import models.main
from models.items.loot_table import LootTableSchema
from models.items.item_template import ItemTemplateSchema

class LootTableSchemaTests(unittest.TestCase):
    def setUp(self):
        self.loot_table_entry = 2
        self.item_1 = 10
        self.item_1_chance = 20
        self.item_2 = 4
        self.item_2_chance = 10
        self.item_3 = 3
        self.item_3_chance = 15

    def test_values(self):
        loot_schema: LootTableSchema = session.query(LootTableSchema).get(self.loot_table_entry)
        self.assertEqual(self.item_1, loot_schema.item1_id)
        self.assertEqual(self.item_1_chance, loot_schema.item1_chance)
        self.assertTrue(isinstance(loot_schema.item1, ItemTemplateSchema))

        self.assertEqual(self.item_2, loot_schema.item2_id)
        self.assertEqual(self.item_2_chance, loot_schema.item2_chance)
        self.assertTrue(isinstance(loot_schema.item2, ItemTemplateSchema))

        self.assertEqual(self.item_3, loot_schema.item3_id)
        self.assertEqual(self.item_3_chance, loot_schema.item3_chance)
        self.assertTrue(isinstance(loot_schema.item3, ItemTemplateSchema))

        for i in range(4, 21):
            item_id = getattr(loot_schema, f'item{i}_id')
            item_chance = getattr(loot_schema, f'item{i}_chance')
            item_obj = getattr(loot_schema, f'item{i}')
            
            self.assertFalse(item_id)
            self.assertFalse(item_chance)
            self.assertIsNone(item_obj)


def tearDownModule():
    import tests.delete_test_db  # module that deletes the DB :)


if __name__ == '__main__':
    unittest.main()
