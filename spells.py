

# The base class for spells
class Spell:
    def __init__(self, name: str, mana_cost: int=0, cooldown: int=0, beneficial_effect: 'BeneficialBuff'=None,
                 harmful_effect: 'DoT'=None):
        self.name = name
        self.mana_cost = mana_cost
        self.cooldown = cooldown
        self._cooldown_counter = 0
        self.is_ready = True  # boolean indicating if the spell is ready to be cast
        self.beneficial_effect = beneficial_effect
        self.harmful_effect = harmful_effect

    def __repr__(self):
        return f'Spell Object {self.name}: {self.mana_cost} Mana, {self._cooldown_counter}/{self.cooldown} CD.'

    def cast(self, caster, target) -> int:
        """
        Cast the spell, starting the cooldown counter and returning its mana cost
        """
        if not (self._cooldown_counter == 0 and caster.has_enough_mana(self.mana_cost)):
            # TODO
            return
        self._cooldown_counter = self.cooldown
        self.is_ready = False

        return self.mana_cost

    def pass_turn(self):
        """
        Decrement the cooldown counter
        :return:
        """
        if self._cooldown_counter != 0:
            self._cooldown_counter -= 1
        else:
            self.is_ready = True
