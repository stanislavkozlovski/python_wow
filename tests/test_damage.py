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

    def test_str_with_phys_and_magic_phys_absorb(self):
        expected_phys = 10.2
        expected_magic = 10.10
        expected_phys_absorbed = 5.5
        dmg = Damage(phys_dmg=10.199, magic_dmg=10.111)
        dmg.phys_absorbed = expected_phys_absorbed
        expected_str = f'{expected_phys:.2f} physical damage ({expected_phys_absorbed:.2f} absorbed) and {expected_magic:.2f} magical damage'

        self.assertEqual(str(dmg), expected_str)

    def test_str_with_phys_dmg_magic_absorbed(self):
        expected_phys = 10.2
        expected_magic = 0
        expected_magic_absorbed = 5.5
        dmg = Damage(phys_dmg=10.199)
        dmg.magic_absorbed = expected_magic_absorbed
        expected_str = f'{expected_phys:.2f} physical damage and {expected_magic:.2f} magical damage ({expected_magic_absorbed:.2f} absorbed)'

        self.assertEqual(str(dmg), expected_str)

    def test_str_with_magic_dmg_phys_absorbed(self):
        expected_magic = 10.2
        expected_phys_absorbed = 5.5
        dmg = Damage(magic_dmg=10.199)
        dmg.phys_absorbed = expected_phys_absorbed
        expected_str = f'0.00 physical damage ({expected_phys_absorbed:.2f} absorbed) and {expected_magic:.2f} magical damage'

        self.assertEqual(str(dmg), expected_str)

    def test_str_with_absorbed_only(self):
        expected_magic_absorbed = 5.5
        expected_phys_absorbed = 5.4
        dmg = Damage()
        dmg.magic_absorbed = expected_magic_absorbed
        dmg.phys_absorbed = expected_phys_absorbed

        expected_str = f'0.00 physical damage ({expected_phys_absorbed:.2f} absorbed) and 0.00 magical damage ({expected_magic_absorbed:.2f} absorbed)'

        self.assertEqual(str(dmg), expected_str)

    def test_str_with_no_damage(self):
        self.assertEqual(str(Damage()), "0 damage")

    def test_sub_with_damage(self):
        """ __sub__ works by adding the phys/magic damage and removing the other from it"""
        dmg_1 = Damage(phys_dmg=5, magic_dmg=5)
        dmg_2 = Damage(phys_dmg=2, magic_dmg=2)
        expected_result = (5+5) - (2+2)

        self.assertEqual(dmg_1-dmg_2, expected_result)

    def test_sub_with_int(self):
        dmg_1 = Damage(phys_dmg=5, magic_dmg=5)
        dmg_2 = 4
        expected_result = (5+5) - 4

        self.assertEqual(dmg_1-dmg_2, expected_result)

    def test_isub_tuple(self):
        dmg_1 = Damage(phys_dmg=10, magic_dmg=10)
        dmg_2 = (5, 5)
        expected_result = Damage(phys_dmg=5, magic_dmg=5)

        dmg_1 -= dmg_2
        self.assertEqual(dmg_1, expected_result)

    def test_isub_damage(self):
        dmg_1 = Damage(phys_dmg=10, magic_dmg=10)
        dmg_2 = Damage(phys_dmg=5, magic_dmg=7)
        expected_result = Damage(phys_dmg=5, magic_dmg=3)

        dmg_1 -= dmg_2

        self.assertEqual(dmg_1, expected_result)

    def test_isub_negative_damage(self):
        """ It should reset the damage to 0, rather than making it negative"""
        dmg_1 = Damage(phys_dmg=10, magic_dmg=10)
        dmg_2 = Damage(phys_dmg=15, magic_dmg=117)
        expected_result = Damage(phys_dmg=0, magic_dmg=0)

        dmg_1 -= dmg_2

        self.assertEqual(dmg_1, expected_result)

    def test_iadd_tuple(self):
        dmg_1 = Damage(phys_dmg=10, magic_dmg=10)
        dmg_2 = (5, 6)
        expected_result = Damage(phys_dmg=15, magic_dmg=16)

        dmg_1 += dmg_2
        self.assertEqual(dmg_1, expected_result)

    def test_iadd_damage(self):
        dmg_1 = Damage(phys_dmg=10, magic_dmg=10)
        dmg_2 = Damage(phys_dmg=5, magic_dmg=6)
        expected_result = Damage(phys_dmg=15, magic_dmg=16)

        dmg_1 += dmg_2
        self.assertEqual(dmg_1, expected_result)

    def test_mul(self):
        dmg_1 = Damage(phys_dmg=2, magic_dmg=3)
        multiplier = 2
        expected = Damage(phys_dmg=2*2, magic_dmg=3*2)

        self.assertEqual(dmg_1 * multiplier, expected)

    def test_handle_absorption(self):
        """ The handle_absorption function subtracts the absorbed damage from the damage.
            Magical damage always gets absorbed first """
        absorption_shield = 5
        dmg = Damage(phys_dmg=10, magic_dmg=6)
        dmg.handle_absorption(absorption_shield)

        expected_dmg = Damage(phys_dmg=10, magic_dmg=1)
        expected_dmg.magic_absorbed = 5

        self.assertEqual(dmg, expected_dmg)


if __name__ == '__main__':
    unittest.main()
