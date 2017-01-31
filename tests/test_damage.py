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

    def test_eq(self):
        """ Two Damage classes should be equal if their magic/phys dmg and absorbed are equal"""
        dmg_1 = Damage(1, 1)
        dmg_2 = Damage(1, 1)
        self.assertEqual(dmg_1, dmg_2)
        dmg_1.phys_absorbed += 0.1
        self.assertNotEqual(dmg_1, dmg_2)
        dmg_1.phys_absorbed = dmg_2.phys_absorbed
        self.assertEqual(dmg_1, dmg_2)
        dmg_1.magic_dmg += 1
        self.assertNotEqual(dmg_1, dmg_2)

    def test_str_only_phys_dmg(self):
        expected_phys = 10.10
        dmg = Damage(phys_dmg=10.111)
        expected_str = f'{expected_phys:.2f} physical damage'

        self.assertEqual(str(dmg), expected_str)

    def test_str_only_phys_dmg_with_absorbed(self):
        expected_phys = 10.10
        expected_absorbed = 10
        dmg = Damage(phys_dmg=10.111)
        dmg.phys_absorbed = expected_absorbed
        expected_str = f'{expected_phys:.2f} physical damage ({expected_absorbed:.2f} absorbed)'

        self.assertEqual(str(dmg), expected_str)

    def test_str_only_mag_dmg(self):
        expected_magic = 10.10
        dmg = Damage(magic_dmg=10.111)
        expected_str = f'{expected_magic:.2f} magical damage'

        self.assertEqual(str(dmg), expected_str)

    def test_str_only_mag_dmg_with_absorbed(self):
        expected_magic = 10.10
        expected_absorbed = 10
        dmg = Damage(magic_dmg=10.111)
        dmg.magic_absorbed = expected_absorbed
        expected_str = f'{expected_magic:.2f} magical damage ({expected_absorbed:.2f} absorbed)'

        self.assertEqual(str(dmg), expected_str)

    def test_str_with_phys_and_magic_dmg(self):
        expected_phys = 10.2
        expected_magic = 10.10
        dmg = Damage(phys_dmg=10.199, magic_dmg=10.111)
        expected_str = f'{expected_phys:.2f} physical damage and {expected_magic:.2f} magical damage'

        self.assertEqual(str(dmg), expected_str)


if __name__ == '__main__':
    unittest.main()
