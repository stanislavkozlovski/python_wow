import unittest

from tests.delete_test_db import delete_test_db  # module that deletes the DB :)
import database.main
from tests.create_test_db import engine, session, Base

database.main.engine = engine
database.main.session = session
database.main.Base = Base

import models.main
from models.creatures.creature_template import CreatureTemplateSchema
from models.creatures.creatures import CreaturesSchema
from models.items.loot_table import LootTableSchema
from entities import Monster, FriendlyNPC, VendorNPC
from items import Item


class CreaturesMonsterTests(unittest.TestCase):
    def setUp(self):
        """
        Test loading three different types of monsters - vendor, fnpc, monster
        """
        self.monster_entry = 16
        self.monster_guid = 15
        self.monster_type = 'monster'
        self.monster_zone = 'Northshire Abbey'
        self.monster_subzone = 'A Peculiar Hut'
        self.monster_gold_range = range(5, 9)
        self.monster_respawnable = False
        self.monster = Monster(monster_id=self.monster_entry, name="Brother Paxton", health=25, mana=0, armor=80, level=3,
                               min_damage=7, max_damage=10, quest_relation_id=0, xp_to_give=100,
                               gold_to_give_range=(5, 8), loot_table=None, gossip="Nobody will foil our plans!")

    def test_schema_values(self):
        """ Load the schema and assert it's as expected """
        loaded_creature: CreaturesSchema = session.query(CreaturesSchema).get(self.monster_guid)

        self.assertEqual(loaded_creature.guid, self.monster_guid)
        self.assertEqual(loaded_creature.creature_id, self.monster_entry)
        self.assertEqual(loaded_creature.zone, self.monster_zone)
        self.assertEqual(loaded_creature.sub_zone, self.monster_subzone)

        self.assertIsNotNone(loaded_creature.creature)
        self.assertTrue(isinstance(loaded_creature.creature, CreatureTemplateSchema))

    def test_convert_to_living_thing_object_monster(self):
        """
        Converting a CreaturesSchema with a type of 'monster' should convert it to a Monster object
        """
        converted_monster = session.query(CreaturesSchema).get(self.monster_guid).convert_to_living_thing_object()
        self.assertTrue(isinstance(converted_monster, Monster))
        # See that it has a loot table
        self.assertTrue(isinstance(converted_monster.loot_table, LootTableSchema))
        self.assertTrue(converted_monster.loot['gold'] in self.monster_gold_range)
        # assert that the expected monster and the one we have are equal
        converted_monster.loot_table = None  # remove the loot table for easier testing
        # These things hold gold which is randomized per monster
        converted_monster.loot = None
        converted_monster._gold_to_give = None
        self.monster.loot = None
        self.monster._gold_to_give = None
        self.assertEqual(vars(converted_monster), vars(self.monster))


class CreaturesFriendlyNpcTests(unittest.TestCase):
    def setUp(self):
        self.npc_entry = 13
        self.npc_guid = 7
        self.npc_type = 'fnpc'
        self.npc_zone = 'Northshire Abbey'
        self.npc_subzone = 'Northshire Valley'
        self.npc_respawnable = True
        self.npc = FriendlyNPC(name='Lumberjack Joe', health=25, mana=0, level=5, min_damage=10, max_damage=15,
                               quest_relation_id=0, loot_table=None,
                               gossip='Hey there $N, fancy helping me cut down this tree over here?')

    def test_schema_values(self):
        loaded_npc: CreaturesSchema = session.query(CreaturesSchema).get(self.npc_guid)
        self.assertEqual(loaded_npc.guid, self.npc_guid)
        self.assertEqual(loaded_npc.creature_id, self.npc_entry)
        self.assertEqual(loaded_npc.type, self.npc_type)
        self.assertEqual(loaded_npc.zone, self.npc_zone)
        self.assertEqual(loaded_npc.sub_zone, self.npc_subzone)
        self.assertTrue(isinstance(loaded_npc.creature, CreatureTemplateSchema))

    def test_convert_to_living_thing_friendly_npc_object(self):
        """
        Converting a CreaturesSchema with a type of 'fnpc' should convert it to a FriendlyNpc object
        """
        loaded_npc: FriendlyNPC = session.query(CreaturesSchema).get(self.npc_guid).convert_to_living_thing_object()
        self.assertTrue(isinstance(loaded_npc, FriendlyNPC))
        self.assertEqual(vars(loaded_npc), vars(self.npc))


class CreaturesVendorNpcTests(unittest.TestCase):
    def setUp(self):
        self.vendor_entry = 14
        self.vendor_guid = 8
        self.vendor_type = 'vendor'
        self.vendor_zone = 'Northshire Abbey'
        self.vendor_subzone = 'Northshire Valley'
        self.vendor_inventory = {'Wolf Meat': (Item(name='Wolf Meat', item_id=1, buy_price=1, sell_price=1), 10)}
        self.vendor = VendorNPC(name='Meatseller Jack', entry=self.vendor_entry, health=20, mana=0, level=4,
                                min_damage=5, max_damage=10, quest_relation_id=0, loot_table=None,
                                gossip="Do you want to buy meat? You've come to the right place!",
                                inventory=self.vendor_inventory)

    def test_schema_values(self):
        loaded_vendor: CreaturesSchema = session.query(CreaturesSchema).get(self.vendor_guid)
        self.assertEqual(loaded_vendor.guid, self.vendor_guid)
        self.assertEqual(loaded_vendor.creature_id, self.vendor_entry)
        self.assertEqual(loaded_vendor.type, self.vendor_type)
        self.assertEqual(loaded_vendor.zone, self.vendor_zone)
        self.assertEqual(loaded_vendor.sub_zone, self.vendor_subzone)
        self.assertTrue(isinstance(loaded_vendor.creature, CreatureTemplateSchema))

    def test_convert_to_living_thing_vendor_npc_object(self):
        loaded_vendor: VendorNPC = session.query(CreaturesSchema).get(self.vendor_guid).convert_to_living_thing_object()
        self.assertIsNotNone(loaded_vendor)
        self.assertEqual(vars(loaded_vendor), vars(self.vendor))


def tearDownModule():
    delete_test_db()

if __name__ == '__main__':
    unittest.main()
