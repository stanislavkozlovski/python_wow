import unittest

from tests.delete_test_db import delete_test_db  # module that deletes the DB :)
import database.main
from tests.create_test_db import engine, session, Base
database.main.engine = engine
database.main.session = session
database.main.Base = Base

import models.main
from models.misc.level_xp_requirement import LevelXpRequirementSchema
from models.misc.levelup_stats import LevelUpStatsSchema
from models.misc.loader import load_character_level_stats, load_character_xp_requirements


class MiscLoaderTests(unittest.TestCase):
    """
    There isn't too much to test here except performance
    """
    def setUp(self):
        self.expected_levelup_stats_count = session.query(LevelUpStatsSchema).count()
        self.expected_levelxp_req_count = session.query(LevelXpRequirementSchema).count()

    def test_load_character_level_stats_correctness(self):
        """
        It should load all the level stats
        """
        loaded_stats = load_character_level_stats()

        self.assertIsNotNone(loaded_stats)
        self.assertTrue(isinstance(loaded_stats, dict))

        # assert that each level is in the keys of the dict
        # (assumes every row is unique corresponding for each level)
        for level in range(1, self.expected_levelup_stats_count + 1):
            self.assertIn(level, loaded_stats)

        self.assertTrue(len(loaded_stats.keys()), self.expected_levelup_stats_count)



def tearDownModule():
    delete_test_db()

if __name__ == '__main__':
    unittest.main()
