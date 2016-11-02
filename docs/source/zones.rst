Disclaimer
==========
The following code is heavily commented for presentation purposes. While the real code does have a fair
bit of comments, they're not as over-abundant and obvious as here.


Zones
==========

Long story short
-----
In general, all the Zones are split into SubZones. The actual storage of monsters/npcs is on a subzone basis.
The Zone class is sort of a wrapper object that holds all our subzones together and holds the current subzone's information in it.
This approach gives us easy access to monsters/etc. of the current subzone we are in and gives us an easy way to store
information about changes in that subzone when we are not in it.

Long story
-----
If you didn't notice, or maybe I didn't show you, we have a pre-defined constant dictionary of ZONES in our main.py::

    "line 11 in main.py"
    ZONES = {"Northshire Abbey": None}
    "Northshire Abbey is considered the starter zone for every character in the game"
which we populate with an instance of our starter zone's class Northshire Abbey::

    "line 17 in main.py"
    ZONES["Northshire Abbey"] = NorthshireAbbey(main_character)
Okay well what the hell is all of this? To understand let's delve into the zones folder in the module holding the base classes for zones - ``zone.py``::

    class Zone:
        # the _map that shows us where we can go from our current subzone
        zone_map = {}  # type: dict - key: current_subzone: str, value: A list of subzones: str which we can go to
        zone_name = "" # name of the zone
        starter_subzone = ""  # the subzone you start in
        loaded_zones = {}  # dictionary that will hold the subzone class objects

        #  the cs in cs_alive_monsters and similar names stands for Current Subzone
The alive monsters/npcs in the subzone. More on these `_alive_monsters and _monster_guid_name_set:`_::

        cs_alive_monsters, cs_monsters_guid_name_set = {}, set() 
        cs_alive_npcs, cs_npcs_guid_name_set = {}, set()  # the alive npcs in the subzone
::

        cs_available_quests = {}  # the subzone's quests that are available to the character. (A quest which the character finished is removed from here)
        # the current subzone's map, a list of string representing to which subzone we can go from the current one
        # this is literally taken from the zone_map dictionary using the curr_subzone as key
        cs_map = []  
        curr_subzone = ""  # the current subzone the character is in

I feel like this isn't doing you much of a favor explaining how it works, so I'll jump onto an example of it's implementation in northshire_abbey.py::

    class NorthshireAbbey(Zone):
        # the _map that shows us where we can go from our current subzone
        # ex: from the subzone Northshire Vineyards we can go to either Northshire Valley or A Peculiar Hut
        zone_map = {"Northshire Valley": ["Northshire Vineyards"],
                    "Northshire Vineyards": ["Northshire Valley", "A Peculiar Hut"],
                    "A Peculiar Hut": ["Northshire Vineyards"]}
        zone_name = "Northshire Abbey"
        starter_subzone = "Northshire Valley"
        # dictionary that will hold the subzone class objects
        # here we will subzone class objects so that we're able to store
        # information like alive monsters, available quests and etc easily upon navigation from zone to zone
        loaded_zones = {"Northshire Valley": None,
                        "Northshire Vineyards": None,
                        "A Peculiar Hut": None}

        def __init__(self, character):
            super().__init__()  # the Zone parent class does not have an __init__ method
            # here we create an object of class SubZone, more on that in a bit
            subzone_object = NorthshireValley(name="Northshire Valley", parent_zone_name=self.zone_name,
                                              zone_map=self.zone_map["Northshire Valley"],
                                              character=character)
            self.cs_alive_monsters, self.cs_monsters_guid_name_set = subzone_object.get_monsters()
            self.cs_alive_npcs, self.cs_npcs_guid_name_set = subzone_object.get_npcs()
            self.cs_available_quests = subzone_object.get_quests()
            self.cs_map = subzone_object.get_map_directions()
            self.curr_subzone = "Northshire Valley"
            self.loaded_zones["Northshire Valley"] = subzone_object  # we attach the subzone object to our loaded_zones dictionary

