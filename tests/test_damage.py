import unittest
from damage import Damage


class DamageTests(unittest.TestCase):
    def test_init(self):
        dmg = Damage(phys_dmg=1.34, magic_dmg=1.49391)
        expected_phys_dmg = 1.3
        expected_m_dmg = 1.5
        expected_absorbed = 0

        # it should round the magic/phys dmg to 1 point after the decimal
        self.assertEqual(dmg.phys_dmg, expected_phys_dmg)
        self.assertEqual(dmg.magic_dmg, expected_m_dmg)
        self.assertEqual(dmg.phys_absorbed, expected_absorbed)
        self.assertEqual(dmg.magic_absorbed, expected_absorbed)


if __name__ == '__main__':
    unittest.main()