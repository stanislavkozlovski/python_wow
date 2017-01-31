import unittest
import unittest.mock
import sys
from copy import deepcopy
from io import StringIO
from datetime import datetime, timedelta

import models.main
from zones.northshire_abbey import NorthshireAbbey, NorthshireValley, NorthshireVineyards
from constants import ZONE_MOVE_BLOCK_SPECIAL_KEY, GARRICK_PADFOOT_GUID


class NorthshireAbbeyTests(unittest.TestCase):
    def setUp(self):
        self.char_mock = unittest.mock.Mock(level=10)
        self.char_mock.has_loaded_script = lambda x: True
        self.char_mock.loaded_script = lambda x: None
        self.char_mock.has_completed_quest = lambda x: False
        self.char_mock.has_killed_monster = lambda x: False
        self.northshire_valley_monster_count = 5
        self.northshire_valley_npc_count = 2
        self.northshire_valley_quest_count = 2
        self.northshire_vineyards_monster_count = 7
        self.northshire_vineyards_npc_count = 0
        self.northshire_vineyards_quest_count = 1
        self.peculiar_hut_monster_count = 1
        self.peculiar_hut_npc_count = 0
        self.peculiar_hut_quest_count = 0

    def tearDown(self):
        """
        Due to the mutability of the static variables, we need to reset them
        on each tearDown. (Since we change them in the tests)
        """
        NorthshireAbbey.loaded_zones = {"Northshire Valley": None,
                                        "Northshire Vineyards": None,
                                        "A Peculiar Hut": None}

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
        self.assertEqual(len(zone.cs_available_quests.keys()), self.northshire_valley_quest_count)
        self.assertEqual(zone.curr_subzone, 'Northshire Valley')

    def test_move_player_valid(self):
        """
        Move the player to a valid subzone giving valid values
        """

        zone = NorthshireAbbey(self.char_mock)
        self.assertIsNone(zone.loaded_zones['Northshire Vineyards'])
        start_subzone, go_to_subzone = 'Northshire Valley', 'Northshire Vineyards'
        result = zone.move_player(current_subzone=start_subzone, destination=go_to_subzone, character=self.char_mock)

        self.assertTrue(result)
        # Should have loaded the zone for the first time
        self.assertIsNotNone(zone.loaded_zones['Northshire Vineyards'])
        self.assertTrue(isinstance(zone.loaded_zones['Northshire Vineyards'], NorthshireVineyards))
        # should have loaded the npcs from the new subzone
        self.assertEqual(len(zone.cs_alive_monsters.keys()), self.northshire_vineyards_monster_count)
        self.assertEqual(len(zone.cs_alive_npcs.keys()), self.northshire_vineyards_npc_count)
        self.assertEqual(len(zone.cs_available_quests.keys()), self.northshire_vineyards_quest_count)

        self.assertEqual(zone.curr_subzone, 'Northshire Vineyards')

    def test_move_to_peculiar_hut_padfoot_alive(self):
        """
        Since Garry Padfoot is alive, we should not be allowed to move
        """
        std_output = StringIO()
        try:
            sys.stdout = std_output
            zone = NorthshireAbbey(self.char_mock)
            self.assertIsNone(zone.loaded_zones['Northshire Vineyards'])
            start_subzone, mid_zone, go_to_subzone = 'Northshire Valley', 'Northshire Vineyards', 'A Peculiar Hut'
            result = zone.move_player(current_subzone=start_subzone, destination=mid_zone,
                                      character=self.char_mock)
            self.assertTrue(result)
            result = zone.move_player(current_subzone=mid_zone, destination=go_to_subzone,
                                      character=self.char_mock)

            self.assertEqual(zone.curr_subzone, mid_zone)
            self.assertEqual(result, ZONE_MOVE_BLOCK_SPECIAL_KEY)
            self.assertTrue("Garrick Padfoot is blocking the way." in std_output.getvalue())
        finally:
            sys.stdout = sys.__stdout__

    def test_move_to_peculiar_hut_padfoot_dead(self):
        zone = NorthshireAbbey(self.char_mock)
        self.assertIsNone(zone.loaded_zones['Northshire Vineyards'])
        start_subzone, mid_zone, go_to_subzone = 'Northshire Valley', 'Northshire Vineyards', 'A Peculiar Hut'
        result = zone.move_player(current_subzone=start_subzone, destination=mid_zone,
                                  character=self.char_mock)
        self.assertTrue(result)
        del zone.cs_alive_monsters[GARRICK_PADFOOT_GUID]
        zone.cs_monsters_guid_name_set.remove((GARRICK_PADFOOT_GUID, 'Garrick Padfoot'))
        result = zone.move_player(current_subzone=mid_zone, destination=go_to_subzone,
                                  character=self.char_mock)

        # Move should have been successful!
        self.assertTrue(result)
        self.assertEqual(len(zone.cs_alive_monsters.keys()), self.peculiar_hut_monster_count)
        self.assertEqual(len(zone.cs_alive_npcs.keys()), self.peculiar_hut_npc_count)
        self.assertEqual(len(zone.cs_available_quests.keys()), self.peculiar_hut_quest_count)

    def test_kill_monsters_complete_quests_move_player_move_back(self):
        """
        Kill the monsters and complete the quests in a subzone, move to another subzone and come back
        Assert that the monsters/quests have not been loaded again and have save their previous state
        """
        zone = NorthshireAbbey(self.char_mock)
        start_subzone, go_to_subzone = 'Northshire Valley', 'Northshire Vineyards'
        # assert that the values are as expected
        self.assertEqual(zone.curr_subzone, 'Northshire Valley')
        self.assertEqual(len(zone.cs_alive_monsters.keys()), self.northshire_valley_monster_count)
        self.assertEqual(len(zone.cs_available_quests.keys()), self.northshire_valley_quest_count)
        # simulate killing all the monsters and completing the quests
        zone.cs_alive_monsters = {}
        zone.cs_monsters_guid_name_set = set()
        zone.cs_available_quests = {}

        zone.move_player(current_subzone=start_subzone, destination=go_to_subzone, character=self.char_mock)
        zone.move_player(current_subzone=go_to_subzone, destination=start_subzone, character=self.char_mock)
        self.assertEqual(len(zone.cs_alive_monsters.keys()), 0)
        self.assertEqual(len(zone.cs_available_quests.keys()), 0)

    def test_invalid_move(self):
        """
        Moving from Northshire Valley to A Peculiar Hut is not possible.
        You first need to move to Northshire Vineyards and then you can access A Peculiar Hut
        """
        zone = NorthshireAbbey(self.char_mock)
        start_subzone, go_to_subzone = 'Northshire Valley', 'A Peculiar Hut'
        result = zone.move_player(current_subzone=start_subzone, destination=go_to_subzone, character=self.char_mock)

        # Assert that we have not moved
        self.assertFalse(result)
        self.assertEqual(zone.curr_subzone, start_subzone)
        self.assertEqual(len(zone.cs_alive_monsters.keys()), self.northshire_valley_monster_count)
        self.assertEqual(len(zone.cs_alive_npcs.keys()), self.northshire_valley_npc_count)
        self.assertEqual(len(zone.cs_available_quests.keys()), self.northshire_valley_quest_count)

    def test_load_zone(self):
        """
        the _load_zone function creates a Zone object and adds it to our loaded_zones dictionary
        """
        zone = NorthshireAbbey(self.char_mock)
        zones_to_load = ['Northshire Vineyards', 'A Peculiar Hut']
        for z_to_load in zones_to_load:
            self.assertIsNone(zone.loaded_zones[z_to_load])
            zone._load_zone(z_to_load, self.char_mock)
            self.assertIsNotNone(zone.loaded_zones[z_to_load])

    def test_load_zone_invalid_zone(self):
        """
        Loading an invalid zone should not go into any of the if blocks and not do anything.
        """
        zone = NorthshireAbbey(self.char_mock)
        original_loaded_zones = deepcopy(zone.loaded_zones)

        zone._load_zone('Aa', self.char_mock)

        for l_zone, obj in original_loaded_zones.items():
            self.assertTrue(isinstance(zone.loaded_zones[l_zone], type(obj)))

    def test_engage_zone_entered_script(self):
        """
        Given the character's subzone and the fact that he has not loaded the script before,
        the Peculiar Hut script should be engaged
        """
        # Some pre-script mocks
        import combat
        combat.engage_combat = lambda *args: True
        self.char_mock.current_subzone = 'A Peculiar Hut'
        self.char_mock.has_loaded_script = lambda x: False

        # move to the desired zone
        zone = NorthshireAbbey(self.char_mock)
        start_subzone, mid_zone, go_to_subzone = 'Northshire Valley', 'Northshire Vineyards', 'A Peculiar Hut'
        zone.move_player(current_subzone=start_subzone, destination=mid_zone,
                                  character=self.char_mock)
        del zone.cs_alive_monsters[GARRICK_PADFOOT_GUID]
        zone.cs_monsters_guid_name_set.remove((GARRICK_PADFOOT_GUID, 'Garrick Padfoot'))
        zone.move_player(current_subzone=mid_zone, destination=go_to_subzone,
                                  character=self.char_mock)

        # start the test
        start = datetime.now()
        zone.engage_zone_entered_script(self.char_mock)
        end = datetime.now()

        # 5 seconds should have passed at least while the script played out
        duration: timedelta = end - start
        self.assertGreater(duration.seconds, 5)


if __name__ == '__main__':
    unittest.main()
