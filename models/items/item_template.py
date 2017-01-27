from sqlalchemy import Column, Integer, String, ForeignKey

from models.spells.loader import load_buff
from utils.helper import create_attributes_dict
from items import Weapon, Equipment, Potion, Item
from utils.helper import parse_int
from database.main import Base


class ItemTemplateSchema(Base):
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
    sub_type = Column(String(30), default=None)
    armor = Column(Integer, default=0)
    health = Column(Integer, default=0)
    mana = Column(Integer, default=0)
    strength = Column(Integer, default=0)
    agility = Column(Integer, default=0)
    buy_price = Column(Integer, default=0)
    sell_price = Column(Integer, default=0)
    min_dmg = Column(Integer, default=0)
    max_dmg = Column(Integer, default=0)
    quest_id = Column(Integer, ForeignKey('quest_template.entry'), nullable=True, default=None)
    effect = Column(Integer)

    def convert_to_item_object(self) -> Item:
        item_id: int = self.entry
        item_name: str = self.name
        item_type: str = self.type
        item_buy_price: int = parse_int(self.buy_price)
        item_sell_price: int = parse_int(self.sell_price)

        if item_type == 'misc':
            item_quest_id = self.quest_id
            return Item(name=item_name, item_id=item_id, buy_price=item_buy_price, sell_price=item_sell_price,
                        quest_id=item_quest_id)
        elif item_type in ['weapon', 'equipment']:
            item_health: int = parse_int(self.health)
            item_mana: int = parse_int(self.mana)
            item_armor: int = parse_int(self.armor)
            item_strength: int = parse_int(self.strength)
            item_agility: int = parse_int(self.agility)
            attributes: {str: int} = create_attributes_dict(bonus_health=item_health, bonus_mana=item_mana,
                                                            armor=item_armor, strength=item_strength,
                                                            agility=item_agility)
            if item_type == 'weapon':
                item_min_dmg: int = parse_int(self.min_dmg)
                item_max_dmg: int = parse_int(self.max_dmg)

                return Weapon(name=item_name, item_id=item_id, attributes_dict=attributes,
                              buy_price=item_buy_price, sell_price=item_sell_price,
                              min_damage=item_min_dmg, max_damage=item_max_dmg)
            else:
                item_slot: str = self.sub_type

                return Equipment(name=item_name, item_id=item_id, slot=item_slot, attributes_dict=attributes,
                                 buy_price=item_buy_price, sell_price=item_sell_price)
        elif item_type == 'potion':
            buff_id: int = self.effect
            item_buff_effect: 'BeneficialBuff' = load_buff(buff_id)

            return Potion(name=item_name, item_id=item_id, buy_price=item_buy_price, sell_price=item_sell_price,
                          buff=item_buff_effect)
        else:
            raise Exception(f'Unsupported item type {item_type}')
