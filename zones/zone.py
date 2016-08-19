"""
This is the base class for zones. Every zone in the game will inherit from this class.
"""


class Zone:
    # the map that shows us where we can go from our current subzone
    zone_map = {}  # type: dict - key: current_subzone: str, value: A list of subzones: str which we can go to
    zone_name = "" # name of the zone

    def get_zone_attributes(self, subzone: str) -> tuple:
        """
        A method used to load the specific monsters, npcs and quests tied to the subzone the character is in.
        First we figure out which subzone we're in, then we see if it has been loaded.
        If it has been loaded - return the already loaded dic, set, dict
        If it has not been loaded - load them from the load functions in loader.py and return them

        :param subzone: the subzone from which we should get the monsters and quests
        :return: A tuple containing the following (1, 2, 3)
         1 - A Dictionary holding information about the monster - Key: GUID, Value: Monster object from class Monster
         2 - A Set holding tuples of (Monster GUID, Monster Name)
         3 - A Dictionary holding information a bout the friendly npcs - Key: GUID, Value: object from class FriendlyNPC
         4 - A Set holding tuples of (NPC GUID, NPC Name)
         5 - A Dictionary holding information about quests - Key: Quest Name, Value: Quest object from class Quest
         6 - A Boolean indicating if we have moved or not
        """

        """
        Here we check for our current subzone, load the attributes from there and return them
        example:
        if subzone == 'Northshire Valley':
            if not self.northshire_valley_loaded:
                self.northshire_valley_alive_monsters, self.northshire_valley_guid_name_set = load_monsters(
                    self.zone_name, subzone)
                self.northshire_valley_alive_npcs, self.northshire_valley_npc_guid_name_set = load_npcs(
                    self.zone_name, subzone)
                self.northshire_valley_quest_list = load_quests(self.zone_name, subzone)
                self.northshire_valley_loaded = True

            return self.northshire_valley_alive_monsters, \
                   self.northshire_valley_guid_name_set, \
                   self.northshire_valley_alive_npcs, \
                   self.northshire_valley_npc_guid_name_set, \
                   self.northshire_valley_quest_list, \
                   True
        """

        return None, None, None, None, None, False

    def get_map_directions(self, subzone: str):  # return the zone map holding the connections of sub_zones
        return set(self.zone_map[subzone])
