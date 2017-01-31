import unittest
import sys
from io import StringIO
import inspect

from classes import Paladin
from spells import PaladinSpell
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
            self.assertNotIn(spell, pl.learned_spells)
        pl._level_up()
        for spell in spells_to_learn:
            self.assertIn(spell, pl.learned_spells)

    def test_level_up_to_level(self):
        """ Except the normal behaviour, it should learn new spells for the character """
        # empty the learned spells, it's stored as a static variable, which is not good practice but doesn't hurt in the game
        Paladin.learned_spells = {}
        pl = Paladin(name="fuck a nine to five")
        to_level = 4

        spells_to_learn = [spell for level in range(2, to_level + 1) for spell in load_paladin_spells_for_level(level)]
        for spell in spells_to_learn:
            has_not_learned_spell = spell.name not in pl.learned_spells
            has_smaller_rank = spell.rank > pl.learned_spells[spell.name].rank if not has_not_learned_spell else False
            self.assertTrue(has_not_learned_spell or has_smaller_rank)
        pl._level_up(to_level=to_level)
        for spell in spells_to_learn:
            self.assertIn(spell.name, pl.learned_spells)

    def test_lookup_and_handle_new_spells(self):
        """ Should look up the available spells for our level and learn them or update our existing ones"""
        Paladin.learned_spells = {}
        pl = Paladin(name="fuck a nine to five")
        print(pl.learned_spells)
        pl.level = 3
        spells_to_learn = [spell for spell in load_paladin_spells_for_level(pl.level)]
        for spell in spells_to_learn:
            has_not_learned_spell = spell.name not in pl.learned_spells
            has_smaller_rank = spell.rank > pl.learned_spells[spell.name].rank if not has_not_learned_spell else False
            self.assertTrue(has_not_learned_spell or has_smaller_rank)

        pl._lookup_and_handle_new_spells()

        for spell in spells_to_learn:
            self.assertIn(spell.name, pl.learned_spells)

    def test_learn_new_spell(self):
        """ Given a PaladinSpell, add it to the learned_spells dictionary"""
        spell = PaladinSpell(name="Too_Alive", rank=5)
        expected_message = f'You have learned a new spell - {spell.name}'

        self.assertNotIn(spell.name, self.dummy.learned_spells)
        try:
            output = StringIO()
            sys.stdout = output

            self.dummy.learn_new_spell(spell)

            self.assertIn(expected_message, output.getvalue())
        finally:
            sys.stdout = sys.__stdout__
        self.assertIn(spell.name, self.dummy.learned_spells)

    def test_lookup_available_spells_to_learn(self):
        """ It's a generator function returning a spell that can be learnt for the level """
        lev = 3
        expected_spells = load_paladin_spells_for_level(lev)
        generator = self.dummy._lookup_available_spells_to_learn(lev)

        self.assertTrue(inspect.isgenerator(generator))
        for spell in expected_spells:
            self.assertEqual(vars(next(generator)), vars(spell))

    def test_update_spell(self):
        """ The update_spell() function updates a spell we already have learned"""
        f_spell = PaladinSpell('Spell', rank=1)
        s_spell = PaladinSpell('Spell', rank=2)
        expected_message = f'Spell {f_spell.name} has been updated to rank {s_spell.rank}!'
        self.dummy.learn_new_spell(f_spell)

        try:
            output = StringIO()
            sys.stdout = output

            self.dummy.update_spell(s_spell)

            self.assertIn(expected_message, output.getvalue())
        finally:
            sys.stdout = sys.__stdout__

        # assert that it updated the rank
        self.assertEqual(self.dummy.learned_spells[s_spell.name].rank, s_spell.rank)
        self.assertGreater(self.dummy.learned_spells[s_spell.name].rank, f_spell.rank)

if __name__ == '__main__':
    unittest.main()
