import unittest

from heal import Heal


class HealTests(unittest.TestCase):
    def test_str(self):
        heal_amount = 5.111
        heal = Heal(heal_amount=heal_amount)
        expected_str = f'{heal_amount:.2f}'

        self.assertEqual(str(heal), expected_str)


if __name__ == '__main__':
    unittest.main()
