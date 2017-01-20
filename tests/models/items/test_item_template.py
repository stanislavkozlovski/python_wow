import unittest

import database.main
from tests.create_test_db import engine, session, Base
database.main.engine = engine
database.main.session = session
database.main.Base = Base

import models.main
from models.items.loot_table import LootTableSchema
from models.items.item_template import ItemTemplateSchema
from models.quests.quest_template import QuestSchema
from items import Item, Weapon, Equipment, Potion


class ItemTemplateMiscItemTests(unittest.TestCase):
    def setUp(self):
        self.item_entry = 2
        self.name = 'Wolf Pelt'
        self.type = 'misc'
        self.buy_price = 1
        self.sell_price = 1
        self.quest_id = 0
        self.expected_item = Item(name=self.name, item_id=self.item_entry,
                                  buy_price=self.buy_price, sell_price=self.sell_price,
                                  quest_id=self.quest_id)

    def test_convert_to_item_object(self):
        received_item = session.query(ItemTemplateSchema).get(2)
        received_item = received_item.convert_to_item_object()
        self.assertEqual(vars(received_item), vars(self.expected_item))


def tearDownModule():
    import tests.delete_test_db  # module that deletes the DB :)

if __name__ == '__main__':
    unittest.main()
