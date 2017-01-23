from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from utils.helper import parse_int
from quest import Quest, FetchQuest, KillQuest
from database.main import Base


class QuestSchema(Base):
    """
    The quest_template table holds information about quests

        entry - id of the quest
        name - name of the quest
        type - type of the quest (currently supported - killquest and fetchquest)
        required_level - the minimum level a character must have to embark on the quest
        monster_required - the name of the creature that this quest is tied to
        item_required - the item this quest requires (if applicable)
        amount_required - the amount of items this quest required (if applicable)
        zone - the zone of this quest
        subzone - the subzone of this quest
        xp_reward - the amount of experience points this quest award
        comment - a comment about the quest
        item_rewardX is the item's ID (entry) in the item-template table. We can have up to 3 (at once) reward from a quest
            (if applicable)
        item_choice_enabled is a integer representing aboolean (1=true, 0=false) which indicates if the
            character will be awarded all the items on completion or he has to choose one from the X items (if applicable)

    Table is as follows:
entry,            name,    type, required_level,           monster_required,  item_required, amount_required,
    1, A Canine Menace,killquest              1,      (name of monster)Wolf,      Wolf Meat,              10,

CONT--          zone,           sub_zone,   xp_reward, comment
       Elwynn Forest,   Northshire Valley,        300, Our First Quest!

       item_reward1, item_reward2, item_reward3, item_choice_enabled
                  1,            2,         Null,                0


    Type decides what kind of quests it is.
    killquest = kill X amount of monster_required
    fetchquest = obtain X amount of item_required.
    """
    __tablename__ = 'quest_template'

    entry = Column(Integer, primary_key=True)
    name = Column(String(60))
    type = Column(String(60))
    level_required = Column(Integer)
    monster_required = Column(String(60), ForeignKey('creature_template.name'))
    item_required = Column(String(60), ForeignKey('item_template.name'))
    amount_required = Column(Integer)
    zone = Column(String(60))
    sub_zone = Column(String(60))
    xp_reward = Column(Integer)
    description = Column(Text)
    reward1_id = Column('item_reward1', Integer, ForeignKey('item_template.entry'))
    reward2_id = Column('item_reward2', Integer, ForeignKey('item_template.entry'))
    reward3_id = Column('item_reward3', Integer, ForeignKey('item_template.entry'))
    item_choice_enabled = Column(Boolean)

    reward1 = relationship('ItemTemplateSchema', foreign_keys=[reward1_id])
    reward2 = relationship('ItemTemplateSchema', foreign_keys=[reward2_id])
    reward3 = relationship('ItemTemplateSchema', foreign_keys=[reward3_id])

    def convert_to_quest_object(self) -> Quest:
        """
        Convert the QuestSchema object to a Quest object
        The currently supported quest types are:
            killquest = kill X amount of monster_required
            fetchquest = obtain X amount of item_required.
        :return: A KillQuest or FetchQuest object
        """
        entry: int = self.entry
        quest_name: str = self.name
        quest_type: str = self.type
        level_requirement: int = parse_int(self.level_required)
        monster_required: str = self.monster_required
        item_required: str = self.item_required
        amount_required: int = parse_int(self.amount_required)
        xp_reward: int = parse_int(self.xp_reward)
        item_rewards: {str: 'Item'} = {item.name: item.convert_to_item_object()
                                       for item in [self.reward1, self.reward2, self.reward3]
                                       if item is not None}
        item_choice_enabled = bool(self.item_choice_enabled)

        if quest_type == "killquest":
            return KillQuest(quest_name=quest_name,
                             quest_id=entry,
                             required_monster=monster_required,
                             required_kills=amount_required,
                             xp_reward=xp_reward,
                             item_reward_dict=item_rewards,
                             reward_choice_enabled=item_choice_enabled,
                             level_required=level_requirement)
        elif quest_type == "fetchquest":
            return FetchQuest(quest_name=quest_name,
                              quest_id=entry,
                              required_item=item_required,
                              required_item_count=amount_required,
                              xp_reward=xp_reward,
                              item_reward_dict=item_rewards,
                              reward_choice_enabled=item_choice_enabled,
                              level_required=level_requirement)
        else:
            raise Exception(f'The quest type {quest_type} is not supported!')
