"""
This is the base class for zones. Every zone in the game will inherit from this class.
"""
from loader import load_monsters, load_npcs, load_quests


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

    def move_player(self, current_subzone: str, destination: str):
        """

        :param current_subzone: the subzone the character is in
        :param destination: the subzone he wants to go in
        :return: a boolean indicating if the move is possible
        """
        pass

    def get_monsters(self):
        pass

    def get_npcs(self):
        pass

    def get_quests(self):
        pass

    def get_map(self):
        pass



class SubZone:
    def __init__(self, name: str, parent_zone_name: str, zone_map: list):
        self.name = name
        self.parent_zone_name = parent_zone_name
        self._map = zone_map  # the _map that shows us where we can go from here

        self.alive_monsters, self.monster_guid_name_set = load_monsters(self.parent_zone_name, self.name)
        self.alive_npcs, self.npc_guid_name_set = load_npcs(self.parent_zone_name, self.name)
        self.quest_list = load_quests(self.parent_zone_name, self.name)

    def get_monsters(self):
        """
        :return Tuple (1,2)
        1 - A Dictionary holding information about the monster - Key: GUID, Value: Monster object from class Monster
        2 - A Set holding tuples of (Monster GUID, Monster Name)"""
        return self.alive_monsters, self.monster_guid_name_set

    def get_npcs(self):
        """
        :return: A Tuple (1,2)
        1 - A Dictionary holding information a bout the friendly npcs - Key: GUID, Value: object from class FriendlyNPC
        2 - A Set holding tuples of (NPC GUID, NPC Name)
        """
        return self.alive_npcs, self.npc_guid_name_set

    def get_quests(self):
        """
        :return: A Dictionary holding information about quests - Key: Quest Name, Value: Quest object from class Quest
        """
        return self.quest_list

    def update_monsters(self, alive_monsters: dict, guid_name_set: set):
        self.alive_monsters = alive_monsters
        self.monster_guid_name_set = guid_name_set

    def update_npcs(self, alive_npcs: dict, guid_name_set: set):
        self.alive_npcs = alive_npcs
        self.npc_guid_name_set = guid_name_set

    def update_quests(self, quests: dict):
        self.quest_list = quests

    def get_map_directions(self):  # return the zone _map holding the connections of sub_zones
        return self._map
