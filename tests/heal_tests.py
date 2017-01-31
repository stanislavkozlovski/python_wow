import unittest

from heal import Heal


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


if __name__ == '__main__':
    unittest.main()
