import unittest

from constants import KEY_ARMOR_ATTRIBUTE
from entities import LivingThing


class LivingThingTests(unittest.TestCase):
    def setUp(self):
        self.name = 'Alex'
        self.health = 100
        self.mana = 100
        self.level = 5
        self.expected_attributes = {KEY_ARMOR_ATTRIBUTE: 0}  # the base stat for every creature
        self.dummy = LivingThing(name=self.name, health=self.health, mana=self.mana, level=self.level)

    def test_init(self):
        self.assertEqual(self.dummy.name, self.name)
        self.assertEqual(self.dummy.health, self.health)
        self.assertEqual(self.dummy.max_health, self.health)
        self.assertEqual(self.dummy.mana, self.mana)
        self.assertEqual(self.dummy.max_mana, self.mana)
        self.assertEqual(self.dummy.level, self.level)
        self.assertEqual(self.dummy.absorption_shield, 0)
        self.assertEqual(self.dummy.attributes, self.expected_attributes)
        self.assertTrue(self.dummy._alive)
        self.assertFalse(self.dummy._in_combat)
        self.assertEqual(self.dummy.buffs, {})  # should not have any buffs on creation

    def test_enter_in_leave_combat_methods(self):
        """
        The is_in_combat function should return whether the object is in combat
            enter_combat should put him in combat
            leave_combat should leave combat and regenerate the living thing
        """
        self.assertFalse(self.dummy.is_in_combat())
        self.dummy.enter_combat()  # enter combat
        self.assertTrue(self.dummy.is_in_combat())

        self.assertEqual(self.dummy.health, self.health)
        self.dummy.health -= 50
        self.assertNotEqual(self.dummy.health, self.health)

        self.dummy.leave_combat()
        # Should have left combat and regenerated health
        self.assertFalse(self.dummy.is_in_combat())
        self.assertEqual(self.dummy.health, self.health)




if __name__ == '__main__':
    unittest.main()
