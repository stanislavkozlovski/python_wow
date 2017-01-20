import unittest

import database.main
from tests.create_test_db import engine, session, Base
database.main.engine = engine
database.main.session = session
database.main.Base = Base

import models.main
from models.items.loader import load_item
from items import Potion
from buffs import BeneficialBuff


class LoaderTests(unittest.TestCase):
    def setUp(self):
        self.item_entry = 4
        self.name = 'Strength Potion'
        self.buy_price = 1
        self.sell_price = 1
        self.effect_id = 1
        self.effect: BeneficialBuff = BeneficialBuff(name="Heart of a Lion",
                                                     buff_stats_and_amounts=[('armor',0), ('strength', 15), ('health', 0), ('mana', 0)],
                                                     duration=5)
        self.potion = Potion(name=self.name, item_id=self.item_entry, buy_price=self.buy_price, sell_price=self.sell_price,
                             buff=self.effect, quest_id=0)

    def test_load_item_valid_item(self):
        """
        It should return the valid item object
        """
        received_item = load_item(self.item_entry)

        self.assertIsNotNone(received_item)
        self.assertTrue(isinstance(received_item, Potion))
        self.assertEqual(vars(received_item), vars(self.potion))

    def test_load_invalid_item_id(self):
        """ It should raise an exception """
        expected_exception_message = "There is no such item with an ID that's 0 or negative!"
        try:
            received_item = load_item(0)
            self.fail()
        except Exception as e:
            self.assertEqual(e.args[0], "There is no such item with an ID that's 0 or negative!")

        try:
            received_item = load_item(-1)
            self.fail()
        except Exception as e:
            self.assertEqual(e.args[0], "There is no such item with an ID that's 0 or negative!")

    def test_load_non_existing_item_id(self):
        """
        Load an item Id that is not in the DB. Ex: 200
        :return:
        """
        non_existant_id = 1024
        expected_exception_message = f'There is no such item with an ID {non_existant_id}!'
        try:
            received_item = load_item(non_existant_id)
            self.fail()
        except Exception as e:
            self.assertEqual(e.args[0], expected_exception_message)



def tearDownModule():
    import tests.delete_test_db  # module that deletes the DB :)

if __name__ == '__main__':
    unittest.main()
