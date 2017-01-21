"""
Collect all the tests and run them here
"""
import unittest, os
# Import all the tests, wow what a pain
from tests.models.character import test_loader as test_char_loader, test_saver as test_char_saver, test_saved_character
from tests.models.creatures import test_creature_template, test_creatures, test_npc_vendor, test_loader as test_creatures_loader
from tests.models.creatures.creature_defaults import test_loader as test_creature_def_loader
from tests.models.items import test_loader as test_item_loader, test_item_template, test_loot_table

modules_to_load = [test_saved_character, test_creature_template, test_creatures, test_npc_vendor,
                   test_creatures_loader, test_creature_def_loader, test_item_loader, test_item_template, test_loot_table,
                   test_char_saver]

loader = unittest.TestLoader()
main_suite = loader.loadTestsFromModule(test_char_loader)
for module in modules_to_load:
    main_suite.addTest(loader.loadTestsFromModule(module))
print(type(main_suite))
runner = unittest.TextTestRunner()
runner.run(main_suite)