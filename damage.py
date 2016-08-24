"""
This module will hold the damage class in the game.
"""


class Damage:
    """ This class holds the damage of every character/monster in the game"""
    def __init__(self, phys_dmg: float=0, magic_dmg: float=0):
        self.phys_dmg = round(phys_dmg, 1)
        self.magic_dmg = round(magic_dmg, 1)

    def __str__(self):
        if self.phys_dmg and self.magic_dmg:
            return "{phys_dmg} physical and {magic_dmg} magical damage".format(phys_dmg=self.phys_dmg,
                                                                              magic_dmg=self.magic_dmg)
        elif self.phys_dmg:
            return "{phys_dmg} physical damage".format(phys_dmg=self.phys_dmg)
        elif self.magic_dmg:
            return "{magic_dmg} magical damage".format(magic_dmg=self.magic_dmg)
        else:
            return "0 damage"

    def __sub__(self, other):
        return (self.phys_dmg + self.magic_dmg) - other

    def __rsub__(self, other):
        return other - (self.phys_dmg + self.magic_dmg)