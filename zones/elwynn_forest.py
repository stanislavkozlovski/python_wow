"""
A Module that will take care of loading creatures that are in the Elwynn Forest zone
This is created so that we don't have to load the creatures every time we change zones AND
to have dead creatures stay dead, not be reloaded

the cs in cs_alive_monsters and similar names stands for Current Subzone
"""
from zones.zone import Zone, SubZone


class ElwynnForest(Zone):
    # the _map that shows us where we can go from our current subzone
    zone_map = {"Northshire Valley": ["Northshire Vineyards"],
                "Northshire Vineyards": ["Northshire Valley"]}
    zone_name = "Elwynn Forest"
    starter_subzone = "Northshire Valley"
    # dictionary that will hold the subzone class objects
    loaded_zones = {"Northshire Valley": None,
                    "Northshire Vineyards": None}

    cs_alive_monsters, cs_monsters_guid_name_set = {}, set()
    cs_alive_npcs, cs_npcs_guid_name_set = {}, set()
    cs_available_quests = {}
    cs_map = []
    curr_subzone = ""

    def __init__(self):
        super().__init__()
        subzone_object = NorthshireValley(name="Northshire Valley", parent_zone_name=self.zone_name,
                                          zone_map=self.zone_map["Northshire Valley"])
        self.cs_alive_monsters, self.cs_monsters_guid_name_set = subzone_object.get_monsters()
        self.cs_alive_npcs, self.cs_npcs_guid_name_set = subzone_object.get_npcs()
        self.cs_available_quests = subzone_object.get_quests()
        self.cs_map = subzone_object.get_map_directions()
        self.curr_subzone = "Northshire Valley"
        self.loaded_zones["Northshire Valley"] = subzone_object

    def move_player(self, current_subzone: str, destination: str):
        """

        :param current_subzone: the subzone the character is in
        :param destination: the subzone he wants to go in
        :return: a boolean indicating if the move is possible
        """
        if current_subzone in self.zone_map.keys() and current_subzone == self.curr_subzone:
            if destination in self.zone_map[current_subzone] and destination in self.loaded_zones.keys():
                # save the information in case we've killed monsters or done quests for example
                temp_sz_object = self.loaded_zones[current_subzone]  # type: SubZone
                temp_sz_object.update_monsters(self.cs_alive_monsters, self.cs_monsters_guid_name_set)
                temp_sz_object.update_npcs(self.cs_alive_npcs, self.cs_npcs_guid_name_set)
                temp_sz_object.update_quests(self.cs_available_quests)
                self.loaded_zones[current_subzone] = temp_sz_object

                if not self.loaded_zones[destination]:
                    # if we have not loaded the zone before, we need to initialize it's class and put it in the loaded_zones
                    if destination == "Northshire Valley":
                        self.loaded_zones[destination] = NorthshireValley(name=destination,
                                                                          parent_zone_name=self.zone_name,
                                                                          zone_map=self.zone_map[destination])
                    elif destination == "Northshire Vineyards":
                        self.loaded_zones[destination] = NorthshireVineyards(name=destination,
                                                                          parent_zone_name=self.zone_name,
                                                                          zone_map=self.zone_map[destination])
                self.curr_subzone = destination
                subzone_object = self.loaded_zones[destination]  # type: SubZone
                # We move, therefore load the new attributes
                self.cs_alive_monsters, self.cs_monsters_guid_name_set = subzone_object.get_monsters()
                self.cs_alive_npcs, self.cs_npcs_guid_name_set = subzone_object.get_npcs()
                self.cs_available_quests = subzone_object.get_quests()
                self.cs_map = subzone_object.get_map_directions()
                return True
            else:
                print("No such destination {}.".format(destination))
        else:
            raise Exception("The subzone is not in the zone_object!")

        return False

    def get_monsters(self):
        return self.cs_alive_monsters, self.cs_monsters_guid_name_set

    def get_npcs(self):
        return self.cs_alive_npcs, self.cs_npcs_guid_name_set

    def get_quests(self):
        return self.cs_available_quests

    def get_map(self):
        return self.cs_map

class NorthshireValley(SubZone):
    pass

class NorthshireVineyards(SubZone):
    pass