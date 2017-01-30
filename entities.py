"""
This holds the classes for every entity in the game: Monsters and Characters currently
"""
import random
from termcolor import colored
from constants import (CHARACTER_DEFAULT_EQUIPMENT, CHARACTER_LEVELUP_BONUS_STATS, CHARACTER_LEVEL_XP_REQUIREMENTS,
                       KEY_ARMOR_ATTRIBUTE, KEY_STRENGTH_ATTRIBUTE, KEY_AGILITY_ATTRIBUTE, KEY_BONUS_HEALTH_ATTRIBUTE,
                       KEY_BONUS_MANA_ATTRIBUTE, KEY_LEVEL_STATS_HEALTH, KEY_LEVEL_STATS_MANA, CHAR_STARTER_ZONE,
                       CHAR_STARTER_SUBZONE, CHAR_ATTRIBUTES_TEMPLATE, MAXIMUM_LEVEL_DIFFERENCE_XP_YIELD)
from information_printer import print_level_up_event, print_vendor_products_for_sale
from exceptions import ItemNotInInventoryError, NonExistantBuffError
from utils.helper import create_character_attributes_template
from items import Item, Weapon, Potion, Equipment
from quest import Quest, FetchQuest
from decorators import has_item_in_stock
from damage import Damage
from buffs import BeneficialBuff, DoT


