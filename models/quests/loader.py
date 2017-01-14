from utils.helper import parse_int
from models.quests.quest_template import QuestSchema
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

        loaded_quests[quest.name] = quest.convert_to_quest_object()

    return loaded_quests
