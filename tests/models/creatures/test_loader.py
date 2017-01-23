import unittest

import database.main
from tests.create_test_db import engine, session, Base

database.main.engine = engine
database.main.session = session
database.main.Base = Base

import models.main
from models.creatures.creature_template import CreatureTemplateSchema
from models.creatures.creatures import CreaturesSchema
from models.creatures.loader import load_monsters, load_npcs
from entities import Monster, FriendlyNPC, VendorNPC
from items import Item


class CharacterMock():
    def __init__(self):
        self.killed_monsters = set()

    def add_killed_monster(self, guid):
        self.killed_monsters.add(guid)

    def has_killed_monster(self, monster_guid: int):
        return monster_guid in self.killed_monsters


class LoaderTest(unittest.TestCase):

    def setUp(self):
        self.character = CharacterMock()
        self.character.add_killed_monster(15)  # Brother Paxton in peculiar hut

    def test_load_monsters_valid(self):
        """ Load all the monsters from Northshire Abbey - Northshire Valley"""
        self.expected_monster_count = 5
        monsters_dict, guid_name_set =  load_monsters(zone='Northshire Abbey', subzone='Northshire Valley', character=self.character)
        self.assertEqual(len(monsters_dict.keys()), self.expected_monster_count)

    def test_load_monsters_invalid_zone(self):
        """ Load all the monsters from an invalid zone, should end up with 0 """
        self.expected_monster_count = 0
        monsters_dict, guid_name_set = load_monsters(zone='Bru', subzone='S',
                                                     character=self.character)
        self.assertEqual(len(monsters_dict.keys()), self.expected_monster_count)
        self.assertEqual(len(guid_name_set), len(monsters_dict.keys()))

    def test_load_monsters_character_has_killed(self):
        """
        Try to load the monsters from a zone in which the character has killed
        a monster. We should end up with 0 monsters
        """
        self.expected_monster_count = 0
        monsters_dict, guid_name_set =  load_monsters(zone='Northshire Abbey', subzone='A Peculiar Hut', character=self.character)
        self.assertEqual(len(monsters_dict.keys()), 0)
        self.assertEqual(len(guid_name_set), 0)

    def test_load_npcs_valid(self):
        """
        Load the npcs from a zone. We should get both FriendlyNPCs and VendorNPCs
        """
        expected_npc_count = 2
        expected_zone = 'Northshire Abbey'
        expected_subzone = 'Northshire Valley'
        npcs_dict, guid_name_set = load_npcs(zone=expected_zone, subzone=expected_subzone)

        for i in guid_name_set:
            self.assertIsNotNone(i)
            self.assertTrue(isinstance(i[0], int))
            self.assertTrue(isinstance(i[1], str))
        for i in npcs_dict.values():
            self.assertTrue(isinstance(i, FriendlyNPC))

        self.assertEqual(len(npcs_dict.keys()), expected_npc_count)
        self.assertEqual(len(npcs_dict.keys()), len(guid_name_set))

    def test_load_npcs_no_npcs(self):
        """
        Load the npcs from a zone which has no NPCs
        """
        expected_npc_count = 0
        expected_zone = 'Northshire Abbey'
        expected_subzone = 'A Peculiar Hut'

        npcs_dict, guid_name_set = load_npcs(zone=expected_zone, subzone=expected_subzone)
        self.assertEqual(len(npcs_dict.keys()), expected_npc_count)
        self.assertEqual(len(npcs_dict.keys()), len(guid_name_set))


if __name__ == '__main__':
    unittest.main()
