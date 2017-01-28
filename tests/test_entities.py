import unittest
from unittest.mock import Mock
import sys
import termcolor
from io import StringIO
from copy import deepcopy
from collections import Counter
from exceptions import NonExistantBuffError

from constants import (
    KEY_ARMOR_ATTRIBUTE, CHARACTER_DEFAULT_EQUIPMENT, CHARACTER_LEVELUP_BONUS_STATS, CHAR_STARTER_SUBZONE,
    CHAR_STARTER_ZONE)
from entities import LivingThing, FriendlyNPC, VendorNPC, Monster, Character
from damage import Damage
from utils.helper import create_attributes_dict
from items import Item, Equipment, Weapon, Potion
from buffs import BeneficialBuff, DoT


class LivingThingTests(unittest.TestCase):
    def setUp(self):
        self.name = 'Alex'
        self.health = 100
        self.mana = 100
        self.level = 5
        self.dummy_buff = BeneficialBuff(name='Zdrave', buff_stats_and_amounts=[('health', self.health)], duration=5)
        self.dummy_dot = DoT(name='Disease', damage_tick=Damage(phys_dmg=15), duration=2, caster_lvl=self.level)
        self.expected_attributes = {KEY_ARMOR_ATTRIBUTE: 0}  # the base stat for every creature
        self.dummy = LivingThing(name=self.name, health=self.health, mana=self.mana, level=self.level)

    def test_init(self):
        self.assertEqual(self.dummy.name, self.name)
        self.assertEqual(self.dummy.health, self.health)
        self.assertEqual(self.dummy.max_health, self.health)
        self.assertEqual(self.dummy.mana, self.mana)
        self.assertEqual(self.dummy.max_mana, self.mana)
        self.assertEqual(self.dummy.level, self.level)
        self.assertEqual(self.dummy.absorption_shield, 0)
        self.assertEqual(self.dummy.attributes, self.expected_attributes)
        self.assertTrue(self.dummy._alive)
        self.assertFalse(self.dummy._in_combat)
        self.assertEqual(self.dummy.buffs, {})  # should not have any buffs on creation

    def test_enter_in_leave_combat_methods(self):
        """
        The is_in_combat function should return whether the object is in combat
            enter_combat should put him in combat
            leave_combat should leave combat and regenerate the living thing
        """
        self.assertFalse(self.dummy.is_in_combat())
        self.dummy.enter_combat()  # enter combat
        self.assertTrue(self.dummy.is_in_combat())

        self.assertEqual(self.dummy.health, self.health)
        self.dummy.health -= 50
        self.assertNotEqual(self.dummy.health, self.health)

        self.dummy.leave_combat()
        # Should have left combat and regenerated health
        self.assertFalse(self.dummy.is_in_combat())
        self.assertEqual(self.dummy.health, self.health)

    def test_subtract_health(self):
        """
        The subtract_health removes health from the LivingThing and check if it has died from that result
        If it has, it calls the _die method which turns self.alive to false
        """
        self.assertTrue(self.dummy.health > 0)
        self.dummy._subtract_health(self.dummy.health)
        # should be at 0 health and dead
        self.assertEqual(self.dummy.health, 0)
        self.assertFalse(self.dummy.is_alive())

    def test_regenerate(self):
        """
        The regenerate function should reset the character's health/mana to it's max
        """
        self.dummy.health -= 50
        self.dummy.mana -= 50
        self.assertNotEqual(self.dummy.health, self.health)
        self.assertNotEqual(self.dummy.mana, self.mana)
        self.dummy._regenerate()
        self.assertEqual(self.dummy.health, self.health)
        self.assertEqual(self.dummy.mana, self.mana)

    def test_handle_overheal(self):
        """
        handle_overheal is a helper function which returns the amount we've been overhealed by
        and resets the health to the maximum
        """
        overheal_amount = 10
        self.dummy.health += overheal_amount
        self.assertGreater(self.dummy.health, self.dummy.max_health)

        received_overheal_amount = self.dummy._handle_overheal()
        self.assertEqual(received_overheal_amount, overheal_amount)
        # should have reset the health
        self.assertEqual(self.dummy.health, self.dummy.max_health)

    def test_add_buff(self):
        """
        The add_buff method should add a DoT/BeneficialBuff to the character's self.buffs dictionary.
        It should also apply the buff's stats to the character (if it's a BeneficialBuff)
        """
        self.assertEqual(self.dummy.buffs, {})
        self.dummy.add_buff(self.dummy_buff)
        self.assertEqual(self.dummy.buffs, {self.dummy_buff: self.dummy_buff.duration})
        # check if the buff has been applied
        # because the buff has been applied out of combat, his current health should get buffed
        self.assertNotEqual(self.dummy.health, self.health)
        self.assertEqual(self.dummy.max_health, self.health + self.dummy_buff.buff_amounts['health'])
        self.assertEqual(self.dummy.health, self.health + self.dummy_buff.buff_amounts['health'])

    def test_add_multiple_buffs(self):
        """
        If it is the same buff, it should just overwrite itself on the duration
        """
        self.assertEqual(self.dummy.buffs, {})
        self.dummy.add_buff(self.dummy_buff)
        self.assertEqual(self.dummy.buffs, {self.dummy_buff: self.dummy_buff.duration})
        self.dummy.buffs[self.dummy_buff] = 0  # reset the duration
        self.dummy.add_buff(self.dummy_buff)

        # health should have been increased only once
        self.assertNotEqual(self.dummy.health, self.health)
        self.assertEqual(self.dummy.max_health, self.health + self.dummy_buff.buff_amounts['health'])
        self.assertEqual(self.dummy.health, self.health + self.dummy_buff.buff_amounts['health'])

    def test_remove_buff(self):
        """
        The remove_buff method should be called whenever a buff has expired from the character.
        It should remove the buff from the character's buffs dictionary and remove the bonuses it gave him
        """
        expected_output = f'Buff {self.dummy_buff.name} has expired from {self.name}.'
        output = StringIO()
        try:
            sys.stdout = output
            self.dummy.add_buff(self.dummy_buff)
            # assert that the health has been increased
            self.assertEqual(self.dummy.max_health, self.health + self.dummy_buff.buff_amounts['health'])
            self.assertEqual(self.dummy.health, self.health + self.dummy_buff.buff_amounts['health'])

            # assert that the health and buff has been removed
            self.dummy.remove_buff(self.dummy_buff)
            self.assertEqual(self.dummy.buffs, {})
            self.assertEqual(self.dummy.max_health, self.health)
            self.assertEqual(self.dummy.health, self.health)

            self.assertIn(expected_output, output.getvalue())
        finally:
            sys.stdout = sys.__stdout__

    def test_update_buffs(self):
        """
        The _update_buffs function goes through every buff and reduces its duration.
        It also removes buffs once their duration has passed :0
        """
        self.dummy.add_buff(self.dummy_buff)

        for i in range(self.dummy_buff.duration - 1):
            self.assertNotEqual(self.dummy.health, self.health)
            self.assertEqual(self.dummy.max_health, self.health + self.dummy_buff.buff_amounts['health'])
            self.assertEqual(self.dummy.health, self.health + self.dummy_buff.buff_amounts['health'])

            self.dummy._update_buffs()

            self.assertEqual(self.dummy.buffs[self.dummy_buff], self.dummy_buff.duration - (i+1))

        self.assertEqual(self.dummy.buffs[self.dummy_buff], 1)
        self.dummy._update_buffs()
        # the buff should have been removed and the health reduced
        self.assertEqual(self.dummy.buffs, {})
        self.assertEqual(self.dummy.health, self.health)

    def test_end_turn_update(self):
        """
        the end_turn_update is called whenever the character's turn ends. It currently
        only calls the _update_buffs() function, which lowers the duration on all of our buffs by one turn
        :return:
        """
        self.dummy.add_buff(self.dummy_buff)

        for i in range(self.dummy_buff.duration - 1):
            self.assertNotEqual(self.dummy.health, self.health)
            self.assertEqual(self.dummy.max_health, self.health + self.dummy_buff.buff_amounts['health'])
            self.assertEqual(self.dummy.health, self.health + self.dummy_buff.buff_amounts['health'])

            self.dummy.end_turn_update()

            self.assertEqual(self.dummy.buffs[self.dummy_buff], self.dummy_buff.duration - (i + 1))

        self.assertEqual(self.dummy.buffs[self.dummy_buff], 1)
        self.dummy.end_turn_update()
        # the buff should have been removed and the health reduced
        self.assertEqual(self.dummy.buffs, {})
        self.assertEqual(self.dummy.health, self.health)

    def test_take_dot_proc(self):
        """
        The take_dot_proc method damages the character for the DoT's damage per tick
        """
        output = StringIO()
        expected_message = f'{self.name} suffers {self.dummy_dot.damage} from {self.dummy_dot.name}!'
        try:
            sys.stdout = output
            self.dummy.take_dot_proc(self.dummy_dot)

            # assert that health has been reduced
            self.assertLess(self.dummy.health, self.health)
            self.assertIn(expected_message, output.getvalue())

            # try to kill him using the dot proc
            for _ in range(100):
                self.dummy.take_dot_proc(self.dummy_dot)
            self.assertLess(self.dummy.health, 0)
            self.assertFalse(self.dummy.is_alive())
        finally:
            sys.stdout = sys.__stdout__

    def test_update_dots(self):
        """
        The _update_dots function reduces the duration of each dot and activates its damage tick
        """
        output = StringIO()
        try:
            sys.stdout = output
            orig_health = self.dummy.health
            first_dot = DoT(name='first', damage_tick=Damage(5), duration=3, caster_lvl=2)
            second_dot = DoT(name='second', damage_tick=Damage(2), duration=5, caster_lvl=2)
            self.dummy.add_buff(first_dot)
            self.dummy.add_buff(second_dot)
            self.assertEqual(self.dummy.buffs, {first_dot: 3, second_dot: 5})

            self.dummy._update_dots()
            # should have reduced the durations
            self.assertEqual(self.dummy.buffs, {first_dot: 2, second_dot: 4})
            # should have subtracted health
            self.assertLess(self.dummy.health, orig_health)
            health_after_first_tick = self.dummy.health

            self.dummy._update_dots()
            self.dummy._update_dots()
            self.assertLess(self.dummy.health, health_after_first_tick)
            # should have removed the first dot
            self.assertEqual(self.dummy.buffs, {second_dot: 2})
            health_after_second_tick = self.dummy.health

            self.dummy._update_dots()
            self.dummy._update_dots()
            self.assertLess(self.dummy.health, health_after_second_tick)
            self.assertEqual(self.dummy.buffs, {})

            stdout_result = output.getvalue()
            self.assertIn('suffers', stdout_result)
            self.assertIn(f'DoT {first_dot.name}', stdout_result)
            self.assertIn(f'DoT {second_dot.name}', stdout_result)
        finally:
            sys.stdout = sys.__stdout__

    def test_start_turn_update(self):
        """
        The start_turn_update function is called when the turn ends.
        It currently ony calls the _update_dots() function, since we handle dot ticks/procs at the start of the turn
        """
        output = StringIO()
        try:
            sys.stdout = output
            orig_health = self.dummy.health
            first_dot = DoT(name='first', damage_tick=Damage(5), duration=3, caster_lvl=2)
            second_dot = DoT(name='second', damage_tick=Damage(2), duration=5, caster_lvl=2)
            self.dummy.add_buff(first_dot)
            self.dummy.add_buff(second_dot)
            self.assertEqual(self.dummy.buffs, {first_dot: 3, second_dot: 5})

            self.dummy.start_turn_update()
            # should have reduced the durations
            self.assertEqual(self.dummy.buffs, {first_dot: 2, second_dot: 4})
            # should have subtracted health
            self.assertLess(self.dummy.health, orig_health)
            health_after_first_tick = self.dummy.health

            self.dummy.start_turn_update()
            self.dummy.start_turn_update()
            self.assertLess(self.dummy.health, health_after_first_tick)
            # should have removed the first dot
            self.assertEqual(self.dummy.buffs, {second_dot: 2})
            health_after_second_tick = self.dummy.health

            self.dummy.start_turn_update()
            self.dummy.start_turn_update()
            self.assertLess(self.dummy.health, health_after_second_tick)
            self.assertEqual(self.dummy.buffs, {})

            stdout_result = output.getvalue()
            self.assertIn('suffers', stdout_result)
            self.assertIn(f'DoT {first_dot.name}', stdout_result)
            self.assertIn(f'DoT {second_dot.name}', stdout_result)
        finally:
            sys.stdout = sys.__stdout__

    def test_remove_non_existant_buff(self):
        """
        Should thrown an error
        """
        expected_message = f"Cannot remove {self.dummy_buff.name} from {self.name} because he does not have it!"
        try:
            self.dummy.remove_buff(self.dummy_buff)
            self.fail('The test should have raised a NonExistantBuffError!')
        except NonExistantBuffError as e:
            received_message = e.args[0]
            self.assertEqual(received_message, expected_message)

    def test_apply_armor_reduction(self):
        """
        Test the _apply_armor_reduction, which reduces the damage given to it via
        a formula regarding the attacker's level and the character's armor points
        It only reduces physical damage
        """
        attacker_level = self.dummy.level
        armor = 500
        self.dummy.attributes['armor'] = armor

        # the formula
        reduction_percentage = armor / (armor + 400 + 85 * attacker_level)

        phys_dmg, magic_dmg = 500, 500
        damage = Damage(phys_dmg=phys_dmg, magic_dmg=magic_dmg)
        expected_phys_dmg, expected_magic_dmg = phys_dmg - (reduction_percentage * phys_dmg), magic_dmg
        expected_damage = Damage(phys_dmg=expected_phys_dmg, magic_dmg=expected_magic_dmg)

        reduced_dmg: Damage = self.dummy._apply_armor_reduction(damage, attacker_level)
        self.assertEqual(reduced_dmg, expected_damage)

    def test_apply_armor_reduction_no_phys_dmg(self):
        attacker_level = self.dummy.level
        armor = 500
        self.dummy.attributes['armor'] = armor

        # the formula
        reduction_percentage = armor / (armor + 400 + 85 * attacker_level)

        phys_dmg, magic_dmg = 0, 500
        damage = Damage(phys_dmg=phys_dmg, magic_dmg=magic_dmg)
        expected_phys_dmg, expected_magic_dmg = phys_dmg - (reduction_percentage * phys_dmg), magic_dmg
        expected_damage = Damage(phys_dmg=expected_phys_dmg, magic_dmg=expected_magic_dmg)

        reduced_dmg: Damage = self.dummy._apply_armor_reduction(damage, attacker_level)
        self.assertEqual(reduced_dmg.phys_dmg, 0)
        self.assertEqual(reduced_dmg, expected_damage)

    def test_calculate_level_difference_damage(self):
        """
        Test the calculate_level_difference_damage, which gives 10% more damage for each level we have
        over the target, or takes 10% damage from us for each level the target has over us
        """
        """
        Since our level is one higher, we should have a 10% damage increase
        """
        target_level = self.dummy.level - 1
        damage = 100
        self.assertEqual(self.dummy._calculate_level_difference_damage(damage, target_level), damage + (damage*0.1))

        """
        Since our level is one smaller, we should have a 10% damage decrease
        """
        target_level = self.dummy.level + 1
        damage = 100
        self.assertEqual(self.dummy._calculate_level_difference_damage(damage, target_level), damage - (damage * 0.1))

    def test_calculate_level_difference_damage_inverse_set(self):
        """
        Test the function with the inverse flag set as true.
        The inverse flag calculates as if we're taking damage and is used
         specifically for DoT procs, since we do not have a reference to the caster from the DoT
        """
        """
        Since our level is one higher, there should be a 10% damage decrease
        """
        target_level = self.dummy.level - 1
        damage = 100
        self.assertEqual(self.dummy._calculate_level_difference_damage(damage, target_level, inverse=True), damage - (damage * 0.1))

        """
        Since our level is one smaller, there should be a 10% damage increase
        """
        target_level = self.dummy.level + 1
        damage = 100
        self.assertEqual(self.dummy._calculate_level_difference_damage(damage, target_level, inverse=True), damage + (damage * 0.1))

    def test_apply_damage_absorption(self):
        """
        The _apply_damage_absorption function subtracts from the received damage according to the
        absorption shield points the character has.
        It calls the damage.handle_absorption method of the Damage class, so further tests regarding
        absorption are in the tests for that class
        """
        orig_absorption_shield = 500
        self.dummy.absorption_shield = orig_absorption_shield
        phys_dmg, magic_dmg = 100, 100
        damage_to_deal = Damage(phys_dmg=100, magic_dmg=100)
        expected_damage = Damage(phys_dmg=0, magic_dmg=0)
        expected_damage.phys_absorbed = phys_dmg
        expected_damage.magic_absorbed = magic_dmg

        reduced_dmg = self.dummy._apply_damage_absorption(damage_to_deal)
        self.assertEqual(reduced_dmg, expected_damage)
        self.assertEqual(self.dummy.absorption_shield, orig_absorption_shield-phys_dmg-magic_dmg)

    def test_apply_damage_absorption_to_print_set(self):
        """
        The function takes a flag called to_print, which if set to True
         only returns the resulting Damage object without modifying the LivingThing's absorption shield
        """
        orig_absorption_shield = 500
        self.dummy.absorption_shield = orig_absorption_shield
        phys_dmg, magic_dmg = 100, 100
        damage_to_deal = Damage(phys_dmg=100, magic_dmg=100)
        expected_damage = Damage(phys_dmg=0, magic_dmg=0)
        expected_damage.phys_absorbed = phys_dmg
        expected_damage.magic_absorbed = magic_dmg

        reduced_dmg = self.dummy._apply_damage_absorption(damage_to_deal, to_print=True)
        self.assertEqual(reduced_dmg, expected_damage)
        self.assertEqual(self.dummy.absorption_shield, orig_absorption_shield)


