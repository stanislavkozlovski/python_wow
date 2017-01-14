from utils.helper import parse_int
from models.quests.quest_template import Quest as QuestSchema
from quest import Quest, FetchQuest, KillQuest
from database.main import session


def load_quests(zone: str, subzone: str, character) -> {str: Quest}:
    """
    Load all the quests in the zone/subzone that are available for the given character.

    :param zone: The zone that the query will use
    :param subzone: The subzone that the query will use
    :param character: The Character object we're loading the quests for.
    :return: A Dctionary Key: Quest Name Value: Quest Object
    """

    loaded_quests: {str: Quest} = {}
    quests = session.query(QuestSchema).filter_by(zone=zone, sub_zone=subzone).all()

    print("Loading Quests...")
    for quest in quests:
        if character.has_completed_quest(quest.entry):
            continue  # do not load the quest into the game if the character has completed it

        entry: int = quest.entry
        quest_name: str = quest.name
        quest_type: str = quest.type
        level_requirement: int = parse_int(quest.level_required)
        monster_required: str = quest.monster_required
        item_required: str = quest.item_required
        amount_required: int = parse_int(quest.amount_required)
        xp_reward: int = parse_int(quest.xp_reward)
        item_rewards: {str: 'Item'} = {item.name: item.convert_to_item_object()
                                       for item in [quest.reward1, quest.reward2, quest.reward3]
                                       if item is not None}
        item_choice_enabled = bool(quest.item_choice_enabled)

        if quest_type == "killquest":
            loaded_quests[quest_name] = KillQuest(quest_name=quest_name,
                                                  quest_id=entry,
                                                  required_monster=monster_required,
                                                  required_kills=amount_required,
                                                  xp_reward=xp_reward,
                                                  item_reward_dict=item_rewards,
                                                  reward_choice_enabled=item_choice_enabled,
                                                  level_required=level_requirement)
        elif quest_type == "fetchquest":
            loaded_quests[quest_name] = FetchQuest(quest_name=quest_name,
                                                   quest_id=entry,
                                                   required_item=item_required,
                                                   required_item_count=amount_required,
                                                   xp_reward=xp_reward,
                                                   item_reward_dict=item_rewards,
                                                   reward_choice_enabled=item_choice_enabled,
                                                   level_required=level_requirement)

    return loaded_quests
