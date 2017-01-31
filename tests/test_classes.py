import unittest
from unittest.mock import Mock
import sys
from io import StringIO
import inspect

from damage import Damage
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

    def test_spell_handler_sor(self):
        """
        The spell handler takes spell names and casts the appropriate function
        It might work in a bad way since it's not too testable
        """
        unsuccessful_message = 'Unsuccessful cast'
        sor_success_msg = 'SOR_CASTED'
        sor_command_name = 'sor'
        # Mock the function that should get called
        self.dummy.spell_seal_of_righteousness = lambda x: sor_success_msg

        try:
            output = StringIO()
            sys.stdout = output
            result = self.dummy.spell_handler(sor_command_name, None)

            self.assertNotIn(unsuccessful_message, output.getvalue())
        finally:
            sys.stdout = sys.__stdout__

        # Assert that it called the spell_seal_of_righteousness function
        self.assertEqual(result, sor_success_msg)

    def test_spell_handler_fol(self):
        unsuccessful_message = 'Unsuccessful cast'
        fol_success_msg = 'FOL_CASTED'
        fol_command_name = 'fol'
        # Mock the function that should get called
        self.dummy.spell_flash_of_light = lambda x: fol_success_msg

        try:
            output = StringIO()
            sys.stdout = output
            result = self.dummy.spell_handler(fol_command_name, None)

            self.assertNotIn(unsuccessful_message, output.getvalue())
        finally:
            sys.stdout = sys.__stdout__

        # Assert that it called the spell_seal_of_righteousness function
        self.assertEqual(result, fol_success_msg)

    def test_spell_handler_ms(self):
        unsuccessful_message = 'Unsuccessful cast'
        ms_success_msg = 'MS_CASTED'
        ms_command_name = 'ms'
        # Mock the function that should get called
        self.dummy.spell_melting_strike = lambda target=None, spell=None: ms_success_msg

        try:
            output = StringIO()
            sys.stdout = output
            result = self.dummy.spell_handler(ms_command_name, None)

            self.assertNotIn(unsuccessful_message, output.getvalue())
        finally:
            sys.stdout = sys.__stdout__

        # Assert that it called the spell_seal_of_righteousness function
        self.assertEqual(result, ms_success_msg)

    def test_spell_handler_invalid_spell(self):
        unsuccessful_message = 'Unsuccessful cast'
        invalid_command = 'WooHoo'

        try:
            output = StringIO()
            sys.stdout = output
            result = self.dummy.spell_handler(invalid_command, None)

            self.assertIn(unsuccessful_message, output.getvalue())
        finally:
            sys.stdout = sys.__stdout__

        self.assertFalse(result)

    def test_spell_seal_of_righteousness(self):
        sor: PaladinSpell = self.dummy.learned_spells[Paladin.KEY_SEAL_OF_RIGHTEOUSNESS]
        expected_message = f'{self.dummy.name} activates {Paladin.KEY_SEAL_OF_RIGHTEOUSNESS}!'
        expected_mana = self.dummy.mana - sor.mana_cost
        self.assertFalse(self.dummy.SOR_ACTIVE)
        self.assertEqual(self.dummy.SOR_TURNS, 0)

        try:
            output = StringIO()
            sys.stdout = output

            self.dummy.spell_seal_of_righteousness(sor)

            self.assertIn(expected_message, output.getvalue())
        finally:
            sys.stdout = sys.__stdout__

        self.assertTrue(self.dummy.SOR_ACTIVE)
        self.assertEqual(self.dummy.SOR_TURNS, 3)
        self.assertEqual(self.dummy.mana, expected_mana)

    def test_spell_seal_of_righteousness_attack(self):
        sor: PaladinSpell = self.dummy.learned_spells[Paladin.KEY_SEAL_OF_RIGHTEOUSNESS]
        expected_damage = sor.damage1
        self.dummy.spell_seal_of_righteousness(sor)
        self.assertTrue(self.dummy.SOR_ACTIVE)
        self.assertEqual(self.dummy.SOR_TURNS, 3)

        result = self.dummy._spell_seal_of_righteousness_attack()

        self.assertEqual(result, expected_damage)
        self.assertEqual(self.dummy.SOR_TURNS, 2)

    def test_spell_seal_of_righteousness_attack_fade(self):
        sor: PaladinSpell = self.dummy.learned_spells[Paladin.KEY_SEAL_OF_RIGHTEOUSNESS]
        expected_message = f'{Paladin.KEY_SEAL_OF_RIGHTEOUSNESS} has faded from {self.dummy.name}'
        self.dummy.spell_seal_of_righteousness(sor)
        self.assertTrue(self.dummy.SOR_ACTIVE)
        self.dummy.SOR_TURNS = 1
        self.dummy._spell_seal_of_righteousness_attack()
        self.assertEqual(self.dummy.SOR_TURNS, 0)
        self.assertTrue(self.dummy.SOR_ACTIVE)

        # Should fade now and not do any damage on turn end
        try:
            output = StringIO()
            sys.stdout = output

            self.dummy.end_turn_update()

            self.assertIn(expected_message, output.getvalue())
        finally:
            sys.stdout = sys.__stdout__

        self.assertFalse(self.dummy.SOR_ACTIVE)

    def test_spell_flash_of_light(self):
        import heal
        # Nullify the chance to double heal for consistent testing
        heal.DOUBLE_HEAL_CHANCE = 0
        fol: PaladinSpell = self.dummy.learned_spells[Paladin.KEY_FLASH_OF_LIGHT]
        expected_message = f'{self.dummy.name} activates {Paladin.KEY_FLASH_OF_LIGHT}!'
        expected_mana = self.dummy.mana - fol.mana_cost
        orig_health = 1
        self.dummy.health = orig_health
        expected_message = f'{fol.name} healed {self.dummy.name} for {fol.heal1}.'

        try:
            output = StringIO()
            sys.stdout = output

            self.dummy.spell_flash_of_light(fol)

            self.assertIn(expected_message, output.getvalue())
        finally:
            sys.stdout = sys.__stdout__

        self.assertEqual(self.dummy.mana, expected_mana)
        self.assertEqual(self.dummy.health, orig_health + fol.heal1)

    def test_spell_flash_of_light_overheal(self):
        import heal
        # Nullify the chance to double heal for consistent testing
        heal.DOUBLE_HEAL_CHANCE = 0
        fol: PaladinSpell = self.dummy.learned_spells[Paladin.KEY_FLASH_OF_LIGHT]
        expected_message = f'{fol.name} healed {self.dummy.name} for 0.00 ({fol.heal1:.2f} Overheal).'
        expected_mana = self.dummy.mana - fol.mana_cost
        orig_health = self.dummy.health
        self.dummy.health = orig_health

        try:
            output = StringIO()
            sys.stdout = output

            self.dummy.spell_flash_of_light(fol)

            self.assertIn(expected_message, output.getvalue())
        finally:
            sys.stdout = sys.__stdout__

        self.assertEqual(self.dummy.mana, expected_mana)
        self.assertEqual(self.dummy.health, orig_health)  # should have only overhealed

    def test_spell_melting_strike(self):
        ms: PaladinSpell = self.dummy.learned_spells[Paladin.KEY_MELTING_STRIKE]
        expected_mana = self.dummy.mana - ms.mana_cost
        expected_message2 = 'Took attack'
        expected_message3 = 'Took buff'
        take_attack = lambda x, y: print('Took attack')
        add_buff = lambda x: print('Took buff')
        target = Mock(name="All",
                      take_attack=take_attack,
                      add_buff=add_buff)
        expected_message = f'{ms.name} damages {target.name} for {ms.damage1:.2f} physical damage!'

        try:
            output = StringIO()
            sys.stdout = output

            result = self.dummy.spell_melting_strike(ms, target)

            self.assertIn(expected_message, output.getvalue())
            self.assertIn(expected_message2, output.getvalue())
            self.assertIn(expected_message3, output.getvalue())
        finally:
            sys.stdout = sys.__stdout__

        self.assertTrue(result)
        self.assertEqual(expected_mana, self.dummy.mana)

    def test_get_auto_attack_damage(self):
        """ Applies damage reduction in regard to level and adds the sor_damage
            It attaches the sor_damage to the magic_dmg in the Damage class and
            returns the sor_dmg explicitly for easy printing"""
        sor: PaladinSpell = self.dummy.learned_spells[Paladin.KEY_SEAL_OF_RIGHTEOUSNESS]
        self.dummy.spell_seal_of_righteousness(sor)

        received_dmg, sor_dmg = self.dummy.get_auto_attack_damage(self.dummy.level)

        self.assertTrue(isinstance(received_dmg, Damage))
        self.assertTrue(self.dummy.min_damage <= received_dmg.phys_dmg <= self.dummy.max_damage)
        self.assertEqual(received_dmg.magic_dmg, sor.damage1)
        self.assertEqual(sor_dmg, sor.damage1)


if __name__ == '__main__':
    unittest.main()
