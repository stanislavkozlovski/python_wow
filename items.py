"""
This holds the classes for every kind of item in the game
"""
from buffs import BeneficialBuff
from termcolor import colored

KEY_BONUS_HEALTH = 'bonus_health'  # TODO: Move these constants to a constants.py module
KEY_BONUS_MANA = 'bonus_mana'
KEY_STRENGTH = 'strength'
KEY_ARMOR = 'armor'
KEY_AGILITY = 'agility'


def create_attributes_dict(bonus_health: int=0, bonus_mana: int=0, armor: int=0, strength: int=0,
                           agility: int=0) -> dict:
    """
    This function takes in stats (attributes) like bonus_health, strength, armor, etc and converts them into a
    pre-defined dictionary holding all of them. This enables easier passing and application of said attributes
    :return: a dict like {"strength": 10, "armor": 4}
    """

    return {KEY_BONUS_HEALTH: bonus_health, KEY_BONUS_MANA: bonus_mana,
            KEY_ARMOR: armor, KEY_STRENGTH: strength, KEY_AGILITY: agility}


def display_attributes(attributes: dict) -> str:
    """
    This function read a dictionary with attributes and returns a string displaying the attributes it gives.
    A template: {armor} {health} {mana} {strength} {agility}
    If any are missing, we don't add them
    """
    attributes_to_print = []

    if attributes[KEY_ARMOR]:
        attributes_to_print.append(f'armor: {attributes[KEY_ARMOR]}')
    if attributes[KEY_BONUS_HEALTH]:
        attributes_to_print.append(f'health: {attributes[KEY_BONUS_HEALTH]}')
    if attributes[KEY_BONUS_MANA]:
        attributes_to_print.append(f'mana: {attributes[KEY_BONUS_MANA]}')
    if attributes[KEY_STRENGTH]:
        attributes_to_print.append(f'strength: {attributes[KEY_STRENGTH]}')
    if attributes[KEY_AGILITY]:
        attributes_to_print.append(f'agility: {attributes[KEY_AGILITY]}')

    return ", ".join(attributes_to_print)


class Item:
    def __init__(self, name: str, item_id: int, buy_price: int, sell_price: int, quest_ID: int=0):
        self.name = name
        self.id = item_id
        self.buy_price = buy_price
        self.sell_price = sell_price
        self.quest_ID = quest_ID

    def __str__(self):
        return colored(f'{self.name}', color="grey") + ' - Miscellaneous Item'


class Weapon(Item):
    def __init__(self, name: str, item_id: int, buy_price: int = 0, sell_price: int = 0, min_damage: int = 0,
                 max_damage: int = 1, attributes_dict: dict=create_attributes_dict()):
        super().__init__(name, item_id, buy_price, sell_price)
        self.min_damage = min_damage
        self.max_damage = max_damage
        self.attributes = attributes_dict  # the attributes this item gives on equip

    def __str__(self):
        return colored(f'{self.name}', color="green") + f'- Weapon ({self.min_damage}-{self.max_damage}) damage'


class Equipment(Item):
    """ Any item that can be equipped in an equipment slot, as distinguished from items that can only be
    carried in the inventory.
    ex: Headpiece, Shoulderpad, Necklace, Chestguard, Bracer, Gloves, Belt, Leggings, Boots"""
    def __init__(self, name: str, item_id: int, slot: str, attributes_dict: dict=create_attributes_dict(), buy_price: int=0, sell_price: int=0):
        super().__init__(name, item_id, buy_price, sell_price)
        self.slot = slot
        self.attributes = attributes_dict

    def __str__(self):
        return (colored(self.name, color='green')
                + ' - {slot_pos} Equipment: '.format(slot_pos=self.slot[0].upper() + self.slot[1:])
                + display_attributes(self.attributes))


class Potion(Item):
    """ Consumable item that gives a buff to the player"""
    def __init__(self, name: str, item_id: int, buy_price: int, sell_price: int, buff: BeneficialBuff, quest_ID: int=0, ):
        super().__init__(name, item_id, buy_price, sell_price, quest_ID)
        self.buff = buff

    def __str__(self):
        return colored(f'{self.name}', color='cyan') + f' - Potion ({self.buff})'

    def get_buff_name(self) -> str:
        return self.buff.name

    def consume(self, character):
        character.add_buff(self.buff)
