from copy import deepcopy
import unittest

from buffs import *
from damage import Damage
from exceptions import InvalidBuffError
from constants import KEY_BUFF_TYPE_ARMOR, KEY_BUFF_TYPE_HEALTH, KEY_BUFF_TYPE_MANA, KEY_BUFF_TYPE_STRENGTH


class StatusEffectTests(unittest.TestCase):
    """
    StatusEffect is the base class for buffs
    """
    def test_init(self):
        test_name = 'testman'
        test_duration = 10
        st_ef = StatusEffect(name=test_name, duration=test_duration)

        self.assertEqual(st_ef.name, test_name)
        self.assertEqual(st_ef.duration, test_duration)

    def test_str(self):
        test_name = 'testman'
        test_duration = 10
        st_ef = StatusEffect(name=test_name, duration=test_duration)
        expected_str = "Default Status Effect"

        self.assertEqual(str(st_ef), expected_str)


class BeneficialBuffTests(unittest.TestCase):
    def test_init(self):
        name = 'BMW'
        stats_amounts = [('strength', 10), ('armor', 20), ('health', 30)]
        duration = 10
        expected_buff_amounts = {'strength': 10, 'armor': 20, 'health': 30, 'mana': 0}
        buff = BeneficialBuff(name=name, buff_stats_and_amounts=stats_amounts, duration=duration)

        self.assertEqual(buff.name, name)
        self.assertEqual(buff.buff_amounts, expected_buff_amounts)
        self.assertEqual(buff.duration, duration)
        self.assertEqual(buff.buff_amounts, {
            KEY_BUFF_TYPE_MANA: 0,
            KEY_BUFF_TYPE_STRENGTH: 10,
            KEY_BUFF_TYPE_HEALTH: 30,
            KEY_BUFF_TYPE_ARMOR: 20
        })

    def test_equals_dunder(self):
        """
        Two buffs are only equal if their name, buffs and duration is the same
        """
        name = 'BMW'
        stats_amounts = [('strength', 10), ('armor', 20), ('health', 30)]
        duration = 10
        buff = BeneficialBuff(name=name, buff_stats_and_amounts=stats_amounts, duration=duration)

        name = 'BMW2'
        stats_amounts = [('strength', 10), ('armor', 20), ('health', 30)]
        duration = 10
        buff2 = BeneficialBuff(name=name, buff_stats_and_amounts=stats_amounts, duration=duration)

        self.assertFalse(buff == buff2) # Different names
        buff2.name = 'BMW'
        buff2.duration = 11
        self.assertFalse(buff == buff2) # Different duration
        buff2.duration = 10
        buff2.buff_amounts['strength'] = 9
        self.assertFalse(buff == buff2)  # Different buff amounts
        buff2.buff_amounts['strength'] = 10
        self.assertTrue(buff == buff2)  # Identical

    def test_str_one_attribute(self):
        name = 'X'
        attr_name, attr_increase = KEY_BUFF_TYPE_STRENGTH, 10
        stats_amounts = [(attr_name, attr_increase)]
        duration = 10

        expected_str = f'Increases {attr_name} by {attr_increase} for {duration} turns.'
        buff = BeneficialBuff(name=name, buff_stats_and_amounts=stats_amounts, duration=duration)
        self.assertEqual(str(buff), expected_str)

    def test_str_two_attributes(self):
        name = 'X'
        attr_name, attr_increase = KEY_BUFF_TYPE_ARMOR, 15
        attr_name2, attr_increase2 = KEY_BUFF_TYPE_STRENGTH, 10
        stats_amounts = [(attr_name, attr_increase), (attr_name2, attr_increase2)]
        duration = 10

        expected_str = f'Increases {attr_name} by {attr_increase} and {attr_name2} by {attr_increase2} for {duration} turns.'
        buff = BeneficialBuff(name=name, buff_stats_and_amounts=stats_amounts, duration=duration)
        self.assertEqual(str(buff), expected_str)

    def test_str_three_attributes(self):
        name = 'X'

        attr_name, attr_increase = KEY_BUFF_TYPE_HEALTH, 20
        attr_name2, attr_increase2 = KEY_BUFF_TYPE_ARMOR, 15
        attr_name3, attr_increase3 = KEY_BUFF_TYPE_STRENGTH, 10
        stats_amounts = [(attr_name, attr_increase), (attr_name2, attr_increase2), (attr_name3, attr_increase3)]
        duration = 10

        expected_str = f'Increases {attr_name} by {attr_increase}, {attr_name2} by {attr_increase2} and {attr_name3} by {attr_increase3} for {duration} turns.'
        buff = BeneficialBuff(name=name, buff_stats_and_amounts=stats_amounts, duration=duration)
        self.assertEqual(str(buff), expected_str)

    def test_manage_buff_types_invalid_buff(self):
        """
        The _manage_buff_types function is called to fill the self.buff_amounts dictionary
        with the given buff stats and amounts in the form of a list.
        It also validates that the given bufff type is valid and raises an error if its not
        """
        invalid_buff_type = 'LoLo'
        expected_error_message = f'Buff type {invalid_buff_type} is not supported!'
        buff = BeneficialBuff('dada', [], 3)
        try:
            buff._manage_buff_types([('armor', 5), (invalid_buff_type, 10)])
            self.fail('Should have raised an InvalidBuffError')
        except InvalidBuffError as e:
            self.assertEqual(str(e), expected_error_message)

    def test_get_buffed_attributes(self):
        """
        The get_buffed_attributes function should return the buffs that have a value increase
        """
        expected_result = {
            KEY_BUFF_TYPE_STRENGTH: 10,
            KEY_BUFF_TYPE_ARMOR: 15
        }
        name = 'X'
        attr_name, attr_increase = KEY_BUFF_TYPE_STRENGTH, 10
        attr_name2, attr_increase2 = KEY_BUFF_TYPE_ARMOR, 15
        stats_amounts = [(attr_name, attr_increase), (attr_name2, attr_increase2)]
        duration = 10

        buff = BeneficialBuff(name=name, buff_stats_and_amounts=stats_amounts, duration=duration)
        result = buff.get_buffed_attributes()

        self.assertEqual(result, expected_result)


