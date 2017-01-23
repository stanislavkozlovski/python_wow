"""
Collect all the tests and run them here
"""
import unittest, os
# Import all the tests, wow what a pain
from tests.models.character import test_loader as test_char_loader, test_saver as test_char_saver, test_saved_character
from tests.models.creatures import test_creature_template, test_creatures, test_npc_vendor, test_loader as test_creatures_loader
from tests.models.creatures.creature_defaults import test_loader as test_creature_def_loader
from tests.models.items import test_loader as test_item_loader, test_item_template, test_loot_table
from tests.models.misc import test_misc_loader
from tests.models.quests import test_loader as test_quest_loader, test_quest_template
from tests.models.spells import test_buff_schema, test_dot_schema, test_paladin_spells
from tests.utils import test_helper

modules_to_load = [test_saved_character, test_creature_template, test_creatures, test_npc_vendor,
                   test_creatures_loader, test_creature_def_loader, test_item_loader, test_item_template, test_loot_table,
                   test_char_saver, test_misc_loader, test_quest_loader, test_quest_template, test_buff_schema,
                   test_dot_schema, test_paladin_spells, test_helper]

loader = unittest.TestLoader()
main_suite = loader.loadTestsFromModule(test_char_loader)
for module in modules_to_load:
    main_suite.addTest(loader.loadTestsFromModule(module))

runner = unittest.TextTestRunner()
runner.run(main_suite)
