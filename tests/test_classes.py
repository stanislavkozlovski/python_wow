import unittest

from classes import Paladin
from models.spells.loader import load_paladin_spells_for_level


class PaladinTests(unittest.TestCase):
    def setUp(self):
        self.name = "Netherblood"
        self.level = 3
        self.dummy = Paladin(name=self.name, level=self.level, health=100, mana=100, strength=10)

    def test_init(self):
        """ The __init__ should load/save all the spells for the Paladin"""
        spells = [spell for level in range(1,self.level+1) for spell in load_paladin_spells_for_level(level)]

        self.assertNotEqual(len(self.dummy.learned_spells), 0)
        for spell in spells:
            self.assertIn(spell.name, self.dummy.learned_spells)
            char_spell = self.dummy.learned_spells[spell.name]
            # find the largest rank in our spells list (the char has the highest rank only)
            max_rank = list(sorted(filter(lambda x: x.name == spell.name, spells), key=lambda x: x.rank))[-1].rank

            self.assertEqual(char_spell.rank, max_rank)

    def test_leave_combat(self):
        """
        Except the normal behaviour, leave_combat should remove the SOR buff from the pally
        and reset his spell cds
        """
        self.dummy._in_combat = True
        self.dummy.SOR_ACTIVE = True
        for spell in self.dummy.learned_spells.values():
            spell._cooldown_counter = 100

        self.assertTrue(self.dummy.is_in_combat())

        self.dummy.leave_combat()

        self.assertFalse(self.dummy.is_in_combat())
        self.assertFalse(self.dummy.SOR_ACTIVE)
        # All cooldowns should be reset
        self.assertTrue(all([spell._cooldown_counter == 0 for spell in self.dummy.learned_spells.values()]))

    def test_reset_spell_cooldowns(self):
        """ The reset_spell_cooldowns goes through every spell and resets its CD"""
        for spell in self.dummy.learned_spells.values():
            spell._cooldown_counter = 100
        self.assertTrue(all([spell._cooldown_counter != 0 for spell in self.dummy.learned_spells.values()]))

        self.dummy.reset_spell_cooldowns()

        self.assertTrue(all([spell._cooldown_counter == 0 for spell in self.dummy.learned_spells.values()]))

    def test_level_up(self):
        """ Except the normal behaviour, it should learn new spells for the character """
        # empty the learned spells, it's stored as a static variable, which is not good practice but doesn't hurt in the game
        Paladin.learned_spells = {}
        pl = Paladin(name="fuck a nine to five")

        spells_to_learn = [spell.name for spell in load_paladin_spells_for_level(pl.level + 1)]
        for spell in spells_to_learn:
            self.assertNotIn(spell, self.dummy.learned_spells)
        pl._level_up()
        for spell in spells_to_learn:
            self.assertIn(spell, self.dummy.learned_spells)


if __name__ == '__main__':
    unittest.main()