So, ignoring the SubZone class and method for a while, we continue onto the methods of the NorthshireAbbey class::

   def move_player(self, current_subzone: str, destination: str, character):
        """
        :param current_subzone: the subzone the character is in
        :param destination: the subzone he wants to go in
        :return: a boolean indicating if the move is possible
        """
        if current_subzone in self.zone_map.keys() and current_subzone == self.curr_subzone:

            if destination in self.zone_map[current_subzone] and destination in self.loaded_zones.keys():
                # Before moving:
                # update the information for our current in case we've killed monsters or done quests for example
                self._update_subzone_attributes(current_subzone)
Here we updated the subzone's attributes before leaving the zone
Next is a hardcoded script to block the player from entering A Peculiar Hut if the Monster Garrick Padfoot is alive::

                if destination == "A Peculiar Hut":
                    # this means we are in Northshire Vineyards
                    if self.GUID_GARRY_PADFOOT in self.cs_alive_monsters.keys():  # if garry padfoot is alive
                        print("Garrick Padfoot is blocking the way.")
                        return 0

                if not self.loaded_zones[destination]:  # if we don't have the destination's attributes loaded load them
                    self._load_zone(destination, character)

                self.curr_subzone = destination

                # We move, therefore update our attributes
                self._update_attributes(destination)
This is different from the update_subzone_attributes method we called above, as this one changes the attributes in the **ZONE** class.
Basically loading up the creatures from the subzone we're entering onto our Zone object.


To enter a zone, we need to create the class object first. This is where _load_zone comes to help::

    def _load_zone(self, subzone: str, character):
        # if we have not loaded the zone before, we need to initialize it's class and put it in the loaded_zones
        if subzone == {ZONENAME}:
            self.loaded_zones[{ZONENAME}] = {ZONENAME}(name=subzone,
		                                          parent_zone_name=self.zone_name,
		                                          zone_map=self.zone_map[subzone],
		                                          character=character)
This if check is repeated for each subzone in our main Zone.

So... this obviously loads the SubZone class. But *what the heck* is it? Time to find out!::

	class SubZone:
	    def __init__(self, name: str, parent_zone_name: str, zone_map: list, character):
		self.name = name
		self.parent_zone_name = parent_zone_name
		self._map = zone_map  # the _map that shows us where we can go from here

		self._alive_monsters, self._monster_guid_name_set = load_monsters(self.parent_zone_name, self.name, character)

_alive_monsters and _monster_guid_name_set:
++++++++++++++++++++++++++++++++++++++++++++
``_alive_monsters`` is a dictionary, the Key of which holds the unique GUID (Database ID) for a given Monster(in the creatures DB table).
As a value, the ``_alive_monsters`` dict holds an object of class ``Monster`` associated with that specific monster.

The ``_monster_guid_name_set`` is a set of TUPLES, which hold the GUID of a monster and it's name. This is essentially what connects
a monster's name to it's ``Monster`` object in the ``_alive_monsters dictionary``.

Examples::

    " in-game print of _alive_monsters "
    {1: <entities.Monster object at 0x01A853F0>, 2: <entities.Monster object at 0x01A85B30>}
    " in-game print of _monster_guid_name_set "
    {(5, 'Wolf'), (2, 'Wolf'), (1, 'Wolf'), (4, 'Wolf'), (3, 'Wolf')}
::

		self._alive_npcs, self._npc_guid_name_set = load_npcs(self.parent_zone_name, self.name)
The variables here are analogous to the monsters'

::

		self._quest_list = load_quests(self.parent_zone_name, self.name, character)
``_quest_list`` is a dictionary, thet Key of which holds the name of the quest and it's value is a object of class ``Quest`` More on Quests here

SubZone summary
+++++++++++++++
The ``SubZone`` class essentially is a container with a name that gets loaded with 
specific monsters/npcs/quests associated with it and holds the information for them.
It has get and set(actually called update) methods in it for getting/updating the monsters/npcs/quests but they are not worth showing here.


 
Let's continue on examining our game!
