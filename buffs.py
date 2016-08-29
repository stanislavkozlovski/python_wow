"""
This module holds information about all kinds of buffs that are applied to an entity
- buffs
- debuffs
- DoTs
etc
"""
from damage import Damage
KEY_BUFF_TYPE_ARMOR = "armor"
KEY_BUFF_TYPE_STRENGTH = "strength"
KEY_BUFF_TYPE_HEALTH = "health"
KEY_BUFF_TYPE_MANA = "mana"


# Standard Buff that increases X stat for Y minutes (in our case: turns)
class Buff:
    # this dictionary will hold the meaningful information of what buff we give
    buff_amounts = {KEY_BUFF_TYPE_ARMOR: 0,
                    KEY_BUFF_TYPE_STRENGTH: 0,
                    KEY_BUFF_TYPE_HEALTH: 0,
                    KEY_BUFF_TYPE_MANA: 0}  # type: dict

    def __init__(self, name: str, buff_stats_and_amounts: list, duration: int, description: str):
        """
        Buff(10, [(armor, 3), (None, None), (None, None)) will increase your armor by 10 for 3 turns

        :param amount: the amount we are going to increase by
        :param buff_stats_and_amounts: A list of tuples, each tuple holding (1,2)
            1 - the stat we are going to buff (str) "armor"
            2 - the amount we are going to buff it by (int) 10
        :param duration: How many turns this buff will be active for, type: int
        """
        self.name = name
        self.buff_stats_and_amounts = buff_stats_and_amounts
        self.duration = duration  # measured in turns
        self.description = description
        self._manage_buff_types(buff_stats_and_amounts)  # updates buff_amounts

    def __str__(self):
        return self.description

    def _manage_buff_types(self, buff_list: list):
        """
        Iterate through the list of tuples and add each buff to our buff_amounts dictionary
        :param buff_list: A list of tuples, each tuple holding the stat we are going to buff and the amount
        """
        for buff_type, buff_amount in buff_list:
            # check if it's a valid buff (we could have a buff with only one stat increase and the others would be null)
            if buff_type and buff_amount:
                if buff_type in self.buff_amounts.keys():
                    self.buff_amounts[buff_type] = buff_amount
                else:
                    raise ValueError("Buff type {} is not supported!".format(buff_type))

    def get_buffed_attributes(self) -> dict:
        """
        Return a dictionary
            Key: buff_type (str)
            Value: buff_amount (int)
        Only filled with the buffs that are increased
        """
        buffed_attributes = {}  # type: dict

        for buff_type, buff_amount in self.buff_amounts.items():
            if buff_amount:
                buffed_attributes[buff_type] = buff_amount

        return  buffed_attributes


# Damage over time debuff
class DoT:

    def __init__(self, name: str, damage_tick: Damage, duration: int, caster_lvl: int):
        """
        Dots(Fireball, 5, 2) will damage you for 5 at the start of each turn for 2 turns.
        :param name:
        :param damage_tick: the damage it will deal to you every turn
        :param duration: How many turns this DoT will be active for
        :param caster_lvl: the level of the caster
        """
        self.name = name
        self.damage = damage_tick  # type: Damage
        self.duration = duration
        self.level = caster_lvl

    def __str__(self):
        return "{} - Deals {} damage every turn for {} turns".format(self.name, self.damage, self.duration)

