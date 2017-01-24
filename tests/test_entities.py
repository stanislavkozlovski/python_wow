import unittest
import sys
import termcolor
from io import StringIO
from exceptions import NonExistantBuffError

from constants import KEY_ARMOR_ATTRIBUTE
from entities import LivingThing, FriendlyNPC
from damage import Damage
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
        self.gossip = 'Hey guyss'
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

if __name__ == '__main__':
    unittest.main()
