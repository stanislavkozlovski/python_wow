import unittest
from unittest.mock import Mock
import sys
import termcolor
from io import StringIO
from exceptions import NonExistantBuffError


from constants import KEY_ARMOR_ATTRIBUTE
from entities import LivingThing, FriendlyNPC, VendorNPC, Monster
from damage import Damage
from items import Item
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


if __name__ == '__main__':
    unittest.main()
