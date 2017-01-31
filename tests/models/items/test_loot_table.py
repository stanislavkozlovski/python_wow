import unittest

import database.main
from tests.create_test_db import engine, session, Base
database.main.engine = engine
database.main.session = session
database.main.Base = Base

import models.main
from items import Item, Potion, Weapon
from buffs import BeneficialBuff
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

    def test_decide_drops(self):
        """
        Test the decide drops function by calling it multiple times until
        all the items drop
        """
        l_table = session.query(LootTableSchema).get(self.loot_table_entry)
        self.expected_item1 = Item(name='Linen Cloth', item_id=self.item_1, buy_price=1, sell_price=1)
        self.effect: BeneficialBuff = BeneficialBuff(name="Heart of a Lion",
                                                     buff_stats_and_amounts=[('strength', 15)],
                                                     duration=5)
        self.expected_item2 = Potion(name='Strength Potion', item_id=4, buy_price=1,
                                     sell_price=1, buff=self.effect, quest_id=0)
        self.expected_item3 = Weapon(name='Worn Axe', item_id=3,
                                    buy_price=1, sell_price=1, min_damage=2, max_damage=6,
                                    attributes={'bonus_health': 0, 'bonus_mana': 0, 'armor': 0, 'strength': 0, 'agility': 0})

        received_items_count = 0
        for _ in range(100):
            drops: [Item] = l_table.decide_drops()
            for drop in drops:
                equal_to_one_of_the_three_items = (drop == self.expected_item1
                                                   or drop == self.expected_item2
                                                   or drop == self.expected_item3)
                self.assertTrue(equal_to_one_of_the_three_items)
                received_items_count += 1

        self.assertGreater(received_items_count, 10)


if __name__ == '__main__':
    unittest.main()
