import unittest

import database.main
from tests.create_test_db import engine, session, Base
database.main.engine = engine
database.main.session = session
database.main.Base = Base
import models.main
from models.creatures.creature_template import CreatureTemplateSchema
from models.creatures.npc_vendor import NpcVendorSchema
from models.items.loot_table import LootTableSchema
from models.items.item_template import ItemTemplateSchema


class CreatureTemplateTests(unittest.TestCase):
    def setUp(self):
        """
        Self dummy is Meatseller Jack
        """
        self.dummy_entry = 14
        self.dummy_name = "Meatseller Jack"
        self.dummy_type = "vendor"
        self.dummy_level = 4
        self.dummy_health = 20
        self.dummy_mana = 0
        self.dummy_armor = 0
        self.dummy_min_damage = 5
        self.dummy_max_damage = 10
        self.dummy_quest_relation_id = 0
        self.dummy_loot_table_id = 0
        self.dummy_gossip = "Do you want to buy meat? You've come to the right place!"
        self.dummy_respawnable = True
        item_for_sale = session.query(ItemTemplateSchema).get(1).convert_to_item_object()
        item_for_sale.buy_price = 1
        self.dummy_inventory = {"Wolf Meat": (item_for_sale, 10)}

    def test_creature_template_values(self):
        dummy: CreatureTemplateSchema = session.query(CreatureTemplateSchema).get(self.dummy_entry)
        self.assertEqual(self.dummy_entry, dummy.entry)
        self.assertEqual(self.dummy_name, dummy.name)
        self.assertEqual(self.dummy_type, dummy.type)
        self.assertEqual(self.dummy_level, dummy.level)
        self.assertEqual(self.dummy_health, dummy.health)
        self.assertEqual(self.dummy_mana, dummy.mana)
        self.assertEqual(self.dummy_quest_relation_id, dummy.quest_relation_id)
        self.assertEqual(self.dummy_loot_table_id, dummy.loot_table_id)
        self.assertIsNone(dummy.loot_table)
        self.assertEqual(self.dummy_armor, dummy.armor)
        self.assertEqual(self.dummy_min_damage, dummy.min_dmg)
        self.assertEqual(self.dummy_max_damage, dummy.max_dmg)
        self.assertEqual(self.dummy_gossip, dummy.gossip)
        self.assertEqual(self.dummy_respawnable, dummy.respawnable)
        self.assertEqual(len(dummy.vendor_inventory), 1)
        self.assertTrue(isinstance(dummy.vendor_inventory[0], NpcVendorSchema))

    def test_build_inventory_with_vendor_npc(self):
        """
        The build_inventory function should create a dictionary of the inventory
        of the vendor. It does so by linking every NpcVendor entry with a foreign
        key to the creature_template row
        """
        vendor_dummy: CreatureTemplateSchema = session.query(CreatureTemplateSchema).get(self.dummy_entry)
        received_inventory = vendor_dummy.build_vendor_inventory()
        self.assertEqual(self.dummy_inventory, received_inventory)

    def test_build_inventory_with_non_vendor_npc(self):
        """
        Test the build_inventory function with an NPC who does not have any links to the
        NpcVendor DB table
        """
        non_vendor_dummy: CreatureTemplateSchema = session.query(CreatureTemplateSchema).get(1)
        received_inventory = non_vendor_dummy.build_vendor_inventory()
        self.assertEqual(received_inventory, {})


def tearDownModule():
    import tests.delete_test_db  # module that deletes the DB :)

if __name__ == '__main__':
    main()
