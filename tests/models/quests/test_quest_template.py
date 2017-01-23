import unittest

from tests.delete_test_db import delete_test_db  # module that deletes the DB :)
import database.main
from tests.create_test_db import engine, session, Base


database.main.engine = engine
database.main.session = session
database.main.Base = Base
import models.main
from models.quests.quest_template import QuestSchema
from models.items.item_template import ItemTemplateSchema
from quest import KillQuest, FetchQuest, Quest


class CreatureTemplateTests(unittest.TestCase):
    def setUp(self):
        """
        There are two type of quests for now - KillQuest and FetchQuest.
        Test both of them
        """
        self.quest_entry = 1
        self.name = 'A Canine Menace'
        self.type = 'killquest'
        self.level_required = 1
        self.monster_required = 'Wolf'
        self.item_required = None
        self.amount_required = 5
        self.zone = 'Northshire Abbey'
        self.subzone = 'Northshire Valley'
        self.xp_reward = 300
        self.description = 'Kill 5 Wolves'
        self.item_reward1 = None
        self.item_reward2 = None
        self.item_reward3 = None
        self.item_choice_enabled = False
        self.expected_kill_quest = KillQuest(quest_name=self.name, quest_id=self.quest_entry,
                                             xp_reward=self.xp_reward, item_reward_dict={}, reward_choice_enabled=False,
                                             level_required=self.level_required, is_completed=False,
                                             required_monster='Wolf', required_kills=5)

    def test_values(self):
        received_q_schema: QuestSchema = session.query(QuestSchema).get(self.quest_entry)
        self.assertTrue(isinstance(received_q_schema.entry, int))
        self.assertTrue(isinstance(received_q_schema.name, str))
        self.assertTrue(isinstance(received_q_schema.type, str))
        self.assertTrue(isinstance(received_q_schema.level_required, int))
        self.assertTrue(isinstance(received_q_schema.monster_required, str))
        self.assertIsNone(received_q_schema.item_required)
        self.assertTrue(isinstance(received_q_schema.amount_required, int))
        self.assertTrue(isinstance(received_q_schema.zone, str))
        self.assertTrue(isinstance(received_q_schema.sub_zone, str))
        self.assertTrue(isinstance(received_q_schema.xp_reward, int))
        self.assertTrue(isinstance(received_q_schema.description, str))
        self.assertIsNone(received_q_schema.reward1_id)
        self.assertIsNone(received_q_schema.reward2_id)
        self.assertIsNone(received_q_schema.reward3_id)
        self.assertTrue(isinstance(received_q_schema.item_choice_enabled, bool))
        # since there are no items as reward these should be none
        self.assertIsNone(received_q_schema.reward1)
        self.assertIsNone(received_q_schema.reward2)
        self.assertIsNone(received_q_schema.reward3)

    def test_convert_to_quest_object_killquest(self):
        received_kill_quest = session.query(QuestSchema).get(self.quest_entry).convert_to_quest_object()
        self.assertEqual(vars(received_kill_quest), vars(self.expected_kill_quest))



def tearDownModule():
    delete_test_db()

if __name__ == '__main__':
    unittest.main()