class FriendlyNpcTests(unittest.TestCase):
    def setUp(self):
        self.gossip = 'Hey guyss, ayy $N'
        self.min_damage, self.max_damage = 5, 5
        self.health, self.mana = 100, 100
        self.name, self.level = 'Rado', 7
        # The FriendlyNpc keeps a colored str object in it
        self.expected_colored_name = termcolor.colored(self.name, 'green')
        self.dummy = FriendlyNPC(name=self.name, health=self.health, mana=self.mana, level=self.level, min_damage=self.min_damage, max_damage=self.max_damage,
                                 quest_relation_id=0, loot_table=None, gossip=self.gossip)

    def test_init(self):
        self.assertEqual(self.dummy.level, self.level)
        self.assertEqual(self.dummy.min_damage, self.min_damage)
        self.assertEqual(self.dummy.max_damage, self.max_damage)
        self.assertEqual(self.dummy.gossip, self.gossip)
        self.assertEqual(self.dummy.colored_name, self.expected_colored_name)

    def test_str(self):
        """
        Should return the name of the FriendlyNPC
        """
        expected_str = str(self.expected_colored_name)
        self.assertEqual(str(self.dummy), expected_str)

    def test_talk(self):
        """
        The talk method should print out the gossip of the npc along with a NPC_NAME says: pre-text
        There is a special symbol - $N, which should be replaced with the player name given in the method
        """
        output = StringIO()
        p_name = 'Mello'
        expected_message = f'{self.expected_colored_name} says: {self.gossip.replace("$N", p_name)}'
        try:
            sys.stdout = output
            self.dummy.talk(player_name=p_name)
            result = output.getvalue()
            self.assertIn(expected_message, result)
        finally:
            sys.stdout = sys.__stdout__


