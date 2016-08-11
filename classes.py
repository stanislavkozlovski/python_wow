from entities import Character, Monster


class Paladin(Character):
    """
    Paladin spells:
        Spells every paladin starts with:
            Seal of Righteousness
                Deals X damage on each attack, needs to be activated first
    """
    SOR_ACTIVE = False  # Seal of Righteousness trigger
    SOR_TURNS = 0  # Holds the remaining turns for SOR
    SOR_DAMAGE = 2  # Holds the damage SOR will deal each auto attack. TODO: Load from DB
    SOR_RANK = 1  # Holds the RANK of SOR

    def __init__(self, name: str, health: int=12, mana: int=15, strength: int=4):
        super().__init__(name=name, health=health, mana=mana, strength=strength)
        self.min_damage = 1
        self.max_damage = 3

    def leave_combat(self):
        super().leave_combat()
        self.SOR_ACTIVE = False  # Remove SOR aura

    # SPELLS
    def spell_handler(self, command: str):
        if command == 'sor':
            self.spell_seal_of_righteousness()

    def spell_seal_of_righteousness(self):
        #  When activated adds X Spell Damage to each attack
        #  Lasts for three turns
        self.SOR_ACTIVE = True
        self.SOR_TURNS = 3
        print("{0} activates Seal of Righteousness!".format(self.name))

    def _spell_seal_of_righteousness_attack(self):
        if self.SOR_TURNS == 0: # fade spell
            self.SOR_ACTIVE = False
            print("Seal of Righteousness has faded from {}".format(self.name))
            return 0
        else:
            self.SOR_TURNS -= 1
            # TODO: Load damage from DB
            return self.SOR_DAMAGE  # damage from SOR

    # SPELLS

    def deal_damage(self, target_level: int):
        import random

        level_difference = self.level - target_level
        percentage_mod = (
        abs(level_difference) * 0.1)  # calculates by how many % we're going to increase/decrease dmg

        sor_damage = 0
        damage_to_deal = random.randint(int(self.min_damage), int(self.max_damage) + 1)

        if self.SOR_ACTIVE:
            sor_damage = self._spell_seal_of_righteousness_attack()

        # 10% more or less damage for each level that differs
        if level_difference == 0:
            pass
        elif level_difference < 0:  # monster is bigger level
            damage_to_deal -= damage_to_deal * percentage_mod  # -X%
            sor_damage -= sor_damage * percentage_mod
        elif level_difference > 0:  # character is bigger level
            damage_to_deal += damage_to_deal * percentage_mod  # +X%
            sor_damage += sor_damage * percentage_mod

        return damage_to_deal, sor_damage

    def attack(self, victim: Monster):
        attacker_swing = self.deal_damage(victim.level)  # tuple holding auto attack and seal damage (if active)

        auto_attack = attacker_swing[0]
        sor_damage = attacker_swing[1]  # if the seal isn't active the damage will be 0

        if sor_damage:
            print("{0} attacks {1} for {2:.2f} + {3:.2f} from Seal of Righteousness!".format(self.name, victim.name, auto_attack, sor_damage))
        else:
            print("{0} attacks {1} for {2:.2f} damage!".format(self.name, victim.name, auto_attack))

        victim.take_attack(auto_attack + sor_damage)

    def get_class(self):
        return 'paladin'