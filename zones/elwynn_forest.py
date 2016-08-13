"""
A Module that will take care of loading creatures that are in the Elwynn Forest zone
This is created so that we don't have to load the creatures every time we change zones AND
to have dead creatures stay dead, not be reloaded
"""
from loader import load_creatures
from loader import load_quests
DB_PATH = "../python_wowDB.db"

class ElwynnForest:
    zone_map = {"Northshire Valley": ["Northshire Vineyards"],  # the map that shows us where we can go from our current subzone
           "Northshire Vineyards": ["Northshire Valley"]}
    NORTHSHIRE_VALLEY_GUID_NAME_SET, NORTHSHIRE_VALLEY_ALIVE_MONSTERS, NORTHSHIRE_VALLEY_QUEST_LIST, NORTHSHIRE_VALLEY_LOADED = {}, {}, [], False
    NORTHSHIRE_VINEYARDS_GUID_NAME_SET, NORTHSHIRE_VINEYARDS_ALIVE_MONSTERS, NORTHSHIRE_VINEYARDS_QUEST_LIST, NORTHSHIRE_VINEYARDS_LOADED = {}, {}, [], False

    def get_live_monsters_guid_name_set_and_quest_list(self, subzone: str) -> tuple:

        if subzone == 'Northshire Valley':
            if not self.NORTHSHIRE_VALLEY_LOADED:
                self.NORTHSHIRE_VALLEY_ALIVE_MONSTERS, self.NORTHSHIRE_VALLEY_GUID_NAME_SET = load_creatures("Elwynn Forest", subzone)
                self.NORTHSHIRE_VALLEY_QUEST_LIST = load_quests("Elwynn Forest", subzone)
                self.NORTHSHIRE_VALLEY_LOADED = True

            return self.NORTHSHIRE_VALLEY_ALIVE_MONSTERS, self.NORTHSHIRE_VALLEY_GUID_NAME_SET, self.NORTHSHIRE_VALLEY_QUEST_LIST

        elif subzone == 'Northshire Vineyards':
            if not self.NORTHSHIRE_VINEYARDS_LOADED:
                self.NORTHSHIRE_VINEYARDS_ALIVE_MONSTERS, self.NORTHSHIRE_VINEYARDS_GUID_NAME_SET = load_creatures("Elwynn Forest", subzone)
                self.NORTHSHIRE_VINEYARDS_QUEST_LIST = load_quests("Elwynn Forest", subzone)
                self.NORTHSHIRE_VINEYARDS_LOADED = True

            return self.NORTHSHIRE_VINEYARDS_ALIVE_MONSTERS, self.NORTHSHIRE_VINEYARDS_GUID_NAME_SET, self.NORTHSHIRE_VINEYARDS_QUEST_LIST

        return None, None, None


    def get_map_directions(self, subzone: str):
        return self.zone_map[subzone]