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


# the base class for all buffs/dots/debuffs
class StatusEffect:
    def __init__(self, name: str, duration: int):
        self.name = name
        self.duration = duration  # measured in turns

    def __str__(self):
        return "Default Status Effect"


# Standard Buff that increases X stat for Y minutes (in our case: turns)
class BeneficialBuff(StatusEffect):
    # this dictionary will hold the meaningful information of what buff we give
    buff_amounts = {KEY_BUFF_TYPE_ARMOR: 0,
                    KEY_BUFF_TYPE_STRENGTH: 0,
                    KEY_BUFF_TYPE_HEALTH: 0,
                    KEY_BUFF_TYPE_MANA: 0}  # type: dict

    def __init__(self, name: str, buff_stats_and_amounts: list, duration: int):
        """
        Buff(10, [(armor, 3), (None, None), (None, None)) will increase your armor by 10 for 3 turns

        :param amount: the amount we are going to increase by
        :param buff_stats_and_amounts: A list of tuples, each tuple holding (1,2)
            1 - the stat we are going to buff (str) "armor"
            2 - the amount we are going to buff it by (int) 10
        :param duration: How many turns this buff will be active for, type: int
        """
        super().__init__(name, duration)
        self.buff_stats_and_amounts = buff_stats_and_amounts
        self._manage_buff_types(buff_stats_and_amounts)  # updates buff_amounts
        # a list which holds tuples of the buffed attributes (will be used for __str__)
        self.non_empty_buffs = list(filter(lambda kv: kv[1] is not 0, self.buff_amounts.items()))

    def __str__(self):
        """ Depending on the amount of stats it buffs, print out a different message"""
        non_empty_buffs_count = len(self.non_empty_buffs)
        # TODO: refactor
        if non_empty_buffs_count == 1:
            increased_attribute, value = self.non_empty_buffs[0]
            return f'Increases {increased_attribute} by {value} for {self.duration} turns.'
        elif non_empty_buffs_count == 2:
            increased_attribute, value = self.non_empty_buffs[0]
            increased_attribute2, value2 = self.non_empty_buffs[1]
            return f'Increases {increased_attribute} by {value} and {increased_attribute2} by {value2} for {self.duration} turns.'
        elif non_empty_buffs_count == 3:
            increased_attribute, value = self.non_empty_buffs[0]
            increased_attribute2, value2 = self.non_empty_buffs[1]
            increased_attribute3, value3 = self.non_empty_buffs[2]

            return (f"Increases {increased_attribute} by {value}, {increased_attribute2} by {value2}"
                    f" and {increased_attribute3} by {value3} for {self.duration} turns.")
        else:
            return ""

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
                    raise ValueError(f'Buff type {buff_type} is not supported!')

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
class DoT(StatusEffect):

    def __init__(self, name: str, damage_tick: Damage, duration: int, caster_lvl: int):
        """
        Dots(Fireball, 5, 2) will damage you for 5 at the start of each turn for 2 turns.
        :param name:
        :param damage_tick: the damage it will deal to you every turn
        :param duration: How many turns this DoT will be active for
        :param caster_lvl: the level of the caster
        """
        super().__init__(name, duration)
        self.damage = damage_tick  # type: Damage
        self.level = caster_lvl

    def __str__(self):
        return f'{self.name} - Deals {self.damage} damage every turn for {self.duration} turns'

