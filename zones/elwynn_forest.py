"""
A Module that will take care of loading creatures that are in the Elwynn Forest zone
This is created so that we don't have to load the creatures every time we change zones AND
to have dead creatures stay dead, not be reloaded
"""
from loader import load_creatures
DB_PATH = "../python_wowDB.db"

class ElwynnForest:
    NORTHSHIRE_ABBEY_GUID_NAME_SET, NORTHSHIRE_ABBEY_ALIVE_MONSTERS, NORTHSHIRE_ABBEY_LOADED = {}, {}, False

    def get_live_monsters_and_guid_name_set(self, subzone: str):

        if subzone == 'Northshire Abbey':
            if not self.NORTHSHIRE_ABBEY_LOADED:
                self.NORTHSHIRE_ABBEY_ALIVE_MONSTERS, self.NORTHSHIRE_ABBEY_GUID_NAME_SET = load_creatures("Elwynn Forest", subzone)
                self.NORTHSHIRE_ABBEY_LOADED = True

            return self.NORTHSHIRE_ABBEY_ALIVE_MONSTERS, self.NORTHSHIRE_ABBEY_GUID_NAME_SET

        return None, None