class LivingThing:
    """
    This is the base class for all things _alive - characters, monsters and etc.
    """

    def __init__(self, name: str, health: int = 1, mana: int = 1, level: int = 1):
        self.name = name
        self.health = health
        self.max_health = health
        self.mana = mana
        self.max_mana = mana
        self.level = level
        self.absorption_shield = 0
        self.attributes = {KEY_ARMOR_ATTRIBUTE: 0}
        self._alive = True
        self._in_combat = False
        self.buffs: {BeneficialBuff or DoT: int} = {}

    def is_alive(self):
        return self._alive

    def is_in_combat(self):
        return self._in_combat

    def enter_combat(self):
        self._in_combat = True

    def leave_combat(self):
        self._in_combat = False
        self._regenerate()

    def start_turn_update(self):
        """
        Here we handle all things that are turn based and dependant on the STAR tof the turn,
        For now: Damage over time effects only (DoT)
        """
        self._update_dots()

    def end_turn_update(self):
        """
        Here we handle all things that are turn based,
        For now: buff durations only
        """
        self._update_buffs()

    def _update_dots(self):
        """
        This method goes through all the DoT effects on the entity, activates their tick, reduces their duration
        and, if the are expired, adds them to a list which holds DoTs that should be removed(expired) from the character
        After iterating through all of the active DoTs, we remove every DoT that is in the list.
        """
        dots_to_remove = []  # type: list of DoTs

        # filter the DoTs from the character's buffs, iterate through active DoTs and reduce duration
        for dot in list(filter(lambda buff: isinstance(buff, DoT), self.buffs.keys())):
            # activate DoT effect
            self.take_dot_proc(dot)
            # reduce duration by 1 turn
            turns_left = self.buffs[dot]
            turns_left -= 1
            self.buffs[dot] = turns_left

            if not turns_left:  # if it is expired
                dots_to_remove.append(dot)

        # remove the buffs
        for dot in dots_to_remove:
            self.remove_buff(dot)

    def _update_buffs(self):
        """
        This method goes through all the Buffs on the netity, reduces their duration
        and, if they are expired (0 duration) adds them to a list which holds Buffs that should be removed (are expired)
        from the character.
        After iterating through all of the active Buffs, we remove every Buff that is in the list
        """
        buffs_to_remove: [BeneficialBuff] = []  # type: list of Buffs

        # iterate through active buffs and reduce duration
        for buff in filter(lambda bf: isinstance(bf, BeneficialBuff), self.buffs.keys()):
            # reduce duration by 1 turn
            turns_left = self.buffs[buff]
            turns_left -= 1
            self.buffs[buff] = turns_left

            if not turns_left:  # if it is expired
                buffs_to_remove.append(buff)

        # remove the buffs
        for buff in buffs_to_remove:
            self.remove_buff(buff)

    def remove_buff(self, buff: BeneficialBuff or DoT):
        """ Method that handles when a buff is removed/expired"""
        if buff not in self.buffs:
            raise NonExistantBuffError(f"Cannot remove {buff.name} from {self.name} because he does not have it!",
                                       buff.name)
        if isinstance(buff, BeneficialBuff):
            self._deapply_buff(buff)
            print(f"Buff {buff.name} has expired from {self.name}.")
        elif isinstance(buff, DoT):
            print(f"DoT {buff.name} has expired from {self.name}.")
        del self.buffs[buff]

    def add_buff(self, buff: BeneficialBuff or DoT):
        """ Method that handles when a buff is added to the player
        also adds DoTs to the list"""
        if buff in self.buffs:
            self._deapply_buff(buff)
        self.buffs[buff] = buff.duration
        if isinstance(buff, BeneficialBuff):
            self._apply_buff(buff)

    def _apply_buff(self, buff: BeneficialBuff):
        """ Add the buff to the living thing's stats"""
        buff_attributes: {str: int} = buff.get_buffed_attributes()

        # iterate through the buffed attributes and apply them to the entity
        for buff_type, buff_amount in buff_attributes.items():
            if buff_type == "health":
                if not self._in_combat:
                    self.health += buff_amount
                self.max_health += buff_amount
            elif buff_type == "mana":
                if not self._in_combat:
                    self.mana += buff_amount
                self.max_mana += buff_amount

    def _deapply_buff(self, buff: BeneficialBuff):
        """ Remove the buff from the living thing's stats"""
        buff_attributes = buff.get_buffed_attributes()  # type: dict

        # iterate through the buffed attributes and remove them from the entity
        for buff_type, buff_amount in buff_attributes.items():
            if buff_type == "health":
                # TODO: Reduce health method to reduce active health too, otherwise we can end up with 10/5 HP
                self.max_health -= buff_amount
                if self.health > self.max_health:
                    self.health = self.max_health
            elif buff_type == "mana":
                # TODO: Reduce mana method to reduce active mana too
                self.max_mana -= buff_amount
                if self.mana > self.max_mana:
                    self.mana = self.max_mana

    def _apply_armor_reduction(self, damage: Damage, attacker_level: int) -> Damage:
        """
        This method applies the armor reduction to a blow, the formula is as follows:
        Percentage to Reduce = Armor / (Armor + 400 + 85 * Attacker_Level)
        :param damage: the raw damage
        :return: the damage with the applied reduction
        """
        armor = self.attributes[KEY_ARMOR_ATTRIBUTE]

        reduction_percentage = armor / (armor + 400 + 85 * attacker_level)
        damage_to_deduct = damage.phys_dmg * reduction_percentage
        reduced_damage = damage.phys_dmg - damage_to_deduct

        return Damage(phys_dmg=reduced_damage, magic_dmg=damage.magic_dmg)

    def _regenerate(self):
        self.health = self.max_health
        self.mana = self.max_mana

    def _handle_overheal(self) -> float:
        """
        This method handles when a character is overhealed, by returning his health to his maximum possible health and
        returning the overheal amount
        :return: The amount we have overhealed for
        """
        overheal = self.health - self.max_health

        self.health = self.max_health

        return overheal

    def _subtract_health(self, damage: Damage):
        """ This method is called whenever the health of the LivingThing is damaged """
        self.health -= damage
        self.check_if_dead()

    def check_if_dead(self):
        if self.health <= 0:
            self._die()

    def take_dot_proc(self, dot: DoT):
        """ this method damages the entity for the dot's proc"""
        dot_proc_damage: Damage = dot.damage

        # due to the way Damage handles addition, subtraction and multiplication, the _calculate_level_difference_damage
        # method below works fine with Damage type
        # noinspection PyTypeChecker
        dot_proc_damage = self._calculate_level_difference_damage(damage_to_deal=dot_proc_damage,
                                                                  target_level=dot.level,
                                                                  inverse=True)
        if dot_proc_damage.phys_dmg:  # if there is physical damage in the DoT, apply armor reduction
            dot_proc_damage = self._apply_armor_reduction(damage=dot_proc_damage,
                                                          attacker_level=self.level)
        if self.absorption_shield:  # if we have a shield
            dot_proc_damage = self._apply_damage_absorption(dot_proc_damage)

        print(f'{self.name} suffers {dot_proc_damage} from {dot.name}!')
        self._subtract_health(dot_proc_damage)

    def _calculate_level_difference_damage(self, damage_to_deal: int, target_level: int, inverse: bool=False) -> int:
        """
        This method calculates the difference in damage according to the entity and the target's levels.
        For each level the target has above the Entity (self), the Entity's damage is reduced by 10%
        Vice-versa, for each level the Entity has above the Target, the Entity's damage is increased by 10%

        ex: self.level = 10, target_level = 5, damage_to_deal = 10
            The entity(self) would deal 50% more damage, resulting in a 15 damage swing, because of the 5 levels he has
            above the target
        :param target_level: The level of the target we want to attack
        :param inverse: If true, this means that we want to inverse this method, meaning we're not the one dealing
                        damage, but the one receiving it. Therefore we need to inverse the calculation, where if  the
                        level_difference < 0 (target is bigger level) we need to increase the damage and vice-versa
        :return: the damage as an int
        """
        level_difference = self.level - target_level
        percentage_mod = (abs(level_difference) * 0.1)  # calculates by how many % we're going to increase/decrease dmg

        if inverse:  # we take damage
            # 10% more or less damage for each level that differs
            if level_difference < 0:  # target is bigger level
                damage_to_deal += damage_to_deal * percentage_mod  # -X%
            elif level_difference > 0:  # entity is bigger level
                damage_to_deal -= damage_to_deal * percentage_mod  # +X%

        elif not inverse:  # we deal damage
            # 10% more or less damage for each level that differs
            if level_difference < 0:  # target is bigger level
                damage_to_deal -= damage_to_deal * percentage_mod  # -X%
            elif level_difference > 0:  # entity is bigger level
                damage_to_deal += damage_to_deal * percentage_mod  # +X%

        return damage_to_deal

    def _apply_damage_absorption(self, damage: Damage, to_print=False) -> Damage:
        """
        This method subtracts the absorption (if any) from the damage
        :param to_print: A boolean indicating if we want to actually subtract the damage from the shield. If it's true,
        we're getting the damage for the sole reason to print it only, therefore we should not modify anything
        :return Damage
        """

        if self.absorption_shield:  # if there is anything to absorb
            # lowers the damage and returns our shield
            if not to_print:  # we want to modify the shield
                self.absorption_shield = damage.handle_absorption(self.absorption_shield)
            else:
                damage.handle_absorption(self.absorption_shield) # only modify the specific damage in order to print it

        return damage

    def _die(self):
        self._alive = False

    def revive(self):
        self._regenerate()
        self._alive = True


