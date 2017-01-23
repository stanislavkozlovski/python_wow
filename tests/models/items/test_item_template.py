import unittest

from tests.delete_test_db import delete_test_db  # module that deletes the DB :)
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
from buffs import BeneficialBuff

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
        self.assertIsNotNone(received_item)
        self.assertTrue(isinstance(received_item, Item))
        self.assertEqual(vars(received_item), vars(self.expected_item))


class ItemTemplateWeaponItemTests(unittest.TestCase):
    """
    Load an ItemTemplate schema and convert it to a Weapon object
    """
    def setUp(self):
        self.item_entry = 3
        self.name = 'Worn Axe'
        self.type = 'weapon'
        self.buy_price = 1
        self.attributes = {
            'bonus_health': 0,
            'bonus_mana': 0,
            'armor': 0,
            'strength': 0,
            'agility': 0

        }
        self.sell_price = 1
        self.quest_id = 0
        self.min_damage = 2
        self.max_damage = 6
        self.expected_item = Weapon(name=self.name, item_id=self.item_entry,
                                    buy_price=self.buy_price, sell_price=self.sell_price,
                                    min_damage=self.min_damage, max_damage=self.max_damage,
                                    attributes_dict=self.attributes)

    def test_convert_to_item_object(self):
        received_item = session.query(ItemTemplateSchema).get(self.item_entry).convert_to_item_object()
        self.assertIsNotNone(received_item)
        self.assertTrue(isinstance(received_item, Weapon))
        self.assertEqual(vars(received_item), vars(self.expected_item))


class ItemTemplatePotionItemTests(unittest.TestCase):
    """
    Load an ItemTemplate schema object and convert it to a Potion object
    """
    def setUp(self):
        self.item_entry = 4
        self.name = 'Strength Potion'
        self.buy_price = 1
        self.sell_price = 1
        self.effect_id = 1
        self.effect: BeneficialBuff = BeneficialBuff(name="Heart of a Lion",
                                                     buff_stats_and_amounts=[('strength', 15)],
                                                     duration=5)
        self.potion = Potion(name=self.name, item_id=self.item_entry, buy_price=self.buy_price, sell_price=self.sell_price,
                             buff=self.effect, quest_id=0)

    def test_convert_to_item_object(self):
        received_item: Potion = session.query(ItemTemplateSchema).get(self.item_entry).convert_to_item_object()

        self.assertIsNotNone(received_item)
        self.assertTrue(isinstance(received_item, Potion))
        self.assertEqual(vars(received_item), vars(self.potion))


def tearDownModule():
    delete_test_db()


if __name__ == '__main__':
    unittest.main()
