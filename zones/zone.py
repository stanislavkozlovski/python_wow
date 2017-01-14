"""
This is the base class for zones. Every zone in the game will inherit from this class.
"""
from database.main import cursor
from loader import load_npcs
from models.quests.loader import load_quests
from models.creatures.loader import load_monsters


class Zone:
    # the _map that shows us where we can go from our current subzone
    zone_map = {}  # type: dict - key: current_subzone: str, value: A list of subzones: str which we can go to
    zone_name = "" # name of the zone
    starter_subzone = ""  # the subzone you start in
    loaded_zones = {}  # dictionary that will hold the subzone class objects

    #  the cs in cs_alive_monsters and similar names stands for Current Subzone
    cs_alive_monsters, cs_monsters_guid_name_set = {}, set()
    cs_alive_npcs, cs_npcs_guid_name_set = {}, set()
    cs_available_quests = {}
    cs_map = []
    curr_subzone = ""

    def move_player(self, current_subzone: str, destination: str, character):
        """

        :param current_subzone: the subzone the character is in
        :param destination: the subzone he wants to go in
        :return: a boolean indicating if the move is possible
        """
        pass

    def _update_subzone_attributes(self, subzone: str):
        """
        Updates the specified SubZone class object in loaded_zones.
        This is done to update information like Completed Quests, Killed Monsters
        """
        # create a temp object
        temp_sz_object = self.loaded_zones[subzone]  # type: SubZone
        # update it
        temp_sz_object.update_monsters(self.cs_alive_monsters, self.cs_monsters_guid_name_set)
        temp_sz_object.update_npcs(self.cs_alive_npcs, self.cs_npcs_guid_name_set)
        temp_sz_object.update_quests(self.cs_available_quests)
        # put it back in the loaded_zones dict
        self.loaded_zones[subzone] = temp_sz_object

    def _load_zone(self, subzone: str, dead_monsters: set):
        pass

    def _update_attributes(self, subzone: str):
        subzone_object = self.loaded_zones[subzone]  # type: SubZone

        self.cs_alive_monsters, self.cs_monsters_guid_name_set = subzone_object.get_monsters()
        self.cs_alive_npcs, self.cs_npcs_guid_name_set = subzone_object.get_npcs()
        self.cs_available_quests = subzone_object.get_quests()
        self.cs_map = subzone_object.get_map_directions()

    def get_cs_monsters(self):
        """
        :return: A tuple (1,2)
         1 - A Dictionary holding information about the monster - Key: GUID, Value: Monster object from class Monster
 +       2 - A Set holding tuples of (Monster GUID, Monster Name)
        """
        return self.cs_alive_monsters, self.cs_monsters_guid_name_set

    def get_cs_npcs(self):
        """
        :return: A Tuple (1,2)
        1 - A Dictionary holding information a bout the friendly npcs - Key: GUID, Value: object from class FriendlyNPC
+       2 - A Set holding tuples of (NPC GUID, NPC Name)
        """
        return self.cs_alive_npcs, self.cs_npcs_guid_name_set

    def get_cs_quests(self):
        """
        :return: A Dictionary holding information about quests - Key: Quest Name, Value: Quest object from class Quest
        """
        return self.cs_available_quests

    def get_cs_map(self):
        """
        :return: A list of strings with the name of the subzones we have access to from our current one
        """
        return self.cs_map

    def engage_zone_entered_script(self, character):
        """
        if there is a script to do when you've entered the zone, here is where you put it
        :param subzone:
        :return:
        """
        pass


class SubZone:

    def __init__(self, name: str, parent_zone_name: str, zone_map: list, character):
        self.name = name
        self.parent_zone_name = parent_zone_name
        self._map = zone_map  # the _map that shows us where we can go from here

        self._alive_monsters, self._monster_guid_name_set = load_monsters(self.parent_zone_name, self.name, character)
        self._alive_npcs, self._npc_guid_name_set = load_npcs(self.parent_zone_name, self.name, cursor)
        self._quest_list = load_quests(self.parent_zone_name, self.name, character)

    def load_on_zone_entry_script(self, character):
        """
        This loads and executes the script we have for the zone
        each zone is left to implement it's own unique script here or import
        it from some module
        """
        pass

    def get_monsters(self):
        """
        :return Tuple (1,2)
        1 - A Dictionary holding information about the monster - Key: GUID, Value: Monster object from class Monster
        2 - A Set holding tuples of (Monster GUID, Monster Name)"""
        return self._alive_monsters, self._monster_guid_name_set

    def get_npcs(self):
        """
        :return: A Tuple (1,2)
        1 - A Dictionary holding information a bout the friendly npcs - Key: GUID, Value: object from class FriendlyNPC
        2 - A Set holding tuples of (NPC GUID, NPC Name)
        """
        return self._alive_npcs, self._npc_guid_name_set

    def get_quests(self):
        """
        :return: A Dictionary holding information about quests - Key: Quest Name, Value: Quest object from class Quest
        """
        return self._quest_list

    def get_map_directions(self):  # return the zone _map holding the connections of sub_zones
        return self._map

    def update_monsters(self, alive_monsters: dict, guid_name_set: set):
        self._alive_monsters = alive_monsters
        self._monster_guid_name_set = guid_name_set

    def update_npcs(self, alive_npcs: dict, guid_name_set: set):
        self._alive_npcs = alive_npcs
        self._npc_guid_name_set = guid_name_set

    def update_quests(self, quests: dict):
        self._quest_list = quests

