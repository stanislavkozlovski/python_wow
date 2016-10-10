"""
This module will hold the damage class in the game.
"""


class Damage:
    """ This class holds the damage of every character/monster in the game"""
    def __init__(self, phys_dmg: float=0, magic_dmg: float=0):
        self.phys_dmg = round(phys_dmg, 1)
        self.magic_dmg = round(magic_dmg, 1)
        self.phys_absorbed, self.magic_absorbed = 0, 0

    def __str__(self):
        """
        Have two separate strings for physical damage and magical damage.
        Fill them if we have such damages and modify them if there is absorption
        Then, return what's appropriate
        """
        phys_dmg_print = ""
        if self.phys_dmg:
            phys_dmg_print = "{phys_dmg:.2f} physical damage".format(phys_dmg=self.phys_dmg)

        if self.phys_absorbed:
            phys_dmg_print = "{phys_dmg:.2f} physical damage ({absorbed:.2f} absorbed)".format(phys_dmg=self.phys_dmg,
                                                                                       absorbed=self.phys_absorbed)


        magic_dmg_print = ""
        if self.magic_dmg:
            magic_dmg_print = "{magic_dmg:.2f} magical damage".format(magic_dmg=self.magic_dmg)

        if self.magic_absorbed:
            magic_dmg_print = "{magic_dmg:.2f} magical damage ({absorbed:.2f} absorbed)".format(magic_dmg=self.magic_dmg,
                                                                                        absorbed=self.magic_absorbed)

        if phys_dmg_print and magic_dmg_print:
            return "{phys:.2f} and {magic:.2f}".format(phys=phys_dmg_print, magic=magic_dmg_print)
        elif phys_dmg_print:
            return phys_dmg_print
        elif magic_dmg_print:
            return magic_dmg_print
        else:
            return "0 damage"

    def __sub__(self, other):
        return (self.phys_dmg + self.magic_dmg) - other

    def __rsub__(self, other):
        return other - (self.phys_dmg + self.magic_dmg)

    def __isub__(self, other: tuple):
        other_phys, other_magic = 0, 0  # type: int
        # unpack other damage
        if isinstance(other, tuple):
            other_phys, other_magic = other
        elif isinstance(other, Damage):
            other_phys = other.phys_dmg
            other_magic = other.magic_dmg

        # does not let the numbers get negative
        modified_phys_damage = max(self.phys_dmg - other_phys, 0)
        modified_magic_damage = max(self.magic_dmg - other_magic, 0)

        return Damage(phys_dmg=modified_phys_damage,
                      magic_dmg=modified_magic_damage)

    def __iadd__(self, other: tuple):
        other_phys, other_magic = 0, 0  # type: int
        # unpack other damage
        if isinstance(other, tuple):
            other_phys, other_magic = other
        elif isinstance(other, Damage):
            other_phys = other.phys_dmg
            other_magic = other.magic_dmg

        return Damage(phys_dmg=self.phys_dmg + other_phys,
                      magic_dmg=self.magic_dmg + other_magic)

    def __mul__(self, other: float):
        return Damage(phys_dmg=(other * self.phys_dmg),
                      magic_dmg=(other * self.magic_dmg))

    def handle_absorption(self, absorption_shield: float):
        """
        This method subtracts the absorbed damage from our damage
        The magical damage always gets absorbed first!
        :param absorption_shield: a float indicating how much damage should get absorbed
        :return: What's left of the absorption
        """

        # subtract magic damage
        if absorption_shield >= self.magic_dmg:
            # shield is bigger
            absorption_shield -= self.magic_dmg
            self.magic_absorbed = self.magic_dmg
            self.magic_dmg = 0

            # subtract physical damage
            if absorption_shield >= self.phys_dmg:
                # shield is bigger
                absorption_shield -= self.phys_dmg
                self.phys_absorbed = self.phys_dmg
                self.phys_dmg = 0
            else:
                #shield is smaller
                self.phys_dmg -= absorption_shield
                self.phys_absorbed = absorption_shield
                absorption_shield = 0
        else:
            # shield is smaller than magic_dmg, we won't get to absorb phys at all
            self.magic_dmg -= absorption_shield
            self.magic_absorbed = absorption_shield
            absorption_shield = 0

        return absorption_shield
