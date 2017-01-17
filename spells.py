

# The base class for spells
class Spell:
    def __init__(self, name: str, rank: int, mana_cost: int=0, cooldown: int=0, beneficial_effect: 'BeneficialBuff'=None,
                 harmful_effect: 'DoT'=None):
        self.name = name
        self.mana_cost = mana_cost
        self.rank = rank
        self.cooldown = cooldown
        self._cooldown_counter = 0
        self.is_ready = True  # boolean indicating if the spell is ready to be cast
        self.beneficial_effect = beneficial_effect
        self.harmful_effect = harmful_effect

    def __repr__(self):
        return f'Spell Object {self.name}: {self.mana_cost} Mana, {self._cooldown_counter}/{self.cooldown} CD.'

    @property
    def turns_on_cd(self):
        """ Returns the turns this spell has left to cooldown """
        return self._cooldown_counter

    def reset_cd(self):
        """
        Resets the spell's cooldown
        """
        self._cooldown_counter = 0

    def cast(self) -> int:
        """
        Cast the spell, starting the cooldown counter and returning its mana cost
        """
        if not self.is_ready:
            # TODO
            return False
        self._cooldown_counter = self.cooldown
        self.is_ready = False

        return True

    def pass_turn(self):
        """
        Decrement the cooldown counter
        :return:
        """
        if self._cooldown_counter != 0:
            self._cooldown_counter -= 1
        else:
            self.is_ready = True


class PaladinSpell(Spell):
    def __init__(self, name: str, rank: int, damage1: int=0, damage2: int=0, damage3: int=0, heal1: int=0, heal2: int=0,
                 heal3: int=0, mana_cost: int=0, cooldown: int=0, beneficial_effect: 'BeneficialBuff' = None,
                 harmful_effect: 'DoT' = None):
        super().__init__(name, rank, mana_cost, cooldown, beneficial_effect, harmful_effect)
        self.damage1 = damage1
        self.damage2 = damage2
        self.damage3 = damage3
        self.heal1 = heal1
        self.heal2 = heal2
        self.heal3 = heal3

    def __repr__(self):
        return (f'Paladin Spell Object {self.name}: {self.mana_cost} Mana, {self._cooldown_counter}/{self.cooldown} CD.'
                f'\nDamage values: {self.damage1} | {self.damage2} | {self.damage3} '
<<<<<<< HEAD
                f'\nHeal values: {self.heal1} | {self.heal2} | {self.heal3}')
=======
                f'\nHeal values: {self.heal1} | {self.heal2} | {self.heal3}')
>>>>>>> parent of a523c24... Revert "Merged branch feature/SQLAlchemy into master"
