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


if __name__ == '__main__':
    unittest.main()
