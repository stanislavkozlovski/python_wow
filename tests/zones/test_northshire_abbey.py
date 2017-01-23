import unittest
import unittest.mock

import models.main
from zones.northshire_abbey import NorthshireAbbey, NorthshireValley, NorthshireVineyards


class NorthshireAbbeyTests(unittest.TestCase):
    def setUp(self):
        self.char_mock = unittest.mock.Mock()
        self.char_mock.has_loaded_script = lambda x: True
        self.char_mock.loaded_script = lambda x: None
        self.char_mock.has_killed_monster = lambda x: False
        self.northshire_valley_monster_count = 5
        self.northshire_valley_npc_count = 2

    def test_zone(self):
        zone = NorthshireAbbey(self.char_mock)
        # it should have loaded subzones
        self.assertTrue(zone.loaded_zones['Northshire Valley'], NorthshireValley)
        # these should not have been loaded because we have not gone in there
        self.assertIsNone(zone.loaded_zones['Northshire Vineyards'])
        self.assertIsNone(zone.loaded_zones['A Peculiar Hut'])
        # it should hold the monsters in the current subzone
        self.assertEqual(len(zone.cs_alive_monsters.keys()), self.northshire_valley_monster_count)
        self.assertEqual(len(zone.cs_alive_npcs.keys()), self.northshire_valley_npc_count)
        self.assertEqual(zone.curr_subzone, 'Northshire Valley')

if __name__ == '__main__':
    unittest.main()