class FriendlyNPC(LivingThing):
    """
    This is the class for friendly creatures in the world
    """

    def __init__(self, name: str, health: int = 1, mana: int = 1, level: int = 1, min_damage: int = 0,
                 max_damage: int=1, quest_relation_id=0, loot_table: 'LootTable'=None, gossip: str = 'Hello'):
        super().__init__(name, health, mana, level)
        self.level = level
        self.min_damage = min_damage
        self.max_damage = max_damage
        self.gossip = gossip
        self.colored_name = colored(self.name, color='green')

    def __str__(self):
        return f'{self.colored_name}'

    def talk(self, player_name: str):
        print(f'{self.colored_name} says: {self.gossip.replace("$N", player_name)}')


class VendorNPC(FriendlyNPC):
    """
    This is the class for the vendor NPCs in the world
    """

    def __init__(self, name: str, entry: int, inventory: dict, health: int=1, mana: int=1, level: int=1,
                 min_damage: int=0, max_damage: int=1, quest_relation_id=0,
                 loot_table: 'LootTable'=None, gossip: str='Hello'):
        super().__init__(name, health, mana, level, min_damage, max_damage, quest_relation_id, loot_table, gossip)
        self.entry = entry
        self.inventory = inventory

    def __str__(self):
        return f'{self.colored_name} <Vendor>'

    def has_item(self, item_name: str) -> bool:
        """
        Checks if the vendor has the item in stock
        :param item_name: The name of the item in a string
        :return: A boolean indicating if we have it or not
        """
        return item_name in self.inventory.keys()

    @has_item_in_stock
    def get_item_info(self, item_name: str) -> Item:
        """
        USED ONLY FOR PRINTING/TESTING PURPOSES
        Returns the item we want to get from the vendor,
        """
        return self.inventory[item_name][0]  # returns the item object

    @has_item_in_stock
    def get_item_price(self, item_name: str) -> int:
        """Returns the price the vendor sells the item for"""
        item, _ = self.inventory[item_name]
        return item.buy_price

    @has_item_in_stock
    def sell_item(self, item_name: str) -> tuple:
        """ Returns a tuple(1,2,3)
            1 - the item object type: Item
            2 - the number of items type: int
            3 - the price of the item type: int"""
        item, item_count = self.inventory[item_name]
        item_price = item.buy_price

        del self.inventory[item_name]

        return item, item_count, item_price


