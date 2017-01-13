from sqlalchemy import Column, Integer, String, Text

from database.main import Base


class Quest(Base):
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
    monster_required = Column(String(60))
    item_required = Column(String(60))
    amount_required = Column(Integer)
    zone = Column(String(60))
    sub_zone = Column(String(60))
    xp_reward = Column(Integer)
    comment = Column(Text)
    item_reward1 = Column(Integer)
    item_reward2 = Column(Integer)
    item_reward3 = Column(Integer)
    item_choice_enabled = Column(Integer)  # TODO: Change
