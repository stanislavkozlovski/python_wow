import random

from damage import Damage
from decorators import cast_spell
from entities import Character, Monster, CHARACTER_DEFAULT_EQUIPMENT
from heal import HolyHeal
from models.spells.loader import load_paladin_spells_for_level
from spells import PaladinSpell


class Paladin(Character):
    """
    Paladin spells:
        Spells every paladin starts with:
            Seal of Righteousness
                Deals X damage on each attack, needs to be activated first
    """
    # TODO: Storing the spells here will be a problem if we ever want to have 2 simultaneous players or
    #       the ability to load another character without exiting the game.
    learned_spells: {str: PaladinSpell} = {}
    SOR_ACTIVE = False  # Seal of Righteousness trigger
    SOR_TURNS = 0  # Holds the remaining turns for SOR
    KEY_FLASH_OF_LIGHT = "Flash of Light"
    KEY_SEAL_OF_RIGHTEOUSNESS = "Seal of Righteousness"
    KEY_MELTING_STRIKE = "Melting Strike"

    def __init__(self, name: str, level: int = 1, health: int = 12, mana: int = 15, strength: int = 4,
                 loaded_scripts: set=set(), killed_monsters: set=set(), completed_quests: set=(),
                 saved_inventory: dict={"gold": 0}, saved_equipment: dict=CHARACTER_DEFAULT_EQUIPMENT):
        super().__init__(name=name, level=level, health=health, mana=mana, strength=strength, loaded_scripts=loaded_scripts,
                         killed_monsters=killed_monsters, completed_quests=completed_quests,
                         saved_inventory=saved_inventory, saved_equipment=saved_equipment)
        # TODO: Equip items AFTER level up
        self.min_damage = 1
        self.max_damage = 3
        self._lookup_and_handle_new_spells()

    def end_turn_update(self):
        super().end_turn_update()
        if self.SOR_TURNS == 0:  # fade spell
            self.SOR_ACTIVE = False
            print(f'{self.KEY_SEAL_OF_RIGHTEOUSNESS} has faded from {self.name}')

    def leave_combat(self):
        super().leave_combat()
        self.SOR_ACTIVE = False  # Remove SOR aura
        self.reset_spell_cooldowns()

    def reset_spell_cooldowns(self):
        """
        Resets the cooldown of every spell
        Typically called when we leave combat
        """
        for spell in self.learned_spells.values():
            spell.reset_cd()

    def _level_up(self, to_level: int=0, to_print: bool=True):
        """
        This method levels the character up, if we're given a to_level we need to level up until we get to that level
        """
        if to_level:
            super()._level_up(to_level=to_level, to_print=to_print)
        else:
            super()._level_up(to_print=to_print)
            self._lookup_and_handle_new_spells()

    def _lookup_and_handle_new_spells(self):
        """
        This method looks up all the new available spells to learn or update their ranks and does so
        accordingly
        """
        for available_spell in self._lookup_available_spells_to_learn(
                self.level):  # generator that returns dictionaries holding spell attributes

            # update spell rank
            if available_spell.name in self.learned_spells:
                self.update_spell(available_spell)
            # learn new spell
            else:
                self.learn_new_spell(spell=available_spell)

    def learn_new_spell(self, spell: PaladinSpell):
        print(f"You have learned a new spell - {spell.name}")

        self.learned_spells[spell.name] = spell

    def _lookup_available_spells_to_learn(self, level: int) -> [PaladinSpell]:
        """
        Generator function yielding from a list of PaladinSpells that the character can learn
        """
        yield from load_paladin_spells_for_level(level)

    def update_spell(self, spell: PaladinSpell):
        spell_name = spell.name
        self.learned_spells[spell_name] = spell
        print(f'Spell {spell.name} has been updated to rank {spell.rank}!')
        print("*" * 20)

    def spell_handler(self, command: str, target: Monster) -> bool:
        """
        :param target: The target the spell is cast on
        :param command: Command telling you which spell to use
        :return: Returns a boolean indicating if the cast was successful or not
        """
        if command == 'sor':
            return self.spell_seal_of_righteousness(self.learned_spells[self.KEY_SEAL_OF_RIGHTEOUSNESS])
        elif command == 'fol':
            return self.spell_flash_of_light(self.learned_spells[self.KEY_FLASH_OF_LIGHT])
        elif command == 'ms':
            return self.spell_melting_strike(spell=self.learned_spells[self.KEY_MELTING_STRIKE], target=target)

        print("Unsuccessful cast")
        return False  # if we do not go into any spell

    @cast_spell
    def spell_seal_of_righteousness(self, spell: PaladinSpell):
        """
         When activated adds DAMAGE1 Spell Damage to each attack
         Lasts for three turns
        :return: boolean indicating if the cast was successful or not
        """
        mana_cost = spell.mana_cost
        self.mana -= mana_cost

        self.SOR_ACTIVE = True
        self.SOR_TURNS = 3
        print(f'{self.name} activates {self.KEY_SEAL_OF_RIGHTEOUSNESS}!')
        return True

    def _spell_seal_of_righteousness_attack(self):
        self.SOR_TURNS -= 1
        return self.learned_spells[self.KEY_SEAL_OF_RIGHTEOUSNESS].damage1  # damage from SOR

    @cast_spell
    def spell_flash_of_light(self, spell):
        """
        Heals the paladin for a certain amount
        :return successful cast or not
        """
        mana_cost = spell.mana_cost
        heal = HolyHeal(heal_amount=spell.heal1)

        self.health += heal
        self.mana -= mana_cost

        if self.health > self.max_health:  # check for overheal
            overheal = self._handle_overheal()
            print(f'{spell.name} healed {self.name} for {heal-overheal:.2f} ({overheal:.2f} Overheal).')
        else:
            print(f'{spell.name} healed {self.name} for {heal}.')

        return True

    @cast_spell
    def spell_melting_strike(self, spell: PaladinSpell, target: Monster):
        """ Damages the enemy for DAMAGE_1 damage and puts a DoT effect, the index of which is EFFECT
        :return successful cast or not"""
        mana_cost: int = spell.mana_cost
        damage: Damage = Damage(phys_dmg=spell.damage1)
        dot: 'DoT' = spell.harmful_effect
        dot.update_caster_level(self.level)

        self.mana -= mana_cost
        # damage the target and add the DoT
        print(f'{spell.name} damages {target.name} for {damage}!')
        target.take_attack(damage, self.level)
        target.add_buff(dot)

        return True

    # SPELLS

    def get_auto_attack_damage(self, target_level: int) -> (Damage, int):
        level_difference = self.level - target_level
        percentage_mod = (abs(level_difference) * 0.1)  # calculates by how many % we're going to increase/decrease dmg

        sor_damage = 0
        damage_to_deal = random.randint(int(self.min_damage), int(self.max_damage) + 1)

        if self.SOR_ACTIVE:
            sor_damage = self._spell_seal_of_righteousness_attack()

        # 10% more or less damage for each level that differs
        if level_difference < 0:  # monster is bigger level
            damage_to_deal -= damage_to_deal * percentage_mod  # -X%
            sor_damage -= sor_damage * percentage_mod
        elif level_difference > 0:  # character is bigger level
            damage_to_deal += damage_to_deal * percentage_mod  # +X%
            sor_damage += sor_damage * percentage_mod

        return Damage(phys_dmg=damage_to_deal, magic_dmg=sor_damage), sor_damage

    def attack(self, victim: Monster):
        attacker_swing: (Damage, int) = self.get_auto_attack_damage(victim.level)

        auto_attack: Damage = attacker_swing[0]  # type: Damage
        # the sor_damage below is used just to check for printing
        sor_damage: int = attacker_swing[1]  # if the seal isn't active the damage will be 0

        auto_attack_print = victim.get_take_attack_damage_repr(auto_attack, self.level)
        if sor_damage:
            print(f'{self.name} attacks {victim.name} for {auto_attack_print} from {self.KEY_SEAL_OF_RIGHTEOUSNESS}!')
        else:
            print(f'{self.name} attacks {victim.name} for {auto_attack_print}!')

        victim.take_attack(auto_attack, self.level)

    def get_class(self):
        """
        Return the class name in lowercase.
        Ex: paladin
        """
        return self.__class__.__name__.lower()
