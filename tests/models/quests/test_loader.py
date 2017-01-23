import unittest
from unittest.mock import Mock

from tests.delete_test_db import delete_test_db  # module that deletes the DB :)
import database.main
from tests.create_test_db import engine, session, Base


database.main.engine = engine
database.main.session = session
database.main.Base = Base

import models.main
from models.quests.quest_template import QuestSchema
from models.quests.loader import load_quests
from models.items.item_template import ItemTemplateSchema
from quest import KillQuest, FetchQuest, Quest
from items import Item, Potion
from buffs import BeneficialBuff


class QuestLoaderTests(unittest.TestCase):
    def setUp(self):
        """
        Functions we'll be testing:
            load_quests - Returns all the quests in the zone that the character has not completed
        """
        self.char_mock = Mock(has_completed_quest=lambda x: False)

    def get_expected_quests(self) -> {str: Quest}:
        quest_entry, name, level_required = 1, 'A Canine Menace', 1
        monster_required, xp_reward = 'Wolf', 300
        expected_kill_quest = KillQuest(quest_name=name, quest_id=quest_entry,
                                             xp_reward=xp_reward, item_reward_dict={}, reward_choice_enabled=False,
                                             level_required=level_required, is_completed=False,
                                             required_monster=monster_required, required_kills=5)
        entry, name, type = 2, 'Canine-Like Hunger', 'fetchquest'
        level_required, monster_required, amount_required = 1, None, 2
        zone, sub_zone, xp_reward = 'Northshire Abbey', 'Northshire Valley', 300
        item_rewards = {
            'Wolf Meat': Item(name='Wolf Meat', item_id=1, buy_price=1, sell_price=1, quest_id=2),
            'Strength Potion': Potion(name='Strength Potion', item_id=4, buy_price=1, sell_price=1,
                                      buff=BeneficialBuff(name="Heart of a Lion",
                                                          buff_stats_and_amounts=[('armor', 0), ('strength', 15),
                                                                                  ('health', 0), ('mana', 0)],
                                                          duration=5))}
        expected_quest = FetchQuest(quest_name=name, quest_id=entry, required_item='Wolf Meat',
                                    xp_reward=xp_reward, item_reward_dict=item_rewards, reward_choice_enabled=True,
                                    level_required=level_required, required_item_count=amount_required,
                                    is_completed=False)

        return {expected_quest.name: expected_quest,
                expected_kill_quest.name: expected_kill_quest}

    def test_load_quests_valid_zone_char_not_completed_anything(self):
        """
        Load the quests from Northshire Abbey / Northshire Valley,
        we should see all of them
        """
        expected_quests = self.get_expected_quests()
        received_quests = load_quests('Northshire Abbey', 'Northshire Valley', self.char_mock)
        self.assertEqual(received_quests, expected_quests)

    def test_load_quests_valid_zone_char_completed_everything(self):
        """
        Since the character has completed everything, we should not get any quests
        """
        self.char_mock.has_completed_quest = lambda x: True
        expected_quests = {}
        received_quests = load_quests('Northshire Abbey', 'Northshire Valley', self.char_mock)

        self.assertEqual(len(received_quests.keys()), 0)
        self.assertEqual(received_quests, expected_quests)

    def test_load_quests_invalid_zone(self):
        """
        The zone does not exist, therefore we should not get any quests
        """
        expected_quests = {}
        received_quests = load_quests('AaAa',' AaaA', self.char_mock)

        self.assertEqual(len(received_quests.keys()), 0)
        self.assertEqual(received_quests, expected_quests)


def tearDownModule():
    delete_test_db()

if __name__ == '__main__':
    unittest.main()
