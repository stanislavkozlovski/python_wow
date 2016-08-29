"""
This module will hold the Heal class in the game.
The heal class holds information about the type of heal we have
"""


class Heal:
    def __init__(self, heal_amount: float=0):
        self.heal_amount = heal_amount

    def __str__(self):
        return "{0:.2f}".format(self.heal_amount)

    def __add__(self, other):
        return other + self.heal_amount

    def __radd__(self, other):
        return other + self.heal_amount

    def __iadd__(self, other: float) -> float:
        return other + self.heal_amount

    def __sub__(self, other: float) -> float:
        return self.heal_amount - other

    def __isub__(self, other: float) -> float:
        return self.heal_amount - other

    def __rsub__(self, other: float) -> float:
        return other - self.heal_amount


class NatureHeal(Heal):
    """
    The idea with nature heal is that every such heal leaves off a HoT (healing over time effect) for a % of the main heal
    """
    pass # TODO: IMPLEMENT


class HolyHeal(Heal):
    """
    The idea with holy heal is that every such heal has a significant chance to heal for double it's original amount.
    """
    pass # TODO: IMPLEMENT


class ProtectiveHeal(Heal):
    """
    The idea with protective heal is that every such heal leaves off a slight absorption shield on the target, absorbing
    a % of the original heal.
    """
    pass # TODO: IMPLEMENT