class VendorNpcTests(unittest.TestCase):
    def setUp(self):
        name, self.entry, health, mana = 'Jack', 1, 100, 100
        level, min_damage, max_damage, quest_relation_id = 3, 2, 6, 0
        loot_table, gossip = None, 'Like a genesisis, $N!'
        self.first_item = Item(name='game', item_id=5, buy_price=5, sell_price=5, quest_id=0)
        self.first_item_stock = 10
        self.second_item = Item(name='copy-cat', item_id=2, buy_price=1, sell_price=1, quest_id=1)
        self.second_item_stock = 1
        self.third_item = Item(name='Domev_se_vrushta', item_id=4, buy_price=2, sell_price=2, quest_id=2)
        self.third_item_stock = 2
        self.expected_colored_name = termcolor.colored(name, color='green')
        self.inventory = {self.first_item.name: (self.first_item, self.first_item_stock),
                          self.second_item.name: (self.second_item, self.second_item_stock),
                          self.third_item.name: (self.third_item, self.third_item_stock)}
        self.dummy = VendorNPC(name=name, entry=self.entry, health=health, mana=mana, level=level, min_damage=min_damage,
                               max_damage=max_damage, quest_relation_id=quest_relation_id, loot_table=loot_table,
                               gossip=gossip, inventory=self.inventory)

    def test_init(self):
        self.assertEqual(self.dummy.inventory, self.inventory)
        self.assertEqual(self.dummy.entry, self.entry)

    def test_str(self):
        """ The __str__ dunder method should return the colored name with a <Vendor> added to it"""
        expected_str = f'{self.expected_colored_name} <Vendor>'
        self.assertEqual(expected_str, str(self.dummy))

    def test_has_item(self):
        """
        has_item returns a boolean if the vendor has the item in his inventory
        """
        valid_item = self.first_item.name
        invalid_item = 'ThreeOnEYeah'
        self.assertTrue(self.dummy.has_item(valid_item))
        self.assertFalse(self.dummy.has_item(invalid_item))

    def test_get_item_info_valid_item(self):
        """
        This get_item_info function is only used for printing purposes
        it returns the item we want from the vendor.
        It is used when the Character queries to see the item
        """
        valid_item_name = self.first_item.name
        received_item: Item = self.dummy.get_item_info(valid_item_name)
        self.assertEqual(received_item, self.first_item)

    def test_get_item_info_invalid_item(self):
        output = StringIO()
        invalid_item_name = 'logic'
        expected_message = f'{self.dummy.name} does not have {invalid_item_name} for sale.'
        try:
            sys.stdout = output
            received_item = self.dummy.get_item_info(invalid_item_name)
            self.assertIsNone(received_item)
            self.assertIn(expected_message, output.getvalue())
        finally:
            sys.stdout = sys.__stdout__

    def test_get_item_price(self):
        """
        the get_item_price function returns the price for the specific item
        """
        received_price = self.dummy.get_item_price(self.first_item.name)
        self.assertEqual(self.first_item.buy_price, received_price)

    def test_get_item_price_invalid_item(self):
        output = StringIO()
        invalid_item_name = 'logic'
        expected_message = f'{self.dummy.name} does not have {invalid_item_name} for sale.'
        try:
            sys.stdout = output
            received_item = self.dummy.get_item_price(invalid_item_name)
            self.assertIsNone(received_item)
            self.assertIn(expected_message, output.getvalue())
        finally:
            sys.stdout = sys.__stdout__

    def test_sell_item(self):
        """ The sell_item function returns the item object, the count of items fro sale and the price for the items"""
        item_sale_info: (Item, int, int) = self.dummy.sell_item(self.first_item.name)
        self.assertTrue(isinstance(item_sale_info[0], Item))
        self.assertEqual(item_sale_info[0], self.first_item)
        self.assertEqual(item_sale_info[1], self.first_item_stock)
        self.assertEqual(item_sale_info[2], self.first_item.buy_price)
        # assert that the item has been sold
        self.assertNotIn(self.first_item.name, self.dummy.inventory)

    def test_sell_item_invalid_item(self):
        output = StringIO()
        invalid_item_name = 'logic'
        expected_message = f'{self.dummy.name} does not have {invalid_item_name} for sale.'
        try:
            sys.stdout = output
            received_item = self.dummy.sell_item(invalid_item_name)
            self.assertIsNone(received_item)
            self.assertIn(expected_message, output.getvalue())
        finally:
            sys.stdout = sys.__stdout__