class DoTTests(unittest.TestCase):
    """
    Tests for the DoT class
    """
    def setUp(self):
        self.name = 'Audi'
        self.damage_tick = Damage(phys_dmg=3)
        self.duration = 5
        self.caster_level = 10

        self.dot_dummy = DoT(self.name, self.damage_tick, self.duration, self.caster_level)

    def test_init(self):
        self.assertEqual(self.dot_dummy.name, self.name)
        self.assertEqual(self.dot_dummy.damage, self.damage_tick)
        self.assertEqual(self.dot_dummy.duration, self.duration)
        self.assertEqual(self.dot_dummy.level, self.caster_level)

    def test_str(self):
        expected_str = f'{self.dot_dummy.name} - Deals {self.dot_dummy.damage} damage every turn for {self.dot_dummy.duration} turns.'
        self.assertEqual(str(self.dot_dummy), expected_str)

    def test_equals(self):
        """
        Two DoTs are equal if their name, damage and duration are the same
        :return:
        """
        second_dot = deepcopy(self.dot_dummy)
        self.assertEqual(self.dot_dummy, second_dot)  # Identical
        second_dot.name = self.name + ' '
        self.assertNotEqual(self.dot_dummy, second_dot)  # Name differs
        second_dot.name = self.name
        second_dot.duration = self.duration + 1
        self.assertNotEqual(self.dot_dummy, second_dot)  # Duration differs
        second_dot.duration = self.duration
        second_dot.damage.phys_dmg = 150
        self.assertNotEqual(self.dot_dummy, second_dot)  # Damage differs

if __name__ == '__main__':
    unittest.main()
