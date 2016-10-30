Disclaimer
==========
The following code is heavily commented for presentation purposes. While the real code does have a fair
bit of comments, they're not as over-abundant and obvious as here.

Character
===========================

This is the class for the player's character. The main character of the game.
It starts off by inheriting another class called LivingThing::

    class LivingThing:
        """
        This is the base class for all things _alive - characters, monsters and etc.
        """
         def __init__(self, name: str, health: int = 1, mana: int = 1, level: int = 1):
                self.name = name  # as a string, the name of the LivingThing 
                self.health = health  # as an integer, the CURRENT hit points. 
                #(this changes while fighting)
                self.max_health = health  # maximum static hit points. 
                #(this does not change while fighting)
                self.mana = mana  # same as health but for mana points, 
                #typically used as a resource for casting spells
                self.max_mana = mana  # same as max_health
                self.level = level  # the level of the LivingThing
                self.absorption_shield = 0  # holds as an integer the hit
                #points the LivingThing has as absorption-shield points.  
                #Basically means how much damage it can absorb until it starts losing health
                
                self.attributes = {self.KEY_ARMOR: 0}  # a dictionary holding the 
                #amount of attributes the LivingThing currently has. 
                
                self._alive = True  # private boolean holding information if the LivingThing is alive
                self._in_combat = False  # private boolean holding information
                #if the LivingThing is in combat (fighting with a monster, etc)
                self.buffs = {}  # dict Key: an instance of class Buff,
                #Value: The turns it has left to be active, int
                # buffs is a dictionary holding instances of the class Buff, more on that later.
                

Here is the character class::

    class Character(LivingThing):
        # keys are used to access the level_stats 
        # dictionary that holds information on stats to update on each level up
        KEY_LEVEL_STATS_HEALTH = 'health'
        KEY_LEVEL_STATS_MANA = 'mana'
        # these keys are used to access the attributes 
        # dictionary which holds information on the character's stats
        KEY_STRENGTH = 'strength'
        KEY_ARMOR = 'armor'
        KEY_AGILITY = 'agility'
        KEY_BONUS_HEALTH = 'bonus_health'
        KEY_BONUS_MANA = 'bonus_mana'
        spell_cooldowns = {}  # dictionary that holds 
        # Key: Spell Name(str), Value: It's cooldown in turns (int)

        def __init__(self, name: str, health: int = 1, mana: int = 1, strength: int = 1, agility: int = 1,
                     loaded_scripts: set=set(), killed_monsters: set=set(), completed_quests: set=set(),
                     saved_inventory: dict={'gold': 0}, saved_equipment: dict=CHARACTER_DEFAULT_EQUIPMENT):
            super().__init__(name, health, mana, level=1)
            self.min_damage = 0  # the minimum amount of damage
            #this Character can deal on an auto-attack
            self.max_damage = 1  # the maximum amount of damage 
            #this Character can deal on an auto-attack
            self.equipped_weapon = Weapon(name="Starter Weapon", item_id=0)  # The weapon the character has equipped
            self.experience = 0  # the amount of experience points 
            #this character currently has. Experience Points are used to gain 
            #levels
            self.xp_req_to_level = 400  # the amount of experience points 
            #needed to get to the next level. It is updated when the character levels up
            
            self.bonus_health = 0  # variable holding the amount of bonus health the 
            #character has accumulated at this very moment from Buffs and etc. 
            #Stored as a variable to be able to easily remove it from the max_health once the Buff expires
            self.bonus_mana = 0  # analogous to bonus_health
            
            # dictionary holding information on the amount of 
            #attributes the character has. More on that here
            self.attributes = {self.KEY_STRENGTH: strength, self.KEY_ARMOR: 75,
            self.KEY_AGILITY: agility, self.KEY_BONUS_HEALTH: 0,
            self.KEY_BONUS_MANA: 0}  # dictionary holding attributes, KEY: strength, Value: 5
                          
            # the zone and subzone the character is currently in
            self.current_zone = "Northshire Abbey"
            self.current_subzone = "Northshire Valley"
            
            self.loaded_scripts = loaded_scripts  # holds the scripts 
            #that the character has seen (which should load only once)
            self.killed_monsters = killed_monsters  # a set that 
            #holds the GUIDs of the creatures that
            #the character has killed (and that should not be killable a second time)
            
            self.completed_quests = completed_quests  
            # a set that holds the name of the quests that the character has completed
            
            # a dictionary of dictionaries holding information about the amount 
            #of stats a character should get according to the level he has just
            #reached. ex: {5: {health: 10, mana: 5}} - meaning when the character 
            #gets to level 5, he will receive 10 health and 5 mana points as a reward
            self._LEVEL_STATS = load_character_level_stats()
            
            # a dictionary holding information about how much XP the character
            #needs to level up when at a certain level.
            # ex {2: 800} means that at level 2, the character needs 800 XP to reach level 3
            self._REQUIRED_XP_TO_LEVEL = load_character_xp_requirements()
            
            # dictionary holding as a key: the unique ID of a quest and as a value: 
            #an instance of the class Quest. More on that here
            self.quest_log = {}
            
            # dictionary holding information about the items the character has in his inventory.
            #Like commented: the key is the name of the item he has and the value
            #is a tuple of a object of the Item class and an integer, accounting for how many
            #times he has that item. 
            #ex: Worn Axe: {<Weapon>, 2} means that the character has 2 Worn Axes in his inventory
            self.inventory = saved_inventory # dict Key: str, Value: tuple(Item class instance, Item Count)
            
            # a dictionary holding the current equipment of the character. 
            #the keys are as a string - the name of the slot for gear. ex: 
            #Shoulder and the value is an object of class Equipment, which inherits Item More on that here
            self.equipment = saved_equipment # dict Key: Equipment slot, Value: object of class Equipment
            
            # this method iterates through the equipment of a character 
            #and adds up the attribute sto the self.attributes dictionary.
            self._handle_load_saved_equipment()  # add up the attributes for our saved_equipment
            
            
