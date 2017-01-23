import unittest

from tests.delete_test_db import delete_test_db  # module that deletes the DB :)
import database.main
from tests.create_test_db import engine, session, Base


database.main.engine = engine
database.main.session = session
database.main.Base = Base
import models.main
from models.spells.paladin_spells_template import PaladinSpellsSchema
from spells import PaladinSpell
from models.items.item_template import ItemTemplateSchema
from models.spells.spell_dots import DotSchema
from buffs import BeneficialBuff, DoT


class PaladinSpellsSchemaTests(unittest.TestCase):
    def setUp(self):
        """
        Test that the values in the Schema are as expected
        And that the convert_to_paladin_spell_object function works
        """
        self.spell_entry = 4
        self.spell_name = 'Melting Strike'
        self.expected_spell = PaladinSpell(name=self.spell_name, rank=1, damage1=3, damage2=0, damage3=0,
                                           heal1=0, heal2=0, heal3=0, mana_cost=6, cooldown=3,
                                           beneficial_effect=None, harmful_effect=None)

    def test_schema_values(self):
        """ Load a schema object and assert that every value is as expected"""
        loaded_schema: PaladinSpellsSchema = session.query(PaladinSpellsSchema).get(self.spell_entry)

        self.assertTrue(isinstance(loaded_schema.id, int))
        self.assertTrue(isinstance(loaded_schema.name, str))
        self.assertTrue(isinstance(loaded_schema.rank, int))
        self.assertTrue(isinstance(loaded_schema.level_required, int))
        self.assertTrue(isinstance(loaded_schema.damage1, int))
        self.assertTrue(isinstance(loaded_schema.damage2, int))
        self.assertTrue(isinstance(loaded_schema.damage3, int))
        self.assertTrue(isinstance(loaded_schema.heal1, int))
        self.assertTrue(isinstance(loaded_schema.heal2, int))
        self.assertTrue(isinstance(loaded_schema.heal3, int))
        self.assertTrue(isinstance(loaded_schema.mana_cost, int))
        self.assertIsNone(loaded_schema.beneficial_effect)
        self.assertTrue(isinstance(loaded_schema.harmful_effect, int))
        self.assertTrue(isinstance(loaded_schema.cooldown, int))
        self.assertTrue(isinstance(loaded_schema.comment, str))
        self.assertIsNone(loaded_schema.buff)
        self.assertTrue(isinstance(loaded_schema.dot, DotSchema))




def tearDownModule():
    delete_test_db()

if __name__ == '__main__':
    unittest.main()
