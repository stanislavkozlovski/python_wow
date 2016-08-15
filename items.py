"""
This holds the classes for every kind of item in the game
"""


class Weapon:
    def __init__(self, min_damage: int = 0, max_damage: int = 1):
        self.min_damage = min_damage
        self.max_damage = max_damage
