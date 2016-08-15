"""
A Module that will take care of loading creatures that are in the Elwynn Forest zone
This is created so that we don't have to load the creatures every time we change zones AND
to have dead creatures stay dead, not be reloaded
"""
from loader import load_creatures, load_quests


class ElwynnForest:
    # the map that shows us where we can go from our current subzone
    zone_map = {"Northshire Valley": ["Northshire Vineyards"],
                "Northshire Vineyards": ["Northshire Valley"]}
    zone_name = "Elwynn Forest"

    northshire_valley_guid_name_set, northshire_valley_alive_monsters, \
    northshire_valley_quest_list, northshire_valley_loaded = {}, {}, [], False

    northshire_vineyards_guid_name_set, northshire_vineyards_alive_monsters, \
    northshire_vineyards_quest_list, northshire_vineyards_loaded = {}, {}, [], False

    def get_live_monsters_guid_name_set_and_quest_list(self, subzone: str) -> tuple:
        """
        A method used to load the specific monsters and quests tied to the subzone the character is in.
        First we figure out which subzone we're in, then we see if it has been loaded.
        If it has been loaded - return the already loaded dic, set, dict
        If it has not been loaded - load them from the load functions in loader.py and return them

        :param subzone: the subzone from which we should get the monsters and quests
        :return: A tuple containing the following (1, 2, 3)
         1 - A Dictionary holding information about the monster - Key: GUID, Value: Monster object from class Monster
         2 - A Set holding tuples of (Monster GUID, Monster Name)
         3 - A Dictionary holding information about quests - Key: Quest Name, Value: Quest object from class Quest
         4 - A Boolean indicating if we have moved or not
        """

        if subzone == 'Northshire Valley':
            if not self.northshire_valley_loaded:
                self.northshire_valley_alive_monsters, self.northshire_valley_guid_name_set = load_creatures(
                    self.zone_name, subzone)
                self.northshire_valley_quest_list = load_quests(self.zone_name, subzone)
                self.northshire_valley_loaded = True

            return self.northshire_valley_alive_monsters, \
                   self.northshire_valley_guid_name_set, \
                   self.northshire_valley_quest_list, \
                   True

        elif subzone == 'Northshire Vineyards':
            if not self.northshire_vineyards_loaded:
                self.northshire_vineyards_alive_monsters, self.northshire_vineyards_guid_name_set = load_creatures(
                    self.zone_name, subzone)
                self.northshire_vineyards_quest_list = load_quests(self.zone_name, subzone)
                self.northshire_vineyards_loaded = True

            return self.northshire_vineyards_alive_monsters, \
                   self.northshire_vineyards_guid_name_set, \
                   self.northshire_vineyards_quest_list, \
                   True

        return None, None, None, False

    def get_map_directions(self, subzone: str):  # return the zone map holding the connections of sub_zones
        return self.zone_map[subzone]