class Monster(LivingThing):
    def __init__(self, monster_id: int, name: str, health: int = 1, mana: int = 1, level: int = 1, min_damage: int = 0,
                 max_damage: int = 1, quest_relation_id=0, xp_to_give: int=0,
                 gold_to_give_range: (int, int)=(0, 0), loot_table: 'LootTable'=None, armor: int=0, gossip: str='',
                 respawnable: bool=False):
        super().__init__(name, health, mana, level)
        self.monster_id = monster_id
        self.level = level
        self.min_damage = min_damage
        self.max_damage = max_damage
        self.xp_to_give = xp_to_give
        self.attributes[KEY_ARMOR_ATTRIBUTE] = armor
        self.gossip = gossip
        self.respawnable = respawnable  # says if the creature can ever respawn, once killed of course
        self._gold_to_give = self._calculate_gold_reward(gold_to_give_range)
        self.quest_relation_id = quest_relation_id
        self.loot_table = loot_table
        self.loot = {"gold": self._gold_to_give}  # dict Key: str, Value: Item class object

    def __str__(self):
        colored_name = colored(self.name, color="red")
        return f'Creature Level {self.level} {colored_name} - {self.health}/{self.max_health} HP ' \
               f'| {self.mana}/{self.max_mana} Mana | {self.min_damage}-{self.max_damage} Damage'

    def get_auto_attack_damage(self, target_level: int):
        # get the base auto attack damage
        damage_to_deal = random.randint(self.min_damage, self.max_damage)
        # factor in the level difference
        damage_to_deal = self._calculate_level_difference_damage(damage_to_deal, target_level)

        return Damage(phys_dmg=damage_to_deal)

    def attack(self, victim: 'Character'):
        monster_swing: Damage = self.get_auto_attack_damage(victim.level)

        victim.take_attack(self.name, monster_swing, self.level)

    def take_attack(self, damage: Damage, attacker_level: int):
        damage = self._apply_armor_reduction(damage, attacker_level)
        damage = self._apply_damage_absorption(damage)
        self._subtract_health(damage)

    def get_take_attack_damage_repr(self, damage: Damage, attacker_level: int) -> Damage:
        """ this method returns the damage that the monster will suffer after taking into account
        armor and absorption. This is used for printing the result
        Currently: Only armor reduction and damage absorption is applied."""
        return self._apply_damage_absorption(self._apply_armor_reduction(damage, attacker_level), to_print=True)

    def _drop_loot(self):
        """
        This method fills up the self.loot dictionary with the items that have dropped off the monster
        """
        if not self.loot_table:
            return
        dropped_items: [Item] = self.loot_table.decide_drops()

        for item in dropped_items:
            self.loot[item.name] = item

    def give_loot(self, item_name: str):
        """ Returns the item that's looted and removes it from the monster's inventory"""
        if item_name not in self.loot:
            print(f'{self.name} did not drop {item_name}.')
            return False

        item: Item = self.loot[item_name]
        del self.loot[item_name]  # remove it as it's looted
        return item

    def _die(self):
        super()._die()
        self._drop_loot()
        print(f'Creature {self.name} has died!')

    def _calculate_gold_reward(self, min_max_gold: tuple) -> int:
        """ Calculate the gold this monster is going to award the player
            min_max_gold: A tuple containing the minimum and maximum amount of gold a creature of this level can give
            (2,5) meaning this creature should give from 2-5 gold, picked at random"""
        return random.randint(min_max_gold[0], min_max_gold[1])

    def say_gossip(self):
        if self.gossip:
            punctuation_mark = self.gossip[-1]

            if punctuation_mark == '!':
                verb = 'yells'
            elif punctuation_mark == '?':
                verb = 'asks'
            else:
                verb = 'says'

            print(f'{self.name} {verb}: {self.gossip}')


