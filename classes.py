import sqlite3

from database.main import cursor
from damage import Damage
from database.database_info import (
    DB_PATH,
    DBINDEX_PALADIN_SPELLS_TEMPLATE_NAME, DBINDEX_PALADIN_SPELLS_TEMPLATE_RANK,
    DBINDEX_PALADIN_SPELLS_TEMPLATE_LEVEL_REQUIRED, DBINDEX_PALADIN_SPELLS_TEMPLATE_DAMAGE1,
    DBINDEX_PALADIN_SPELLS_TEMPLATE_DAMAGE2, DBINDEX_PALADIN_SPELLS_TEMPLATE_DAMAGE3,
    DBINDEX_PALADIN_SPELLS_TEMPLATE_HEAL1, DBINDEX_PALADIN_SPELLS_TEMPLATE_HEAL2,
    DBINDEX_PALADIN_SPELLS_TEMPLATE_HEAL3, DBINDEX_PALADIN_SPELLS_TEMPLATE_MANA_COST,
    DBINDEX_PALADIN_SPELLS_TEMPLATE_EFFECT, DBINDEX_PALADIN_SPELLS_TEMPLATE_COOLDOWN)
from entities import Character, Monster, CHARACTER_DEFAULT_EQUIPMENT
from heal import HolyHeal
from spells import PaladinSpell

from loader import load_dot


