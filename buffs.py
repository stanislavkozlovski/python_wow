"""
This module holds information about all kinds of buffs that are applied to an entity
- buffs
- debuffs
- DoTs
etc
"""
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

    def __init__(self, name: str, amount: int, buff_type: str, duration: int):
        """
        Buff(10, armor, 3) will increase your armor by 10 for 3 turns

        :param amount: the amount we are going to increase by
        :param buff_type: a string, holding the name of the stat we are going to increase
        :param duration: How many turns this buff will be active for, type: int
        """
        self.name = name
        self.amount = amount
        self.duration = duration  # measured in turns
        self.manage_buff_type(buff_type)  # updates buff_amounts

    def manage_buff_type(self, buff_type: str):
        """ Update the amount in our buff_amounts dictionary according to the type of buff we're given"""
        if buff_type in self.buff_amounts.keys():
            self.buff_amounts[buff_type] = self.amount
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