class MonsterTests(unittest.TestCase):
    def setUp(self):
        self.monster_id = 1
        self.name, self.health, self.mana, self.level = 'Monstru', 100, 100, 4
        self.min_damage, self.max_damage, self.quest_relation_id = 3, 6, 0
        self.xp_to_give, self.gold_to_give_range = 250, (50, 100)
        self.armor, self.gossip, self.respawnable = 100, 'Grr, I kill you!', True
        self.dropped_item_mock = Mock(name='something')
        self.dropped_item_mock2 = Mock(name='smth')
        loot_to_drop = [self.dropped_item_mock, self.dropped_item_mock2]
        self.loot_table = Mock(decide_drops=lambda: loot_to_drop)
        self.dummy = Monster(monster_id=self.monster_id, name=self.name, health=self.health, mana=self.mana,
                             level=self.level, min_damage=self.min_damage, max_damage=self.max_damage,
                             quest_relation_id=self.quest_relation_id, xp_to_give=self.xp_to_give,
                             gold_to_give_range=self.gold_to_give_range, loot_table=self.loot_table,
                             armor=self.armor, gossip=self.gossip, respawnable=self.respawnable)

    def test_init(self):
        self.assertEqual(self.dummy.monster_id, self.monster_id)
        self.assertEqual(self.dummy.level, self.level)
        self.assertEqual(self.dummy.min_damage, self.min_damage)
        self.assertEqual(self.dummy.max_damage, self.max_damage)
        self.assertEqual(self.dummy.xp_to_give, self.xp_to_give)
        self.assertEqual(self.dummy.attributes, {'armor': self.armor})
        self.assertEqual(self.dummy.gossip, self.gossip)
        self.assertEqual(self.dummy.respawnable, self.respawnable)
        # gold to give must be between range
        self.assertTrue(self.gold_to_give_range[0] <= self.dummy._gold_to_give <= self.gold_to_give_range[1])
        self.assertEqual(self.dummy.quest_relation_id, self.quest_relation_id)
        self.assertEqual(self.dummy.loot_table, self.loot_table)
        self.assertEqual(self.dummy.loot, {'gold': self.dummy._gold_to_give})

    def test_str(self):
        """
        The str method should return all sorts of information regarding the creature
        """
        colored_monster_name = termcolor.colored(self.name, color='red')
        expected_str = f'Creature Level {self.level} {colored_monster_name} - {self.dummy.health}/{self.health} HP | {self.dummy.mana}/{self.mana} Mana | {self.min_damage}-{self.max_damage} Damage'

        self.assertEqual(str(self.dummy), expected_str)

    def test_get_auto_attack_damage(self):
        """
        The get_auto_attack_damage should return a basic attack damage from the Monster class
        it chooses a random integer between the min/max damage and
        """
        target_level = self.dummy.level  # so the level doesn't affect the damage
        result: Damage = self.dummy.get_auto_attack_damage(target_level)

        self.assertTrue(isinstance(result, Damage))
        self.assertTrue(self.min_damage <= result.phys_dmg <= self.max_damage)

    def test_attack(self):
        """
        The attack function deals damage to the monster while applying armor reduction and absorption
        It calls the victim's take_attack function with the damage dealt
        """
        output = StringIO()
        victim_level = self.dummy.level
        # Modify the take_attack function to print the damage it took so we can assert it takes the appropriate damage
        victim_mock = Mock(take_attack=lambda *args: print(args[1].phys_dmg), level=victim_level)
        expected_damage = self.dummy.get_auto_attack_damage(victim_level)
        try:
            sys.stdout = output
            self.dummy.attack(victim_mock)
            # the damage should be different, since it's always random
            std_output = output.getvalue()
            self.assertNotIn(str(expected_damage.phys_dmg), std_output)
            dealt_dmg: float = float(std_output)
            self.assertTrue(self.min_damage <= dealt_dmg <= self.max_damage)
        finally:
            sys.stdout = sys.__stdout__

    def test_take_attack(self):
        """
        The take_attack function deals the damage given to it to the Monster after applying
        armor reduction and absorption
        """
        dmg_to_take = Damage(magic_dmg=10)  # magic so we don't get reduction by the armor
        attacker_level = self.dummy.level
        self.dummy.take_attack(dmg_to_take, attacker_level)
        self.assertEqual(self.dummy.health, self.health-dmg_to_take.magic_dmg)

    def test_take_attack_armor_reduction(self):
        """
        Test if the take_attack function actually applies armor reduction
        """
        armor = 500
        self.dummy.attributes['armor'] = armor
        dmg_to_take = Damage(phys_dmg=10)
        attacker_level = self.dummy.level

        # get the expected damage after reduction
        reduction_percentage = armor / (armor + 400 + 85 * attacker_level)
        damage_to_deduct = dmg_to_take.phys_dmg * reduction_percentage
        reduced_damage = dmg_to_take.phys_dmg - damage_to_deduct

        self.dummy.take_attack(dmg_to_take, attacker_level)

        self.assertEqual(self.dummy.health, int(self.health - reduced_damage))

    def test_take_attack_absorption(self):
        """
        Test the take_attack function when the monster has an absorption shield
        """
        magic_dmg, absorption_shield = 11, 10
        self.dummy.absorption_shield = absorption_shield
        dmg_to_take = Damage(magic_dmg=magic_dmg)
        attacker_level = self.dummy.level

        self.dummy.take_attack(dmg_to_take, attacker_level)
        expected_health = self.health - (dmg_to_take.magic_dmg - absorption_shield)
        self.assertEqual(self.dummy.health, expected_health)

    def test_take_attack_absorption_and_armor(self):
        """ Test the function, this time accouting for armor and absorption """
        orig_health = self.dummy.health
        absorption_shield = 16
        armor = 500
        self.dummy.absorption_shield = absorption_shield
        self.dummy.attributes['armor'] = armor
        attacker_level = self.dummy.level

        dmg_to_take = Damage(phys_dmg=15, magic_dmg=15)

        # get the expected damage after armor reduction
        reduction_percentage = armor / (armor + 400 + 85 * attacker_level)
        damage_to_deduct = dmg_to_take.phys_dmg * reduction_percentage
        reduced_damage = dmg_to_take.phys_dmg - damage_to_deduct

        # NOTE: Magical damage always gets absorbed first
        leftover_shield = absorption_shield - dmg_to_take.magic_dmg
        expected_dmg = reduced_damage - leftover_shield

        # ACT
        self.dummy.take_attack(dmg_to_take, attacker_level)

        self.assertEqual(self.dummy.health, round(orig_health-expected_dmg, 1))

    def test_get_take_attack_damage_repr(self):
        """
        The get_take_attack_damage_repr returns a Damage object only to for printing purposes.
        It does not lower the monster's  health in any way.
        """
        orig_health = self.dummy.health
        armor = self.armor
        phys_dmg, magic_dmg = 15, 20
        dmg_to_take = Damage(phys_dmg, magic_dmg)
        attacker_level = self.dummy.level

        # get the expected damage after reduction
        reduction_percentage = armor / (armor + 400 + 85 * attacker_level)
        damage_to_deduct = dmg_to_take.phys_dmg * reduction_percentage
        reduced_damage = dmg_to_take.phys_dmg - damage_to_deduct

        result: Damage = self.dummy.get_take_attack_damage_repr(dmg_to_take, attacker_level)
        expected_result = Damage(phys_dmg=reduced_damage, magic_dmg=magic_dmg)

        self.assertTrue(isinstance(result, Damage))
        self.assertEqual(self.dummy.health, orig_health)
        self.assertEqual(result, expected_result)

    def test_drop_loot(self):
        expected_loot = {self.dropped_item_mock.name: self.dropped_item_mock,
                         self.dropped_item_mock2.name: self.dropped_item_mock2}
        default_loot = {'gold': self.dummy._gold_to_give}
        expected_loot.update(default_loot)

        self.assertEqual(self.dummy.loot, default_loot)
        self.dummy._drop_loot()
        self.assertEqual(self.dummy.loot, expected_loot)

    def test_drop_loot_empty_loot_table(self):
        """ It should return None when there is no loot table"""
        self.dummy.loot_table = None
        self.assertIsNone(self.dummy._drop_loot())

    def test_give_loot(self):
        """
        The give_loot function is called whenever the character loots something from the monster.
        It checks if the item is in the loot and if it is, removes it and returns it
        """
        # fill the loot dict
        self.dummy._drop_loot()

        received_item = self.dummy.give_loot(self.dropped_item_mock.name)

        self.assertTrue(isinstance(received_item, type(self.dropped_item_mock)))
        self.assertEqual(received_item, self.dropped_item_mock)
        self.assertTrue(self.dropped_item_mock.name not in self.dummy.loot)

    def test_give_loot_nonexisting_item(self):
        output = StringIO()
        expected_print = f'{self.dummy.name} did not drop {self.dropped_item_mock.name}.'
        # fill the loot dict
        self.dummy._drop_loot()
        # get the item once
        received_item = self.dummy.give_loot(self.dropped_item_mock.name)

        # try to get it again
        try:
            sys.stdout = output
            self.dummy.give_loot(self.dropped_item_mock.name)
            self.assertIn(expected_print, output.getvalue())
        finally:
            sys.stdout = sys.__stdout__

    def test_die(self):
        """ the _die function calls the super()_die() function and _drop_loot to fill the loot dict"""
        output = StringIO()
        expected_print = f'Creature {self.dummy.name} has died!'

        try:
            sys.stdout = output

            self.dummy._die()

            self.assertFalse(self.dummy.is_alive())
            self.assertNotEqual(self.dummy.loot, {})
            self.assertEqual(len(self.dummy.loot.keys()), 3)
            self.assertIn(expected_print, output.getvalue())
        finally:
            sys.stdout = sys.__stdout__

    def test_calculate_gold_reward(self):
        """
        The calculate_gold_reward returns a random integer between the gold_to_give_range
        """
        min_g, max_g = 50, 100
        received_gold = self.dummy._calculate_gold_reward((min_g, max_g))

        self.assertTrue(min_g <= received_gold <= max_g)

        # assert that the return value is random and fairly spread out
        multiple_gold_rewards = [self.dummy._calculate_gold_reward((min_g, max_g)) for _ in range(100)]
        count = Counter(multiple_gold_rewards)
        most_common_num, count = count.most_common()[0]

        self.assertTrue(count < len(multiple_gold_rewards) // 3)

    def test_yell_gossip(self):
        """
        The monster should say/yell/ask his gossip according to what it ends with.
        """
        expected_message = f'{self.dummy.name} yells: {self.dummy.gossip}'
        output = StringIO()
        try:
            sys.stdout = output
            self.dummy.say_gossip()
            self.assertIn(expected_message, output.getvalue())
        finally:
            sys.stdout = sys.__stdout__

    def test_say_gossip(self):
        """
        The monster should 'say' his gossip since it does not end in an exclamation/question mark
        """
        self.dummy.gossip = "And I'm like hello"
        expected_message = f'{self.dummy.name} says: {self.dummy.gossip}'
        output = StringIO()
        try:
            sys.stdout = output
            self.dummy.say_gossip()
            self.assertIn(expected_message, output.getvalue())
        finally:
            sys.stdout = sys.__stdout__

    def test_ask_gossip(self):
        """
        The monster should 'ask' his gossip since it ends in an question mark
        """
        self.dummy.gossip = "And I'm like hello?"
        expected_message = f'{self.dummy.name} asks: {self.dummy.gossip}'
        output = StringIO()
        try:
            sys.stdout = output
            self.dummy.say_gossip()
            self.assertIn(expected_message, output.getvalue())
        finally:
            sys.stdout = sys.__stdout__


class CharacterTests(unittest.TestCase):
    def setUp(self):
        self.name, self.health, self.mana, self.strength = 'Neth', 100, 100, 10
        self.agility, self.loaded_scripts, self.killed_monsters = 5, set(), set()
        self.completed_quests, self.saved_inventory, self.saved_equipment = set(), {'gold': 0}, deepcopy(CHARACTER_DEFAULT_EQUIPMENT)
        self.dummy = Character(name=self.name, health=self.health, mana=self.mana, strength=self.strength,
                               agility=self.agility, loaded_scripts=self.loaded_scripts, killed_monsters=self.killed_monsters,
                               completed_quests=self.completed_quests, saved_equipment=self.saved_equipment,
                               saved_inventory=self.saved_inventory)

    def test_init(self):
        # The damage should be modified since the character is level 1 and has some strength/agi
        level_one_bonus_stats = CHARACTER_LEVELUP_BONUS_STATS[1]
        expected_agility = level_one_bonus_stats['agility']   # agility modified armor/strength
        expected_strength = level_one_bonus_stats['strength'] + (expected_agility * 0.5)
        expected_armor = level_one_bonus_stats['armor'] + (expected_agility * 2.5)
        expected_attributes = {
            'bonus_health': 0,
            'bonus_mana': 0,
            'agility': expected_agility,
            'armor': expected_armor,
            'strength': expected_strength
        }
        self.assertNotEqual(self.dummy.min_damage, 0)
        self.assertNotEqual(self.dummy.max_health, 1)
        self.assertEqual(self.dummy.level, 1)
        self.assertEqual(self.dummy.attributes, expected_attributes)
        self.assertEqual(self.dummy.current_zone, CHAR_STARTER_ZONE)
        self.assertEqual(self.dummy.current_subzone, CHAR_STARTER_SUBZONE)

    def test_equip_item(self):
        """
        The equip item takes na item from our inventory and adds it to our equipment, swapping with the
        already equipped item essentially
        """
        original_health = self.dummy.health
        self.item_to_equip = Equipment(name='FirstHead', item_id=1, slot='headpiece',
                                       attributes=create_attributes_dict(bonus_health=1000), buy_price=1)
        self.dummy.inventory = {
            self.item_to_equip.name: (self.item_to_equip, 1)
        }

        # act

        # Equip the  item
        self.dummy.equip_item(item=self.item_to_equip)
        # assert that the bonus health has been added
        self.assertNotEqual(self.dummy.health, original_health)
        self.assertTrue(self.dummy.health - original_health >= 1000)
        # assert that the item is not in the inventory anymore
        self.assertTrue(self.item_to_equip.name not in self.dummy.inventory)

        # assert that its in the equipment
        self.assertEqual(self.dummy.equipment['headpiece'], self.item_to_equip)

    def test_equip_dequip_item(self):
        """
        Test that everything works as expected when equipping an item over another
        """
        original_health = self.dummy.health
        self.gear = Equipment(name='FirstHead', item_id=1, slot='headpiece',
                              attributes=create_attributes_dict(bonus_health=1000), buy_price=1)
        self.item_to_eq = Equipment(name='SecondHead', item_id=1, slot='headpiece',
                                    attributes=create_attributes_dict(), buy_price=1)
        self.dummy.inventory = {
            self.gear.name: (self.gear, 1),
            self.item_to_eq.name: (self.item_to_eq, 1)
        }

        # act

        # Equip the first item
        self.dummy.equip_item(item=self.gear)
        self.assertNotEqual(self.dummy.health, original_health)
        self.assertTrue(self.dummy.health - original_health >= 1000)
        self.assertTrue(self.gear.name not in self.dummy.inventory)
        self.assertEqual(self.dummy.equipment['headpiece'], self.gear)

        # Equip the second item
        self.dummy.equip_item(item=self.item_to_eq)
        # health should be subtracted
        self.assertEqual(self.dummy.health, original_health)
        self.assertTrue(self.item_to_eq.name not in self.dummy.inventory)
        self.assertEqual(self.dummy.equipment['headpiece'], self.item_to_eq)
        # assert that the old item is in the inventory
        self.assertTrue(self.gear.name in self.dummy.inventory)
        self.assertEqual(self.dummy.inventory[self.gear.name], (self.gear, 1))

    def test_equip_item_weapon(self):
        original_health = self.dummy.health
        orig_min_dmg, orig_max_dmg = self.dummy.min_damage, self.dummy.max_damage
        self.wep_to_eq = Weapon(name='wep', item_id=1, min_damage=10, max_damage=20, attributes=create_attributes_dict(
            bonus_health=1000, strength=1000
        ))
        self.dummy.inventory = {
            self.wep_to_eq.name: (self.wep_to_eq, 1)
        }
        equipped_weapon = self.dummy.equipped_weapon
        self.assertTrue(equipped_weapon.name not in self.dummy.inventory)

        self.assertNotEqual(self.dummy.equipped_weapon, self.wep_to_eq)

        self.dummy.equip_item(self.wep_to_eq)

        #  assert that the item is equipped and the old item is in the inventory
        self.assertEqual(self.dummy.equipped_weapon, self.wep_to_eq)
        self.assertGreater(self.dummy.health, original_health)
        self.assertTrue(equipped_weapon.name in self.dummy.inventory)
        self.assertEqual(self.dummy.inventory[equipped_weapon.name], (equipped_weapon, 1))
        # assert that the damage has been modified
        self.assertGreater(self.dummy.min_damage, orig_min_dmg)
        self.assertGreater(self.dummy.max_damage, orig_max_dmg)

    def test_equip_item_non_equippable_item(self):
        self.item_to_eq = Item(name='Evangelism', item_id=1, buy_price=1, sell_price=1)
        orig_health, orig_mana, orig_agi, orig_stren = self.dummy.health, self.dummy.mana, self.dummy.attributes['agility'], self.dummy.attributes['strength']
        self.dummy.inventory = {
            self.item_to_eq.name: (self.item_to_eq, 1)
        }

        self.dummy.equip_item(self.item_to_eq)

        # assert that nothing has happened
        self.assertEqual(self.dummy.health, orig_health)
        self.assertEqual(self.dummy.mana, orig_mana)
        self.assertEqual(self.dummy.attributes['agility'], orig_agi)
        self.assertEqual(self.dummy.attributes['strength'], orig_stren)
        # assert that the item has not moved
        self.assertTrue(self.item_to_eq.name in self.dummy.inventory)
        self.assertEqual(self.dummy.inventory[self.item_to_eq.name], (self.item_to_eq, 1))

    def test_equip_item_non_equippable_multiple_times(self):
        """
        Due to a previous bug, equipping an item multiple times would increase the character's armor/strength
            up to infinity, due to the way the calculate_stats function worked.
        Assert that the stats do not change
        """
        self.item_to_eq = Item(name='Evangelism', item_id=1, buy_price=1, sell_price=1)
        orig_health, orig_mana, orig_agi, orig_stren = self.dummy.health, self.dummy.mana, self.dummy.attributes[
            'agility'], self.dummy.attributes['strength']
        self.dummy.inventory = {
            self.item_to_eq.name: (self.item_to_eq, 1)
        }

        for _ in range(10000):
            self.dummy.equip_item(self.item_to_eq)

        # assert that nothing has happened
        self.assertEqual(self.dummy.health, orig_health)
        self.assertEqual(self.dummy.mana, orig_mana)
        self.assertEqual(self.dummy.attributes['agility'], orig_agi)
        self.assertEqual(self.dummy.attributes['strength'], orig_stren)
        # assert that the item has not moved
        self.assertTrue(self.item_to_eq.name in self.dummy.inventory)
        self.assertEqual(self.dummy.inventory[self.item_to_eq.name], (self.item_to_eq, 1))

    def test_consume_item(self):
        """
        The consume_item function consumes the given potion from the inventory, adding a buff to the
        player and removing the potion from the inventory
        :return:
        """
        orig_strength = self.dummy.attributes['strength']
        self.item_entry = 4
        self.name = 'Strength Potion'
        self.buy_price = 1
        self.sell_price = 1
        self.effect_id = 1
        self.effect: BeneficialBuff = BeneficialBuff(name="Heart of a Lion",
                                                     buff_stats_and_amounts=[('strength', 15)],
                                                     duration=5)
        self.potion = Potion(name=self.name, item_id=self.item_entry, buy_price=self.buy_price,
                             sell_price=self.sell_price,
                             buff=self.effect, quest_id=0)

        self.dummy.inventory = {
            self.potion.name: (self.potion, 1)
        }

        self.dummy.consume_item(self.potion)

        current_strength = self.dummy.attributes['strength']
        self.assertGreater(current_strength, orig_strength)

        self.assertTrue(self.potion.name not in self.dummy.inventory)

    def test_consume_item_non_consumable_item(self):
        self.item_to_eq = Item(name='Evangelism', item_id=1, buy_price=1, sell_price=1)
        self.dummy.inventory = {
            self.item_to_eq.name: (self.item_to_eq, 1)
        }
        self.dummy.consume_item(self.item_to_eq)
        self.assertTrue(self.item_to_eq.name in self.dummy.inventory)

    def test_equip_weapon(self):
        """
        The _equip_weapon function directly equips the weapon and adds the attributes to the player
        """
        output = StringIO()
        original_health = self.dummy.health
        orig_min_dmg, orig_max_dmg = self.dummy.min_damage, self.dummy.max_damage
        self.wep_to_eq = Weapon(name='wep', item_id=1, min_damage=10, max_damage=20, attributes=create_attributes_dict(
            bonus_health=1000, strength=1000
        ))
        expected_message = f'{self.dummy.name} has equipped Weapon {self.wep_to_eq.name}'
        try:
            sys.stdout = output

            self.dummy._equip_weapon(self.wep_to_eq)

            #  assert that the item is equipped
            self.assertEqual(self.dummy.equipped_weapon, self.wep_to_eq)
            self.assertGreater(self.dummy.health, original_health)
            # assert that the damage has been modified
            self.assertGreater(self.dummy.min_damage, orig_min_dmg)
            self.assertGreater(self.dummy.max_damage, orig_max_dmg)
            self.assertIn(expected_message, output.getvalue())
        finally:
            sys.stdout = sys.__stdout__

    def test_equip_gear(self):
        """
        The _equip_gear function takes an Equipment object and 'equips' on the character.
        It does not take care of the old one and is simply there  to print, add the item and add the attributes it gives
        """
        output = StringIO()
        orig_health = self.dummy.health
        self.gear = Equipment(name='FirstHead', item_id=1, slot='headpiece',
                              attributes=create_attributes_dict(bonus_health=1000), buy_price=1)
        expected_message = f'{self.dummy.name} has equipped {self.gear.slot} {self.gear.name}'
        try:
            sys.stdout = output

            self.dummy._equip_gear(self.gear)

            self.assertNotEqual(self.dummy.health, orig_health)
            self.assertTrue(self.dummy.health - orig_health >= 1000)
            self.assertEqual(self.dummy.equipment['headpiece'], self.gear)
            self.assertIn(expected_message, output.getvalue())
        finally:
            sys.stdout = sys.__stdout__

    def test_add_item_to_inventory_new_item(self):
        """
        The add_item_to_inventory function adds a given item to the inventory
        """
        item_mock = Mock(name='someItemBitch')
        self.assertNotIn(item_mock.name, self.dummy.inventory)

        for i in range(100):
            self.dummy.add_item_to_inventory(item_mock)

            self.assertIn(item_mock.name, self.dummy.inventory)
            self.assertEqual(self.dummy.inventory[item_mock.name], (item_mock, i+1))

    def test_add_item_to_inventory_multiple_items(self):
        item_mock = Mock(name='someItemBitch')
        self.assertNotIn(item_mock.name, self.dummy.inventory)

        self.dummy.add_item_to_inventory(item_mock, 200)

        self.assertIn(item_mock.name, self.dummy.inventory)
        self.assertEqual(self.dummy.inventory[item_mock.name], (item_mock, 200))

    def test_add_attributes(self):
        """
        The add_attributes function simply takes a dictionary of expected attributes and adds them
        to the character's
        """
        # subtract the strength/armor because we will recalculate the added values from the agility
        orig_health, orig_mana, orig_stren = self.dummy.health, self.dummy.mana, self.dummy.attributes['strength'] - self.dummy._bonus_strength
        orig_agi, orig_armor = self.dummy.attributes['agility'], self.dummy.attributes['armor'] - self.dummy._bonus_armor

        added_agi, added_health, added_mana = 1000, 1000, 1000
        expected_agility = orig_agi + added_agi
        expected_strength = orig_stren + (expected_agility * 0.5)
        expected_armor = orig_armor + (expected_agility * 2.5)
        expected_health = orig_health + added_health
        expected_mana = orig_mana + added_mana
        expected_min_dmg = self.dummy.equipped_weapon.min_damage + (0.4 * expected_strength)
        expected_max_dmg = self.dummy.equipped_weapon.max_damage + (0.4 * expected_strength)

        attributes_to_add = create_attributes_dict(bonus_health=added_health, bonus_mana=added_mana, strength=0, agility=added_agi, armor=0)

        # Act
        self.dummy._add_attributes(attributes_to_add)

        self.assertEqual(self.dummy.attributes['strength'], expected_strength)
        self.assertEqual(self.dummy.attributes['agility'], expected_agility)
        self.assertEqual(self.dummy.attributes['armor'], expected_armor)
        self.assertEqual(self.dummy.health, expected_health)
        self.assertEqual(self.dummy.mana, expected_mana)
        self.assertEqual(self.dummy.min_damage, expected_min_dmg)
        self.assertEqual(self.dummy.max_damage, expected_max_dmg)

    def test_add_attributes_empty_attributes(self):
        """
        Nothing should change
        """
        orig_health, orig_mana, orig_stren = self.dummy.health, self.dummy.mana, self.dummy.attributes['strength']
        orig_agi, orig_armor = self.dummy.attributes['agility'], self.dummy.attributes['armor']
        orig_min_damage, orig_max_damage = self.dummy.min_damage, self.dummy.max_damage

        attributes_to_add = create_attributes_dict()  # is empty

        self.dummy._add_attributes(attributes_to_add)

        self.assertEqual(self.dummy.attributes['strength'], orig_stren)
        self.assertEqual(self.dummy.attributes['agility'], orig_agi)
        self.assertEqual(self.dummy.attributes['armor'], orig_armor)
        self.assertEqual(self.dummy.health, orig_health)
        self.assertEqual(self.dummy.mana, orig_mana)
        self.assertEqual(self.dummy.min_damage, orig_min_damage)
        self.assertEqual(self.dummy.max_damage, orig_max_damage)

    def test_subtract_attributes(self):
        """
        The add_attributes function simply takes a dictionary of attributes and subtract them
        from the character's. It trusts that after subtracting no attributes will be negative
        """
        # subtract the strength/armor because we will recalculate the added values from the agility
        orig_health, orig_mana, orig_stren = self.dummy.health, self.dummy.mana, self.dummy.attributes[
            'strength'] - self.dummy._bonus_strength
        orig_agi, orig_armor = self.dummy.attributes['agility'], self.dummy.attributes['armor'] - self.dummy._bonus_armor

        subtracted_agi, subtracted_health, subtracted_mana = 1, 1, 1
        expected_agility = orig_agi - subtracted_agi
        expected_strength = orig_stren + (expected_agility * 0.5)
        expected_armor = orig_armor + (expected_agility * 2.5)
        expected_health = orig_health - subtracted_health
        expected_mana = orig_mana - subtracted_mana
        expected_min_dmg = self.dummy.equipped_weapon.min_damage + (0.4 * expected_strength)
        expected_max_dmg = self.dummy.equipped_weapon.max_damage + (0.4 * expected_strength)

        attributes_to_add = create_attributes_dict(bonus_health=subtracted_health, bonus_mana=subtracted_mana, strength=0,
                                                   agility=subtracted_agi, armor=0)

        # Act
        self.dummy._subtract_attributes(attributes_to_add)

        self.assertEqual(self.dummy.attributes['strength'], expected_strength)
        self.assertEqual(self.dummy.attributes['agility'], expected_agility)
        self.assertEqual(self.dummy.attributes['armor'], expected_armor)
        self.assertEqual(self.dummy.health, expected_health)
        self.assertEqual(self.dummy.mana, expected_mana)
        self.assertEqual(self.dummy.min_damage, expected_min_dmg)
        self.assertEqual(self.dummy.max_damage, expected_max_dmg)

    def test_subtract_attributes_empty_attributes(self):
        # subtract the strength/armor because we will recalculate the added values from the agility
        orig_health, orig_mana, orig_stren = self.dummy.health, self.dummy.mana, self.dummy.attributes[
            'strength'] - self.dummy._bonus_strength
        orig_agi, orig_armor = self.dummy.attributes['agility'], self.dummy.attributes['armor'] - self.dummy._bonus_armor
        orig_min_damage, orig_max_damage = self.dummy.min_damage, self.dummy.max_damage

        subtracted_agi, subtracted_health, subtracted_mana = 0, 0, 0
        expected_agility = orig_agi - subtracted_agi
        expected_strength = orig_stren + (expected_agility * 0.5)
        expected_armor = orig_armor + (expected_agility * 2.5)
        expected_health = orig_health - subtracted_health
        expected_mana = orig_mana - subtracted_mana

        attributes_to_add = create_attributes_dict(bonus_health=0, bonus_mana=0,
                                                   strength=0,
                                                   agility=0, armor=0)

        # Act
        self.dummy._subtract_attributes(attributes_to_add)

        self.assertEqual(self.dummy.attributes['strength'], expected_strength)
        self.assertEqual(self.dummy.attributes['agility'], expected_agility)
        self.assertEqual(self.dummy.attributes['armor'], expected_armor)
        self.assertEqual(self.dummy.health, expected_health)
        self.assertEqual(self.dummy.mana, expected_mana)
        self.assertEqual(self.dummy.min_damage, orig_min_damage)
        self.assertEqual(self.dummy.max_damage, orig_max_damage)

    def test_calculate_stats_formulas(self):
        """
        Apart from the horrendous name, this function simply recalculates all our stats after they have allegedly been changed.

        """
        orig_health, orig_mana, orig_stren = self.dummy.health, self.dummy.mana, self.dummy.attributes['strength']
        orig_agi, orig_armor = self.dummy.attributes['agility'], self.dummy.attributes['armor']
        orig_min_damage, orig_max_damage = self.dummy.min_damage, self.dummy.max_damage

        # since we've done nothing, calling the method should not change anything
        for _ in range(50):
            self.dummy._calculate_stats_formulas()

        self.assertEqual(self.dummy.attributes['strength'], orig_stren)
        self.assertEqual(self.dummy.attributes['agility'], orig_agi)
        self.assertEqual(self.dummy.attributes['armor'], orig_armor)
        self.assertEqual(self.dummy.health, orig_health)
        self.assertEqual(self.dummy.mana, orig_mana)
        self.assertEqual(self.dummy.min_damage, orig_min_damage)
        self.assertEqual(self.dummy.max_damage, orig_max_damage)

    def test_calculate_stats_formulas_in_combat(self):
        """ Adding more health in combat should increase the char's max health but not affect his current health"""
        self.dummy.enter_combat()
        orig_current_health, orig_max_health = self.dummy.health, self.dummy.max_health
        orig_current_mana, orig_max_mana = self.dummy.mana, self.dummy.max_mana

        mana_increase, health_increase = 100, 100
        expected_max_health, expected_max_mana = orig_max_health + health_increase, orig_max_mana + mana_increase
        expected_current_health, expected_current_mana = orig_current_health, orig_current_mana

        # increase the health/mana from the attributes
        self.dummy.attributes['bonus_health'] += health_increase
        self.dummy.attributes['bonus_mana'] += mana_increase
        self.dummy._calculate_stats_formulas()

        self.assertEqual(self.dummy.health, expected_current_health)
        self.assertEqual(self.dummy.mana, expected_current_mana)

        self.assertEqual(self.dummy.max_health, expected_max_health)
        self.assertEqual(self.dummy.max_mana, expected_max_mana)

    def test_get_auto_attack_damage(self):
        """
        The get_auto_attack_damage function returns a Damage object with random physical damage, according to
        the min/max damage of the character and his level difference
        """
        # let them be the same level so no level difference damage is applied
        for _ in range(100):
            result: Damage = self.dummy.get_auto_attack_damage(target_level=self.dummy.level)
            self.assertTrue(isinstance(result, Damage))
            self.assertEqual(result.magic_dmg, 0)
            self.assertNotEqual(result.phys_dmg, 0)
            phys_dmg = result.phys_dmg

            self.assertTrue(int(self.dummy.min_damage) <= phys_dmg <= int(self.dummy.max_damage))

    def test_take_attack(self):
        """
        The take_attack function deals the damage given to it to the Character after applying
        armor reduction and absorption
        """
        output = StringIO()
        monster_name = 'WhatUp'
        expected_message = f'{monster_name} attacks {self.dummy.name} for'  # intentionally omit the exact damage
        dmg_to_take = Damage(magic_dmg=10)  # magic so we don't get reduction by the armor
        attacker_level = self.dummy.level
        try:
            sys.stdout = output

            self.dummy.take_attack(monster_name, dmg_to_take, attacker_level)
            self.assertEqual(self.dummy.health, self.health-dmg_to_take.magic_dmg)
            self.assertIn(expected_message, output.getvalue())
        finally:
            sys.stdout = sys.__stdout__

    def test_take_attack_armor_reduction(self):
        """
        Test if the take_attack function actually applies armor reduction
        """
        armor = 500
        self.dummy.attributes['armor'] = armor
        dmg_to_take = Damage(phys_dmg=10)
        attacker_level = self.dummy.level

        # get the expected damage after reduction
        reduction_percentage = armor / (armor + 400 + 85 * attacker_level)
        damage_to_deduct = dmg_to_take.phys_dmg * reduction_percentage
        reduced_damage = dmg_to_take.phys_dmg - damage_to_deduct

        self.dummy.take_attack('', dmg_to_take, attacker_level)

        self.assertAlmostEqual(self.dummy.health, self.health - reduced_damage, 1)

    def test_take_attack_absorption(self):
        """
        Test the take_attack function when the monster has an absorption shield
        """
        magic_dmg, absorption_shield = 11, 10
        self.dummy.absorption_shield = absorption_shield
        dmg_to_take = Damage(magic_dmg=magic_dmg)
        attacker_level = self.dummy.level

        self.dummy.take_attack('', dmg_to_take, attacker_level)
        expected_health = self.health - (dmg_to_take.magic_dmg - absorption_shield)
        self.assertEqual(self.dummy.health, expected_health)

    def test_take_attack_absorption_and_armor(self):
        """ Test the function, this time accouting for armor and absorption """
        orig_health = self.dummy.health
        absorption_shield = 16
        armor = 500
        self.dummy.absorption_shield = absorption_shield
        self.dummy.attributes['armor'] = armor
        attacker_level = self.dummy.level

        dmg_to_take = Damage(phys_dmg=15, magic_dmg=15)

        # get the expected damage after armor reduction
        reduction_percentage = armor / (armor + 400 + 85 * attacker_level)
        damage_to_deduct = dmg_to_take.phys_dmg * reduction_percentage
        reduced_damage = dmg_to_take.phys_dmg - damage_to_deduct

        # NOTE: Magical damage always gets absorbed first
        leftover_shield = absorption_shield - dmg_to_take.magic_dmg
        expected_dmg = reduced_damage - leftover_shield

        # ACT
        self.dummy.take_attack('', dmg_to_take, attacker_level)

        self.assertEqual(self.dummy.health, round(orig_health-expected_dmg, 1))

    def test_handle_health_change_increase_out_of_combat(self):
        """
        The handle_health_change function fixes up the character's current health when
        his max health has been modified. (via a Buff most likely)
        """
        # Remove 50 from his health and add 49 to his max health, he should be at 99/149 health
        original_max_health = self.dummy.max_health
        self.dummy.health -= 50
        health_inc = 49
        self.dummy.max_health += health_inc
        expected_health, expected_max_health = 99, 149

        self.dummy._handle_health_change(original_max_health)

        self.assertEqual(self.dummy.health, expected_health)
        self.assertEqual(self.dummy.max_health, expected_max_health)

    def test_handle_health_change_decrease_out_of_combat(self):
        # Remove 50 from his health and decrease his max health by 40, his current health should be unchanged
        original_max_health = self.dummy.max_health
        self.dummy.health -= 50  # simulate damage
        health_dec = 49
        self.dummy.max_health -= health_dec
        # Since its out of combat, his current health should drop as well
        expected_health, expected_max_health = 1, 51

        self.dummy._handle_health_change(original_max_health)

        self.assertEqual(self.dummy.health, expected_health)
        self.assertEqual(self.dummy.max_health, expected_max_health)

    def test_handle_health_change_decrease_in_combat(self):
        # Remove 50 from his health and decrease his max health by 40, his current health should be unchanged
        original_max_health = self.dummy.max_health
        self.dummy.enter_combat()
        self.dummy.health -= 50  # simulate damage
        health_dec = 49
        self.dummy.max_health -= health_dec
        # Since its in combat, his current health should not be affected
        expected_health, expected_max_health = 50, 51

        self.dummy._handle_health_change(original_max_health)

        self.assertEqual(self.dummy.health, expected_health)
        self.assertEqual(self.dummy.max_health, expected_max_health)

    def test_apply_buff(self):
        """
        The difference with this _apply_buff function to the other is
        it also applies attributes
        """
        stren_increase, armor_increase = 100, 100
        test_buff = BeneficialBuff(name="Silence",
                                   buff_stats_and_amounts=(('strength', stren_increase), ('armor', armor_increase)), duration=5)
        orig_strength, orig_armor = self.dummy.attributes['strength'], self.dummy.attributes['armor']
        expected_strength = (orig_strength + stren_increase)
        expected_armor = orig_armor + armor_increase
        expected_min_dmg, expected_max_dmg = self.dummy.equipped_weapon.min_damage + (0.4 * expected_strength), self.dummy.equipped_weapon.max_damage + (0.4 * expected_strength)

        self.dummy._apply_buff(test_buff)

        self.assertEqual(self.dummy.min_damage, expected_min_dmg)
        self.assertEqual(self.dummy.max_damage, expected_max_dmg)
        self.assertEqual(self.dummy.attributes['strength'], expected_strength)
        self.assertEqual(self.dummy.attributes['armor'], expected_armor)

    def test_apply_buff_low_hp_out_of_combat(self):
        """
        Have a character be at low HP and apply a buff which increases his HP
        by 10. If he is out of combat, his health should increase by 10 points

        NOTE: This is somewhat irrelevant, as there should not be a case where the
        character's HP is anything less than maximum while out of combat... but who knows
        what can happen
        """
        health_inc = 10
        health_buff = BeneficialBuff(name="SMALL_HEALTH", buff_stats_and_amounts=[('health', health_inc)], duration=20)
        self.dummy._subtract_health(Damage(phys_dmg=90))
        left_hp = self.dummy.health
        expected_hp = left_hp + health_inc

        self.dummy._apply_buff(health_buff)

        self.assertEqual(self.dummy.health, expected_hp)

    def test_deapply_buff(self):
        stren_increase, armor_increase, health_inc, mana_inc = 100, 100, 100, 100
        test_buff = BeneficialBuff(name="Silence", buff_stats_and_amounts=(('strength', stren_increase), ('armor', armor_increase), ('health', health_inc), ('mana', mana_inc)), duration=5)
        orig_min_dmg, orig_max_dmg = self.dummy.min_damage, self.dummy.max_damage
        orig_strength, orig_armor = self.dummy.attributes['strength'], self.dummy.attributes['armor']
        orig_health, orig_mana = self.dummy.health, self.dummy.mana
        expected_strength = (orig_strength + stren_increase)
        expected_armor = orig_armor + armor_increase
        expected_min_dmg, expected_max_dmg = self.dummy.equipped_weapon.min_damage + (
        0.4 * expected_strength), self.dummy.equipped_weapon.max_damage + (0.4 * expected_strength)
        expected_health, expected_mana = orig_health + health_inc, orig_mana + mana_inc
        self.dummy._apply_buff(test_buff)  # <--- Apply the buff
        self.assertEqual(self.dummy.health, expected_health)
        self.assertEqual(self.dummy.mana, expected_mana)
        self.assertEqual(self.dummy.min_damage, expected_min_dmg)
        self.assertEqual(self.dummy.max_damage, expected_max_dmg)
        self.assertEqual(self.dummy.attributes['strength'], expected_strength)
        self.assertEqual(self.dummy.attributes['armor'], expected_armor)

        # Act, deapplying the buff
        self.dummy._deapply_buff(test_buff)
        self.assertEqual(self.dummy.health, orig_health)
        self.assertEqual(self.dummy.mana, orig_mana)
        self.assertEqual(self.dummy.min_damage, orig_min_dmg)
        self.assertEqual(self.dummy.max_damage, orig_max_dmg)
        self.assertEqual(self.dummy.attributes['strength'], orig_strength)
        self.assertEqual(self.dummy.attributes['armor'], orig_armor)

    def test_deapply_buff_with_health_in_combat(self):
        """
        Apply a buff to the user while out of combat, giving him health
         and remove the buff while he is in combat. The maximum health should
         not be less than the current health
        """
        health_inc = 100
        health_buff = BeneficialBuff('HEALTH', buff_stats_and_amounts=[('health', health_inc)], duration=5)
        orig_health, orig_max_health = self.dummy.health, self.dummy.max_health
        self.dummy._apply_buff(health_buff)
        self.assertEqual(self.dummy.health, orig_health + health_inc)
        self.assertEqual(self.dummy.max_health, orig_max_health + health_inc)

        self.dummy.enter_combat()
        self.dummy._deapply_buff(health_buff)

        self.assertEqual(self.dummy.health, orig_health)
        self.assertEqual(self.dummy.max_health, orig_max_health)
        self.assertGreaterEqual(self.dummy.max_health, self.dummy.health)


if __name__ == '__main__':
    unittest.main()
