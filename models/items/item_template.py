from sqlalchemy import Column, Integer, String, ForeignKey

from database.main import Base


class ItemTemplate(Base):
    """
    Holds information about an item.
        entry - the unique ID
        name - the name of the item
        type - the type of the item (currently supported - misc, weapon, equipment, potion)
        subtype - the subtype, currently applies to equipment - ex: headpiece
        armor - the amount of armor this item gives
        strength - the amount of strength this item gives
        agility - the amount of agility this item gives
        buy_price - the amount of gold this item is bought for (by default)
        sell_price - the amount of gold this item is sold for
        min_dmg - the minimum amount of damage this item deals (if applicable)
        max_dmg - the maximum amount of damage this item deals (if applicable)
        quest_id - the ID of the quest this item is connected to (if applicable)
        effect - the effect this item has (if applicable) ex: A potion gives this effect on use

    The item_template table is as follows:
    entry,      name, type,  subtype, armor, health, mana, strength, agility, buy_price, sell_price, min_dmg, max_dmg, quest_ID, effect
        1,'Wolf Pelt','misc', Null, Null,   Null, Null,     Null,    Null,         1,          1,     Null, Null  ,        1,      0
    The item is of type misc, making us use the default class Item. It is also collected for the quest with ID 1

    entry,             name,    type, subtype,  armor, health, mana, strength, agility,  buy_price, sell_price, min_dmg, max_dmg, quest_ID, effect
      100, 'Arcanite Reaper', 'weapon',   Null,  0,     0,    0,        0,       0,        125,          100,     56,      128,        0,      0
    This item is of type weapon, making us use the class Weapon to create it

    entry,             name,    type,   subtype, armor, health, mana, strength, agility, buy_price, sell_price, min_dmg, max_dmg, quest_ID, effect
        4,'Strength Potion', 'potion',    Null, Null,   Null, Null,    Null,    Null,         1,           1,    Null,    Null,        0,      1
    This item is of type Potion and when consumed gives off the effect (spell_buffs table entry) 1
    """
    __tablename__ = 'item_template'

    entry = Column(Integer, primary_key=True)
    name = Column(String(40), unique=True)
    type = Column(String(30))
    sub_type = Column(String(30))
    armor = Column(Integer)
    health = Column(Integer)
    mana = Column(Integer)
    strength = Column(Integer)
    agility = Column(Integer)
    buy_price = Column(Integer)
    sell_price = Column(Integer)
    min_dmg = Column(Integer)
    max_dmg = Column(Integer)
    quest_id = Column(Integer, ForeignKey('quest_template.entry'), nullable=True)
    effect = Column(Integer)
