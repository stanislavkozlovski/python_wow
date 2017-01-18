import unittest

import database.main
from tests.create_test_db import engine, session, Base

database.main.engine = engine
database.main.session = session
database.main.Base = Base

import models.main
from models.creatures.creature_template import CreatureTemplateSchema
from models.creatures.creatures import CreaturesSchema
from models.items.loot_table import LootTableSchema
from entities import Monster


class CreaturesTests(unittest.TestCase):
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


def tearDownModule():
    import tests.delete_test_db  # module that deletes the DB :)

if __name__ == '__main__':
    unittest.main()