class Paladin(Character):
    """
    Paladin spells:
        Spells every paladin starts with:
            Seal of Righteousness
                Deals X damage on each attack, needs to be activated first
    """
    learned_spells = {}
    SOR_ACTIVE = False  # Seal of Righteousness trigger
    SOR_TURNS = 0  # Holds the remaining turns for SOR
    KEY_FLASH_OF_LIGHT = "Flash of Light"
    KEY_SEAL_OF_RIGHTEOUSNESS = "Seal of Righteousness"
    KEY_MELTING_STRIKE = "Melting Strike"

    def __init__(self, name: str, level: int = 1, health: int = 12, mana: int = 15, strength: int = 4,
                 loaded_scripts: set=set(), killed_monsters: set=set(), completed_quests: set=(),
                 saved_inventory: dict={"gold": 0}, saved_equipment: dict=CHARACTER_DEFAULT_EQUIPMENT):
        super().__init__(name=name, health=health, mana=mana, strength=strength, loaded_scripts=loaded_scripts,
                         killed_monsters=killed_monsters, completed_quests=completed_quests,
                         saved_inventory=saved_inventory, saved_equipment=saved_equipment)
        self.min_damage = 1
        self.max_damage = 3
        self._lookup_and_handle_new_spells()

        if level > 1: self._level_up(to_level=level)

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

    def _level_up(self, to_level: int=0):
        """ This method levels the character up, if we're given a to_level we need to level up until we get to that level"""
        if to_level:
            # level up multiple times
            for i in range(self.level, to_level):
                self._level_up()
            self.xp_req_to_level = self._lookup_next_xp_level_req()
        else:
            # level up once
            super()._level_up()
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

    def learn_new_spell(self, spell: dict):
        print(f"You have learned a new spell - {spell.name}")

        self.learned_spells[spell.name] = spell


    def _lookup_available_spells_to_learn(self, level: int) -> PaladinSpell:
        """
        Generator function
            paladin_spells_template table is as follows:
            ID, Name of Spell, Rank of Spell, Level Required for said Rank, Damage1, Damage2, Damage3, Heal1, Heal2, Heal3, Effect, Cooldown, Comment
            1,Seal of Righteousness,       1,                            1,       2,       0,       0,     0,     0,     0,      0,        0,Seal of Righteousness
            effect is a special effect according to the spell, only Melting Strike has one for now and it serves as the
            entry in spell_dots
            cooldown is the amount of turns it takes for this spell to be ready again after being cast
            :return: A dictionary holding keys for each row (rank, damage1, damage2 etc.)
        """

        with sqlite3.connect(DB_PATH) as connection:
            cursor = connection.cursor()
            # this will return a list of tuples holding information about each spell we have the req level to learn
            spell_reader = cursor.execute("SELECT * FROM paladin_spells_template WHERE level_required = ?", [level])

            for line in spell_reader:
                name = line[DBINDEX_PALADIN_SPELLS_TEMPLATE_NAME]
                rank = line[DBINDEX_PALADIN_SPELLS_TEMPLATE_RANK]  # type: int
                level_req = line[DBINDEX_PALADIN_SPELLS_TEMPLATE_LEVEL_REQUIRED]  # type: int
                damage_1 = line[DBINDEX_PALADIN_SPELLS_TEMPLATE_DAMAGE1]  # type: int
                damage_2 = line[DBINDEX_PALADIN_SPELLS_TEMPLATE_DAMAGE2]  # type: int
                damage_3 = line[DBINDEX_PALADIN_SPELLS_TEMPLATE_DAMAGE3]  # type: int
                heal_1 = line[DBINDEX_PALADIN_SPELLS_TEMPLATE_HEAL1]  # type: int
                heal_2 = line[DBINDEX_PALADIN_SPELLS_TEMPLATE_HEAL2]  # type: int
                heal_3 = line[DBINDEX_PALADIN_SPELLS_TEMPLATE_HEAL3]  # type: int
                mana_cost = line[DBINDEX_PALADIN_SPELLS_TEMPLATE_MANA_COST]  # type: int
                beneficial_effect = line[11]  # type: int
                harmful_effect = line[12]
                cooldown = line[13]  # type: int
                cooldown = cooldown if cooldown else 0  # if we get a None, we turn it into 0
                yield PaladinSpell(name=name, rank=rank, mana_cost=mana_cost, beneficial_effect=beneficial_effect,
                                   harmful_effect=harmful_effect, damage1=damage_1, damage2=damage_2, damage3=damage_3,
                                   heal1=heal_1, heal2=heal_2, heal3=heal_3, cooldown=cooldown)

    def update_spell(self, spell: dict):
        spell_name = spell.name
        self.learned_spells[spell_name] = spell
        print(f'Spell {spell.name} has been updated to rank {spell.rank}!')
        print("*" * 20)

    def spell_handler(self, command: str, target: Monster) -> bool:
        """

        :param command: Command telling you which spell to use
        :return: Returns a boolean indicating if the cast was successful or not
        """
        if command == 'sor':
            return self.spell_seal_of_righteousness()
        elif command == 'fol':
            return self.spell_flash_of_light()
        elif command == 'ms':
            return self.spell_melting_strike(target=target)

        print("Unsuccessful cast")
        return False  # if we do not go into any spell

    def spell_seal_of_righteousness(self):
        """
         When activated adds DAMAGE1 Spell Damage to each attack
         Lasts for three turns
        :return: boolean indicating if the cast was successful or not
        """
        spell = self.learned_spells[self.KEY_SEAL_OF_RIGHTEOUSNESS]
        mana_cost = spell.mana_cost
        if not self.has_enough_mana(mana_cost):
            print(f'Not enough mana! {spell.name} requires {mana_cost} but you have {self.mana}!')
            return False
        # proceed with casting the spell and start its cooldown timer
        is_ready = spell.cast()
        if not is_ready:
            print(f'{spell.name} is still on cooldown!')
            return False

        self.mana -= mana_cost
        # self._spell_trigger_cd(self.KEY_SEAL_OF_RIGHTEOSNESS)
        self.SOR_ACTIVE = True
        self.SOR_TURNS = 3
        print(f'{self.name} activates {self.KEY_SEAL_OF_RIGHTEOUSNESS}!')
        return True

    def _spell_seal_of_righteousness_attack(self):
        if self.SOR_TURNS == 0:  # fade spell
            self.SOR_ACTIVE = False
            print(f'{self.KEY_SEAL_OF_RIGHTEOUSNESS} has faded from {self.name}')
            return 0
        else:
            self.SOR_TURNS -= 1
            return self.learned_spells[self.KEY_SEAL_OF_RIGHTEOUSNESS].damage1  # damage from SOR

    def spell_flash_of_light(self):
        """
        Heals the paladin for a certain amount
        :return successful cast or not
        """
        spell = self.learned_spells[self.KEY_FLASH_OF_LIGHT]
        mana_cost = spell.mana_cost
        if not self.has_enough_mana(mana_cost):
            print(f'Not enough mana! {spell.name} requires {mana_cost} but you have {self.mana}!')
            return False
        # proceed with casting the spell and start its cooldown timer
        is_ready = spell.cast()
        if not is_ready:
            print(f'{spell.name} is still on cooldown!')
            return False
        heal = HolyHeal(heal_amount=spell.heal1)

        self.health += heal  # TODO: Handle overheal otherwhere... is it not handled btw?
        self.mana -= mana_cost
        # self._spell_trigger_cd(self.KEY_FLASH_OF_LIGHT)

        if self.health > self.max_health:  # check for overheal
            overheal = self._handle_overheal()
            print(f'{self.KEY_FLASH_OF_LIGHT} healed {self.name} for {heal-overheal:.2f} ({overheal:.2f} Overheal).')
        else:
            print(f'{self.KEY_FLASH_OF_LIGHT} healed {self.name} for {heal}.')

        return True

    def spell_melting_strike(self, target: Monster):
        """ Damages the enemy for DAMAGE_1 damage and puts a DoT effect, the index of which is EFFECT
        :return successful cast or not"""
        spell = self.learned_spells[self.KEY_MELTING_STRIKE]
        mana_cost = spell.mana_cost
        if not self.has_enough_mana(mana_cost):
            print(f'Not enough mana! {spell.name} requires {mana_cost} but you have {self.mana}!')
            return False
        # proceed with casting the spell and start its cooldown timer
        is_ready = spell.cast()
        if not is_ready:
            print(f'{spell.name} is on cooldown for {spell.turns_on_cd} more turns!')
            return False
        damage = Damage(phys_dmg=spell.damage1)
        dot = load_dot(spell.harmful_effect, level=self.level, cursor=cursor)

        self.mana -= mana_cost
        # damage the target and add the DoT
        print(f'{self.KEY_MELTING_STRIKE} damages {target.name} for {damage}!')
        target.take_attack(damage, self.level)
        target.add_buff(dot)

        return True

    # SPELLS

    def get_auto_attack_damage(self, target_level: int) -> tuple:
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

        return Damage(phys_dmg=damage_to_deal, magic_dmg=sor_damage), sor_damage

    def attack(self, victim: Monster):
        attacker_swing = self.get_auto_attack_damage(
            victim.level)  # tuple holding Damage object and seal damage (if active)

        auto_attack = attacker_swing[0]  # type: Damage
        # the sor_damage below is used just to check for printing
        sor_damage = attacker_swing[1]  # if the seal isn't active the damage will be 0

        auto_attack_print = victim.get_take_attack_damage(auto_attack, self.level)
        if sor_damage:
            print(f'{self.name} attacks {victim.name} for {auto_attack_print} from {self.KEY_SEAL_OF_RIGHTEOUSNESS}!')
        else:
            print(f'{self.name} attacks {victim.name} for {auto_attack_print}!')

        victim.take_attack(auto_attack, self.level)

    def has_enough_mana(self, mana_cost: int) -> bool:
        """
        Check if we have enough mana to cast the spell we want to cast and return the result.
        """
        return self.mana >= mana_cost


    def get_class(self):
        return 'paladin'