As you can see, lots of stuff. Now let me present some basic functions of the Character class
It's worth noting that whenever we stop fighting a monster (leave combat), we regen back to full hp/mana::

    def leave_combat(self):
        self._in_combat = False
        self._regenerate()
    def _regenerate(self):
        self.health = self.max_health
        self.mana = self.max_mana

Dealing damage
===============================
Speaking of fighting, let's see how we deal damage::

    def get_auto_attack_damage(self, target_level: int) -> Damage:
        # get the base auto attack damage
        damage_to_deal = random.randint(int(self.min_damage), int(self.max_damage) + 1)
Takes a random integer between the minimum and maximum auto attack damage::

        # factor in the level difference
        damage_to_deal = self._calculate_level_difference_damage(damage_to_deal, target_level)
Factors in the level difference of the attacker and victim, which is, long story short:
10% bonus for every level difference in respect to both sides. Meaning that if the character is level 5 and the victim
is level 10, the character will deal 50% less damage. Vice-versa if the character is level 10 and the victim - level 5, the
character will deal 50% more damage.::

        return Damage(phys_dmg=damage_to_deal)
Returns an object of class Damage with it's phys_dmg variable set to the amount of auto attack damage.


Taking Damage
===============================
You can't deal damage without taking any::

   	def take_attack(self, monster_name:str, damage: Damage, attacker_level: int):
		damage = self._apply_armor_reduction(damage, attacker_level)
        damage = self._apply_damage_absorption(damage)
        print("{0} attacks {1} for {2}!".format(monster_name, self.name, damage))
        self._subtract_health(damage)

#. We reduce the damage according to the armor the character has::

 	def _apply_armor_reduction(self, damage: Damage, attacker_level: int) -> Damage:
        """
        This method applies the armor reduction to a blow, the formula is as follows:
        Percentage to Reduce = Armor / (Armor + 400 + 85 * Attacker_Level)
        :param damage: the raw damage
        :return: the damage with the applied reduction
        """
        armor = self.attributes[self.KEY_ARMOR]
        reduction_percentage = armor / (armor + 400 + 85 * attacker_level)  # we get the percentage of damage to reduce
Important note: We take only the .phys_dmg property of the Damage class and leave the magical damage untouched::

        damage_to_deduct = damage.phys_dmg * reduction_percentage  # get the damage we need to deduct	
        reduced_damage = damage.phys_dmg - damage_to_deduct  # deduct the damage

        return Damage(phys_dmg=reduced_damage, magic_dmg=damage.magic_dmg)



#. Then, we direct as much damage as we can to the Character's absorption shield::

    def _apply_damage_absorption(self, damage: Damage, to_print=False) -> Damage:
        """
        This method subtracts the absorption (if any) from the damage
        :param to_print: A boolean indicating if we want to actually subtract the damage from the shield. If it's true,
        we're getting the damage for the sole reason to print it only, therefore we should not modify anything
        :return Tuple(Damage, absorbed(float)
        """

        if self.absorption_shield:  # if there is anything to absorb
            # lowers the damage and returns our shield
            if not to_print:  # we want to modify the shield
                self.absorption_shield = damage.handle_absorption(self.absorption_shield)
Note: The Damage class has a method that deducts the damage given an absorption shield value. More on that here
The to_print boolean variable is used when we want to modify the damage variable only to print it later. 
To stress on it: to_print is True only when the returned variable of _apply_damage_absorption is used for printing exclusively,
not touching the Character's health/absorption shield at all.::
            else:
                damage.handle_absorption(self.absorption_shield) # only modify the specific damage in order to print it

        return damage

#. Finally, we subtract the damage from the Character's health::

    def _subtract_health(self, damage: Damage):
        """ This method is called whenever the health of the Character is damaged """
        self.health -= damage
        self.check_if_dead()

Well, I can't just leave you there without letting you see the check_if_dead method!::

    def check_if_dead(self):
        if self.health <= 0:
            self._die()

	####GOES TO####
    def _die(self):
        self._alive = False  # super()._die()
        print("Character {} has died!".format(self.name))

Join us next time where we delve into the zones system of the game and the overall loading of monsters/npcs

:any:`zones`

