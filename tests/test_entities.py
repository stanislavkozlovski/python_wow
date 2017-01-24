import unittest
import sys
from io import StringIO
from exceptions import NonExistantBuffError

from constants import KEY_ARMOR_ATTRIBUTE
from entities import LivingThing
from buffs import BeneficialBuff


class LivingThingTests(unittest.TestCase):
    def setUp(self):
        self.name = 'Alex'
        self.health = 100
        self.mana = 100
        self.level = 5
        self.dummy_buff = BeneficialBuff(name='Zdrave', buff_stats_and_amounts=[('health', self.health)], duration=5)
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


if __name__ == '__main__':
    unittest.main()
