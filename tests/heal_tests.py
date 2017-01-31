import unittest

from heal import Heal, HolyHeal


class HealTests(unittest.TestCase):
    def test_str(self):
        heal_amount = 5.111
        heal = Heal(heal_amount=heal_amount)
        expected_str = f'{heal_amount:.2f}'

        self.assertEqual(str(heal), expected_str)

    def test_add(self):
        """ __add__ takes a numeric type (int/float) """
        heal_amount = 5
        heal = Heal(heal_amount=heal_amount)

        add_amount = 10
        expected_amount = heal_amount + add_amount

        self.assertEqual(heal + add_amount, expected_amount)

    def test_radd(self):
        heal_amount = 5
        heal = Heal(heal_amount=heal_amount)

        add_amount = 10
        expected_amount = heal_amount + add_amount

        add_amount += heal
        self.assertEqual(add_amount, expected_amount)

    def test_iadd(self):
        heal_amount = 5
        heal = Heal(heal_amount=heal_amount)
        add_amount = 10

        expected_heal = Heal(heal_amount=heal_amount + add_amount)

        heal += add_amount
        self.assertEqual(heal, expected_heal)

    def test_sub(self):
        heal_amount = 5
        heal = Heal(heal_amount=heal_amount)
        sub_amount = 3

        expected_amount = 2

        self.assertEqual(heal - sub_amount, expected_amount)

    def test_isub(self):
        heal_amount = 5
        heal = Heal(heal_amount=heal_amount)
        sub_amount = 3

        expected_heal = Heal(heal_amount=heal_amount-sub_amount)
        heal -= sub_amount

        self.assertEqual(heal, expected_heal)

    def test_isub_negative_amount(self):
        """ Should reset it to 0 rather than have it stay negative"""
        heal_amount = 5
        heal = Heal(heal_amount=heal_amount)
        sub_amount = 10

        expected_heal = Heal(heal_amount=0)
        heal -= sub_amount

        self.assertEqual(heal, expected_heal)

    def test_rsub(self):
        heal_amount = 5
        heal = Heal(heal_amount=heal_amount)
        amount = 10

        expected_result = amount - heal_amount

        self.assertEqual(amount-heal, expected_result)

    def test_eq(self):
        """ __eq__ checks for the heal_amount being equal"""
        heal_1 = Heal(heal_amount=5)
        heal_2 = Heal(heal_amount=5)

        self.assertEqual(heal_1, heal_2)


class HolyHealTests(unittest.TestCase):
    def test_init(self):
        # the __init__ should decide whether the heal will be a crit or not, depending
        # on the check_double_heal() function which relies on a constant percentage chance
        # in constants.py

        # create multiple heals
        heals = []
        heal_amount = 5
        for _ in range(100):
            heals.append(HolyHeal(heal_amount).heal_amount)

    def test_str(self):
        heal = HolyHeal(heal_amount=5)
        heal.will_double_heal = False

        expected_message = f'{heal.heal_amount:.2f}'
        self.assertEqual(str(heal), expected_message)

    def test_str_with_double_heal(self):
        heal = HolyHeal(heal_amount=5)
        heal.will_double_heal = True

        expected_message = f'{heal.heal_amount:.2f} crit'
        self.assertEqual(str(heal), expected_message)

    def test_check_double_heal(self):
        """ check_double_heal returns a boolean whether the heal should be double """
        heal = HolyHeal(heal_amount=5)
        double_heals = [heal.check_double_heal() for _ in range(100)]
        false_count = len([part for part in double_heals if not part])
        true_count = len([part for part in double_heals if part])

        # since it's a 30% chance, the false_count should always be bigger
        self.assertGreater(false_count, true_count)
        self.assertTrue(any(double_heals))



if __name__ == '__main__':
    unittest.main()