class Character(LivingThing):
    def __init__(self, name: str, health: int = 1, mana: int = 1, strength: int = 1, agility: int = 1,
                 loaded_scripts: set=set(), killed_monsters: set=set(), completed_quests: set=set(),
                 saved_inventory: dict={'gold': 0}, saved_equipment: dict=CHARACTER_DEFAULT_EQUIPMENT):
        super().__init__(name, health, mana, level=0)
        self.min_damage = 0
        self.max_damage = 1
        self.equipped_weapon = Weapon(name="Starter Weapon", item_id=0)
        self.experience = 0
        self.xp_req_to_level = 400
        self._bonus_health = 0
        self._bonus_mana = 0
        self._bonus_strength = 0
        self._bonus_armor = 0
        self.attributes: {str: int} = create_character_attributes_template()
        self._level_up(False)  # level up to 1
        self.current_zone = CHAR_STARTER_ZONE
        self.current_subzone = CHAR_STARTER_SUBZONE
        # holds the scripts that the character has seen (which should load only once)
        self.loaded_scripts: set() = loaded_scripts
        # holds the GUIDs of the creatures that the character has killed (and that should not be killable a second time)
        self.killed_monsters: set() = killed_monsters
        self.completed_quests: set() = completed_quests  # ids of the quests that the character has completed
        self.quest_log = {}
        self.inventory = saved_inventory # dict Key: str, Value: tuple(Item class instance, Item Count)
        self.equipment = saved_equipment # dict Key: Equipment slot, Value: object of class Equipment
        self._handle_load_saved_equipment()  # add up the attributes for our saved_equipment

    def start_turn_update(self):
        super().start_turn_update()
        self.update_spell_cooldowns()

    def add_item_to_inventory(self, item: Item, item_count=1):
        count = item_count
        if item.name in self.inventory:
            count += self.inventory[item.name][1]

        self.inventory[item.name] = (item, count)

    def equip_item(self, item: Item):
        """
        This method equips an item to the character and handles the appropriate change in inventory following the equip
        (equipped item goes back to the inventory and the item to be equipped is removed from the inventory)
        :param item:
        :return:
        """
        if isinstance(item, Weapon):
            item_in_inventory, count = self.inventory[item.name]

            # remove the item we're equipping from the inventory
            if count == 1:  # remove from the inventory
                del self.inventory[item.name]
            else:  # reduce it's count
                self.inventory[item.name] = item_in_inventory, count-1

            # transfer the equipped weapon to the inventory
            eq_weapon = self.equipped_weapon

            self.add_item_to_inventory(eq_weapon)

            self._subtract_attributes(eq_weapon.attributes)  # remove the attributes it has given us
            self._equip_weapon(item)
        elif isinstance(item, Equipment):
            item_in_inventory, count = self.inventory[item.name]

            # remove the item we're equipping from the inventory
            if count == 1:  # remove from the inventory
                del self.inventory[item.name]
            else:  # reduce it's count
                self.inventory[item.name] = item_in_inventory, count - 1

            # transfer the equipped item back to the inventory
            # TODO: Handle custom error if there isn't such a slot in the equipment
            equipped_item: Equipment = self.equipment[item.slot]

            if equipped_item:
                self.add_item_to_inventory(equipped_item)
                self._subtract_attributes(equipped_item.attributes)

            self._equip_gear(item)

        self._calculate_stats_formulas()  # always recalculate formulas when adding an item

    def consume_item(self, item: Item):
        """
        This method consumes a consumable item and processes the item's effect
        :param item: an instance of class Item
        """
        if isinstance(item, Potion):
            potion: Potion = item
            potion_in_inventory, count = self.inventory[potion.name]

            # remove the potion we're consuming from the inventory
            if count == 1:  # remove from the inventory
                del self.inventory[potion.name]
            else:  # reduce it's count
                self.inventory[potion.name] = potion_in_inventory, count - 1

            print(f'{self.name} drinks {potion.name} and is afflicted by {potion.get_buff_name()}')
            # call the potion's consume method
            potion.consume(self)

    def _equip_weapon(self, weapon: Weapon):
        print(f'{self.name} has equipped Weapon {weapon.name}')
        self.equipped_weapon = weapon
        self._add_attributes(weapon.attributes)

    def _equip_gear(self, item: Equipment):
        """ equip an equipment item like a Headpiece, Shoulderpad, Chestguard and etc."""
        print(f'{self.name} has equipped {item.slot} {item.name}')
        self.equipment[item.slot] = item
        self._add_attributes(item.attributes)

    def _add_attributes(self, attributes: dict):
        """ this function goes through a dictionary that holds character attributes and adds them
        with the character's. Called whenever we equip an item
        We directly apply it to the character's attributes dictionary because we trust that the
        argument has gone through helper.py's create_attributes function
        and has valid attribute names"""
        for attribute_name, attribute_value in attributes.items():
            self.attributes[attribute_name] += attribute_value
        self._calculate_stats_formulas()

    def _subtract_attributes(self, attributes: dict):
        """ this function goes through a dictionary that holds character attributes and adds them
            with the character's. Called whenever we dequip an item
            We directly apply it to the character's attributes dictionary because we trust that the
            argument has gone through helper.py's create_attributes function
            and has valid attribute names"""
        for attribute_name, attribute_value in attributes.items():
            # we also trust that the values cannot be negative after the subtraction, because the same amount has
            # been added beforehand and we currently do not support any features that lower a character's
            # attributes outside of combat, where he will not be able to dequip an item
            self.attributes[attribute_name] -= attribute_value
        self._calculate_stats_formulas()

    def _calculate_stats_formulas(self):
        """
        Whenever we level up or equip an item, our stats are changed.
        According to that change, we need to recalculate the formulas in which those stats are used in.
        """

        # update health according to bonus health
        orig_max_h = self.max_health
        self.max_health -= self._bonus_health  # remove the old bonus health
        self._bonus_health = self.attributes[KEY_BONUS_HEALTH_ATTRIBUTE]  # update bonus health
        self.max_health += self._bonus_health  # add bonus health again
        orig_max_m = self.max_mana
        self.max_mana -= self._bonus_mana
        self._bonus_mana = self.attributes[KEY_BONUS_MANA_ATTRIBUTE]
        self.max_mana += self._bonus_mana

        self._handle_health_change(orig_max_h)
        self._handle_mana_change(orig_max_m)

        # formula for agility is: for each point of agility, add 2.5 armor and 0.5 strength
        agility = self.attributes[KEY_AGILITY_ATTRIBUTE]

        # remove the old bonus strength/armor
        self.attributes[KEY_STRENGTH_ATTRIBUTE] -= self._bonus_strength
        self.attributes[KEY_ARMOR_ATTRIBUTE] -= self._bonus_armor
        # recalculate them
        self._bonus_strength = agility * 0.5
        self._bonus_armor = agility * 2.5
        # add them back again
        self.attributes[KEY_STRENGTH_ATTRIBUTE] += self._bonus_strength
        self.attributes[KEY_ARMOR_ATTRIBUTE] += self._bonus_armor

        "Now we need to update our damage, because the strength might have been changed"

        # current formula for damage is: wep_dmg * 0.4 * strength
        strength = self.attributes[KEY_STRENGTH_ATTRIBUTE]
        self.min_damage = self.equipped_weapon.min_damage + (0.4 * strength)
        self.max_damage = self.equipped_weapon.max_damage + (0.4 * strength)

    def _handle_health_change(self, orig_max_h):
        """ Handles cases where the maximum health of the Character has been changed"""
        if orig_max_h < self.max_health and not self.is_in_combat():  # Has increased
            # Increase the current health only if the character is out of combat
            hp_increase = self.max_health - orig_max_h
            self.health += hp_increase
        elif orig_max_h > self.max_health:  # Has decreased
            hp_decrease = orig_max_h - self.max_health
            if self.health > self.max_health:
                self.health -= hp_decrease
                if self.health != self.max_health:
                    raise Exception('Expected health to be equal to the max hp once decreased')
            elif not self.is_in_combat():
                """
                If the character's health is not over the max_health and only out of combat,
                decrease his current HP
                """
                self.health -= hp_decrease

    def _handle_mana_change(self, orig_max_m):
        """ Handles cases where the maximum mana of the Character has been changed"""
        if orig_max_m < self.max_mana and not self.is_in_combat():  # Has increased
            # Increase the current mana only if the character is out of combat
            m_increase = self.max_mana - orig_max_m
            self.mana += m_increase
        elif orig_max_m > self.max_mana:  # Has decreased
            m_decrease = orig_max_m - self.max_mana
            if self.mana > self.max_mana:
                self.mana -= m_decrease
                if self.mana != self.max_mana:
                    raise Exception('Expected mana to be equal to the max hp once decreased')
            elif not self.is_in_combat():
                """
                If the character's mana is not over the max_mana and only out of combat,
                decrease his current HP
                """
                self.mana -= m_decrease

    def spell_handler(self, command: str, target: Monster):
        """
        Every class will have different spells, this method will make sure the proper spell is caster
        :param command: the spell name that is to be cast
        :param target: The target on which the spell is going to be cast
        :return:
        """
        pass

    def get_auto_attack_damage(self, target_level: int) -> Damage:
        # get the base auto attack damage
        damage_to_deal = random.randint(int(self.min_damage), int(self.max_damage))
        # factor in the level difference
        damage_to_deal = self._calculate_level_difference_damage(damage_to_deal, target_level)

        return Damage(phys_dmg=damage_to_deal)

    def attack(self, victim: Monster):
        pass

    def take_attack(self, monster_name: str, damage: Damage, attacker_level: int):
        damage = self._apply_armor_reduction(damage, attacker_level)
        damage = self._apply_damage_absorption(damage)

        print(f'{monster_name} attacks {self.name} for {damage}!')
        self._subtract_health(damage)

    def _apply_buff(self, buff: BeneficialBuff):
        """ Add the buffed attributes to the character's stats"""
        buff_attributes: {str: int} = buff.get_buffed_attributes()

        # iterate through the buffed attributes and apply them to the character
        for buff_type, buff_amount in buff_attributes.items():
            if buff_type == "health":
                self.attributes[KEY_BONUS_HEALTH_ATTRIBUTE] += buff_amount
            elif buff_type == "mana":
                self.attributes[KEY_BONUS_MANA_ATTRIBUTE] += buff_amount
            else:
                self.attributes[buff_type] += buff_amount

            self._calculate_stats_formulas()  # always recalculate the formulas when stats are changed

    def _deapply_buff(self, buff: BeneficialBuff):
        """ Remove the buff from the character's stats"""
        buff_attributes: {str: int} = buff.get_buffed_attributes()

        # iterate through the buffed attributes and remove them from the character
        for buff_type, buff_amount in buff_attributes.items():
            if buff_type == "health":
                self.attributes[KEY_BONUS_HEALTH_ATTRIBUTE] -= buff_amount
            elif buff_type == "mana":
                self.attributes[KEY_BONUS_MANA_ATTRIBUTE] -= buff_amount
            else:
                self.attributes[buff_type] -= buff_amount

            self._calculate_stats_formulas()  # always recalculate the formulas when stats are changed

    def _die(self):
        super()._die()
        print(f'Character {self.name} has died!')

    def has_enough_gold(self, gold: int) -> bool:
        """
        :return: a boolean indicating if we have that much gold
        """
        return self.inventory['gold'] >= gold

    def has_item(self, item: str) -> bool:
        """ This method checks if the character has the item in his inventory"""
        if item == 'gold':
            # gold is a special keyword used to store the gold in the inventory
            return False

        return item in self.inventory.keys()

    def buy_item(self, sale: (Item, int, int)):
        """
        This method is used when we buy an item from a vendor. It subtracts the price of the item from our gold and
        gives us the item in our inventory
        :param sale: A Tuple(1,2,3)
                        1 - the item object type: Item
                        2 - the number of items type: int
                        3 - the price of the item type: int
        """
        item, item_count, item_price = sale

        self.inventory['gold'] -= item_price

        self.award_item(item, item_count)

    def sell_item(self, item_name: str):
        """
        This method is used when the character sells an item to the vendor.
        We give **him** the item and he gives us gold for it
        """
        item, item_count = self.inventory[item_name]

        # remove the item from the inventory
        if item_count == 1:
            del self.inventory[item.name]
        else:
            self.inventory[item_name] = (item, item_count-1)

        gold_award = item.sell_price
        print(f'You have sold {item_name} for {gold_award} gold.')
        print()
        self.award_gold(gold_award)

    def add_quest(self, quest: Quest):
        if quest.ID in self.quest_log:
            raise Exception(f'{quest.name} is already in your quest log!')

        self.quest_log[quest.ID] = quest
        # there are some cases where the quest can be completed on accept, i.e having the required items
        quest.check_if_complete(self)
        self._check_if_quest_completed(quest)

    def _check_if_quest_completed(self, quest: Quest):
        if quest.ID not in self.quest_log:
            raise Exception(f'You do not have {quest.name} in your quest log!')
        if quest.is_completed:
            self._complete_quest(quest)

    def _complete_quest(self, quest: Quest):
        item_reward = quest.give_item_rewards()
        xp_reward = quest.give_reward()

        if isinstance(quest, FetchQuest):
            # if we just completed a fetch quest, we need to remove the required items for the quest
            self._remove_fetch_quest_required_items(quest)

        print(f'Quest {quest.name} is completed! XP awarded: {quest.xp_reward}!')
        if isinstance(item_reward, Item):
            print(f'{self.name} is awarded {item_reward.name} from the quest {quest.name}!')
            self.award_item(item_reward)
        elif isinstance(item_reward, list):
            for item in item_reward:
                print(f'{self.name} is awarded {item.name} from the quest {quest.name}!')
                self.award_item(item)

        del self.quest_log[quest.ID]  # remove from quest log

        self.completed_quests.add(quest.ID)
        self._award_experience(xp_reward)

    def _remove_fetch_quest_required_items(self, quest: FetchQuest):
        item_name, count = quest.required_item, quest.required_item_count

        self._remove_item_from_inventory(item_name=item_name, item_count=count)

    def _award_experience(self, xp_reward: int):
        """ Method that awards experience to the player and checks if he levels up"""
        self.experience += xp_reward
        self.check_if_levelup()

    def award_monster_kill(self, monster: Monster, monster_guid: int):
        """
        This method is called whenever a Monster is killed. It gives the monster's XP reward,
                counts him for the appropriate quest (if there is one) and adds him to the killed_monsters
                (if he's not respawnable)
        """
        monster_level = monster.level
        xp_reward = monster.xp_to_give
        monster_quest_ID = monster.quest_relation_id

        level_difference = self.level - monster_level
        xp_bonus_reward = 0
        if level_difference >= MAXIMUM_LEVEL_DIFFERENCE_XP_YIELD:
            xp_reward = 0
        elif level_difference < 0:  # monster is higher level
            # 10% increase of XP for every level the monster has over player
            percentage_mod = abs(level_difference) * 0.1
            xp_bonus_reward += int(xp_reward * percentage_mod)  # convert to int

        if xp_bonus_reward:
            print(f'XP awarded: {xp_reward} + bonus {xp_bonus_reward} for the level difference!')
        else:
            print(f'XP awarded: {xp_reward}!')

        if not monster.respawnable:
            self.killed_monsters.add(monster_guid)

        self._award_experience(xp_reward + xp_bonus_reward)

        # If this monster is for a quest and we have that quest
        if monster_quest_ID and monster_quest_ID in self.quest_log:
            self.quest_log[monster_quest_ID].update_kills()

            self._check_if_quest_completed(quest)

    def award_gold(self, gold: int):
        self.inventory['gold'] += gold

    def award_item(self, item: Item, item_count=1):
        """ Take an item and put it into the character's inventory,
        store it as a tuple holding (Item Object, Item Count) """
        item_quest_id = item.quest_id

        self.add_item_to_inventory(item, item_count)

        if item_quest_id and item_quest_id in self.quest_log and not self.quest_log[item_quest_id].is_completed:
            # if the item is related to a quest and if we have that quest and said quest is not completed
            temp_quest = self.quest_log[item_quest_id]

            # have the quest check if the player has enough items to complete it
            temp_quest.check_if_complete(self.inventory)

            self.quest_log[item_quest_id] = temp_quest

            self._check_if_quest_completed(temp_quest)

    def _remove_item_from_inventory(self, item_name: str, item_count: int=1, remove_all: bool = False):
        """ This method removes the specified item from the player's inventory
            :param item_count: the count we want to remove, ex: we may want to remove 2 Wolf Meats, as opposed to one
            :param remove_all: simply removes all the items, with this variable set to True, item_count is useless"""
        if item_name not in self.inventory.keys():
            raise ItemNotInInventoryError(f'{item_name} is not in {self.name}\'s inventory!',
                                          inventory=self.inventory, item_name=item_name)

        if remove_all:
            del self.inventory[item_name]
        else:
            item, count_in_inventory = self.inventory[item_name]

            # subtract the number of items we're removing from the number we have
            resulting_count = count_in_inventory - item_count

            if resulting_count <= 0:
                # if it's 0 or less, remove the key/value pair
                del self.inventory[item_name]
            else:
                # if we have items left, simply reduce their count
                self.inventory[item_name] = item, resulting_count

    def _handle_load_saved_equipment(self):
        """
        This function is used to add the attributes of all the character's equipment.
        NOTE: This is used only on the initial character load
        """
        for item in filter(lambda itm: itm is not None, self.equipment.values()):
            self._add_attributes(item.attributes)

    def check_if_levelup(self):
        if self.experience >= self.xp_req_to_level:
            self._level_up()
            self.experience = 0
            self.xp_req_to_level = self._lookup_next_xp_level_req()

    def _level_up(self, to_print=True):
        self.level += 1

        current_level_stats = CHARACTER_LEVELUP_BONUS_STATS[self.level]
        # access the dictionary holding the appropriate value increases for each level
        hp_increase_amount = current_level_stats[KEY_LEVEL_STATS_HEALTH]
        mana_increase_amount = current_level_stats[KEY_LEVEL_STATS_MANA]
        strength_increase_amount = current_level_stats[KEY_STRENGTH_ATTRIBUTE]
        agility_increase_amount = current_level_stats[KEY_AGILITY_ATTRIBUTE]
        armor_increase_amount = current_level_stats[KEY_ARMOR_ATTRIBUTE]

        self.max_health += hp_increase_amount
        self.max_mana += mana_increase_amount
        self.attributes[KEY_STRENGTH_ATTRIBUTE] += strength_increase_amount
        self.attributes[KEY_ARMOR_ATTRIBUTE] += armor_increase_amount
        self.attributes[KEY_AGILITY_ATTRIBUTE] += agility_increase_amount
        self._calculate_stats_formulas()  # recalculate formulas with stats
        self._regenerate()  # regen to full hp/mana

        print_level_up_event(name=self.name, level=self.level, armor_inc=armor_increase_amount,
                             hp_inc=hp_increase_amount, mana_inc=mana_increase_amount,
                             strength_inc=strength_increase_amount, agi_inc=agility_increase_amount)

    def print_inventory(self):
        print("Your inventory:")

        # print the gold separately so it always comes up on top
        print(f"\t{self.inventory['gold']} gold")
        for key, item_tuple in self.inventory.items():
            if key is not 'gold':
                item, item_count = item_tuple
                print(f'\t{item_count} {item}')

    def _lookup_next_xp_level_req(self):
        return CHARACTER_LEVEL_XP_REQUIREMENTS[self.level]

    def loaded_script(self, script_name: str):
        """
        This method is called whenever the character loads a script that should be loaded only once
        It adds the script's name in the character's loaded_scripts set, which is checked every time a
        script wants to load. Thus that script will never load again for the same character.
        :param script_name: the name of the script
        """
        self.loaded_scripts.add(script_name)

    def has_loaded_script(self, script_name: str) -> bool:
        """
        Returns a boolean whether the character has loaded the script before or not
        """
        return script_name in self.loaded_scripts

    def has_killed_monster(self, monster_guid: int) -> bool:
        """
        Returns a boolean whether the character has killed the specified monster before
        """
        return monster_guid in self.killed_monsters

    def has_completed_quest(self, quest_id: str) -> bool:
        """
        Returns a boolean whether the character has completed the specified quest before
        """
        return quest_id in self.completed_quests

    def update_spell_cooldowns(self):
        """
        This method is called at the start of every turn
        It reduces the active cooldowns of our spells by 1, because a turn has passed
        """
        for spell in self.learned_spells.values():
            spell.pass_turn()

    def get_class(self) -> str:
        """Returns the class of the character as a string"""
        pass
