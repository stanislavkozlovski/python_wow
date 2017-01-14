from models.items.item_template import ItemTemplate
from models.spells.loader import load_buff
from loader import parse_int
from items import create_attributes_dict, Weapon, Equipment, Potion, Item
from database.main import session


def load_item(item_ID: int):
    """
    Load an item from item_template, convert it to a object of Class Item and return it
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
    :returns a class object, depending on what the type is
    """
    if item_ID <= 0 or item_ID is None:
        raise Exception("There is no such item with an ID that's 0 or negative!")
    item_template_info = session.query(ItemTemplate).get(item_ID)

    item_id: int = item_template_info.entry
    item_name: str = item_template_info.name
    item_type: str = item_template_info.type
    item_buy_price: int = parse_int(item_template_info.buy_price)
    item_sell_price: int = parse_int(item_template_info.sell_price)

    if item_type == 'misc':
        item_quest_id = item_template_info.quest_id
        return Item(name=item_name, item_id=item_id, buy_price=item_buy_price, sell_price=item_sell_price,
                    quest_ID=item_quest_id)
    elif item_type in ['weapon', 'equipment']:
        item_health: int = parse_int(item_template_info.health)
        item_mana: int = parse_int(item_template_info.mana)
        item_armor: int = parse_int(item_template_info.armor)
        item_strength: int = parse_int(item_template_info.strength)
        item_agility: int = parse_int(item_template_info.agility)
        attributes: {str: int} = create_attributes_dict(bonus_health=item_health, bonus_mana=item_mana,
                                                        armor=item_armor, strength=item_strength, agility=item_agility)
        if item_type == 'weapon':
            item_min_dmg: int = parse_int(item_template_info.min_dmg)
            item_max_dmg: int = parse_int(item_template_info.max_dmg)

            return Weapon(name=item_name, item_id=item_id, attributes_dict=attributes,
                                buy_price=item_buy_price, sell_price=item_sell_price,
                                min_damage=item_min_dmg, max_damage=item_max_dmg)
        else:
            item_slot: str = item_template_info.sub_type

            return Equipment(name=item_name, item_id=item_id, slot=item_slot, attributes_dict=attributes,
                             buy_price=item_buy_price, sell_price=item_sell_price)
    elif item_type == 'potion':
        buff_id: int = item_template_info.effect
        item_buff_effect: 'BeneficialBuff' = load_buff(buff_id)

        return Potion(name=item_name, item_id=item_id, buy_price=item_buy_price, sell_price=item_sell_price,
                      buff=item_buff_effect)
    else:
        raise Exception(f'Unsupported item type {item_type}')
