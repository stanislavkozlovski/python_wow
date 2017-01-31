"""
This holds the classes for every kind of item in the game
"""
from buffs import BeneficialBuff
from termcolor import colored
from constants import (
    CHAR_ATTRIBUTES_TEMPLATE, KEY_BONUS_HEALTH_ATTRIBUTE, KEY_BONUS_MANA_ATTRIBUTE,
    KEY_STRENGTH_ATTRIBUTE, KEY_AGILITY_ATTRIBUTE, KEY_ARMOR_ATTRIBUTE)
from utils.helper import display_attributes


class Item:
    def __init__(self, name: str, item_id: int, buy_price: int, sell_price: int, quest_id: int=0):
        self.name = name
        self.id = item_id
        self.buy_price = buy_price
        self.sell_price = sell_price
        self.quest_id = quest_id

    def __str__(self):
        return colored(f'{self.name}', color="grey") + ' - Miscellaneous Item'

    def __eq__(self, other):
        return self.id == other.id


class Weapon(Item):
    def __init__(self, name: str, item_id: int, buy_price: int = 0, sell_price: int = 0, min_damage: int = 0,
                 max_damage: int = 1, attributes: dict=CHAR_ATTRIBUTES_TEMPLATE):
        super().__init__(name, item_id, buy_price, sell_price)
        self.min_damage = min_damage
        self.max_damage = max_damage
        self.attributes = attributes  # the attributes this item gives on equip

    def __str__(self):
        return colored(f'{self.name}', color="green") + f'- Weapon ({self.min_damage}-{self.max_damage}) damage'


class Equipment(Item):
    """ Any item that can be equipped in an equipment slot, as distinguished from items that can only be
    carried in the inventory.
    ex: Headpiece, Shoulderpad, Necklace, Chestguard, Bracer, Gloves, Belt, Leggings, Boots"""
    def __init__(self, name: str, item_id: int, slot: str, attributes: dict=CHAR_ATTRIBUTES_TEMPLATE, buy_price: int=0, sell_price: int=0):
        super().__init__(name, item_id, buy_price, sell_price)
        self.slot = slot
        self.attributes = attributes

    def __str__(self):
        return (colored(self.name, color='green')
                + ' - {slot_pos} Equipment: '.format(slot_pos=self.slot[0].upper() + self.slot[1:])
                + display_attributes(self.attributes))


class Potion(Item):
    """ Consumable item that gives a buff to the player"""
    def __init__(self, name: str, item_id: int, buy_price: int, sell_price: int, buff: BeneficialBuff, quest_id: int=0):
        super().__init__(name, item_id, buy_price, sell_price, quest_id)
        self.buff = buff

    def __str__(self):
        return colored(f'{self.name}', color='cyan') + f' - Potion ({self.buff})'

    def get_buff_name(self) -> str:
        return self.buff.name

    def consume(self, character):
        character.add_buff(self.buff)
