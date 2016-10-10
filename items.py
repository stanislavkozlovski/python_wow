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


class Item:
    def __init__(self, name: str, item_id: int, buy_price: int, sell_price: int, quest_ID: int=0):
        self.name = name
        self.id = item_id
        self.buy_price = buy_price
        self.sell_price = sell_price
        self.quest_ID = quest_ID

    def __str__(self):
        return colored("{}".format(self.name), color="grey") + " - Miscellaneous Item"


class Weapon(Item):
    def __init__(self, name: str, item_id: int, buy_price: int = 0, sell_price: int = 0, min_damage: int = 0, max_damage: int = 1):
        super().__init__(name, item_id, buy_price, sell_price)
        self.min_damage = min_damage
        self.max_damage = max_damage

    def __str__(self):
        return colored("{}".format(self.name), color="green") +  "- Weapon ({}-{}) damage".format(self.min_damage,
                                                                                                  self.max_damage)


class Potion(Item):
    """ Consumable item that gives a buff to the player"""
    def __init__(self, name: str, item_id: int, buy_price: int, sell_price: int, buff: BeneficialBuff, quest_ID: int=0, ):
        super().__init__(name, item_id, buy_price, sell_price, quest_ID)
        self.buff = buff

    def __str__(self):
        return colored("{}".format(self.name), color="cyan") + " - Potion ({})".format(self.buff)

    def get_buff_name(self) -> str:
        return self.buff.name

    def consume(self, character):
        character.add_buff(self.buff)