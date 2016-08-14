import sqlite3

from entities import Character, Monster
from database_info import (
    DB_PATH,
    DBINDEX_PALADIN_SPELLS_TEMPLATE_NAME, DBINDEX_PALADIN_SPELLS_TEMPLATE_RANK,
    DBINDEX_PALADIN_SPELLS_TEMPLATE_LEVEL_REQUIRED, DBINDEX_PALADIN_SPELLS_TEMPLATE_DAMAGE1,
    DBINDEX_PALADIN_SPELLS_TEMPLATE_DAMAGE2, DBINDEX_PALADIN_SPELLS_TEMPLATE_DAMAGE3,
    DBINDEX_PALADIN_SPELLS_TEMPLATE_HEAL1, DBINDEX_PALADIN_SPELLS_TEMPLATE_HEAL2,
    DBINDEX_PALADIN_SPELLS_TEMPLATE_HEAL3, DBINDEX_PALADIN_SPELLS_TEMPLATE_MANA_COST)


class Paladin(Character):
    """
    Paladin spells:
        Spells every paladin starts with:
            Seal of Righteousness
                Deals X damage on each attack, needs to be activated first
    """
    learned_spells = {"Seal of Righteousness": {"damage_on_swing": 2, "mana_cost": 4, "rank": 1}
                      }
    SOR_ACTIVE = False  # Seal of Righteousness trigger
    SOR_TURNS = 0  # Holds the remaining turns for SOR

    def __init__(self, name: str, health: int=12, mana: int=15, strength: int=4):
        super().__init__(name=name, health=health, mana=mana, strength=strength)
        self.min_damage = 1
        self.max_damage = 3

    def leave_combat(self):
        super().leave_combat()
        self.SOR_ACTIVE = False  # Remove SOR aura

    def _level_up(self):
        super()._level_up()

        for available_spell in self._lookup_available_spells_to_learn(self.level):  # generator that returns dictionaries holding spell attributes

            # update spell rank
            if available_spell['name'] in self.learned_spells:
                self.update_spell(available_spell)
            # learn new spell
            else:
                self.learn_new_spell(spell=available_spell)
                pass

    def learn_new_spell(self, spell: dict):
        print("You have learned a new spell - {}".format(spell['name']))

        self.learned_spells[spell['name']] = spell

    def _lookup_available_spells_to_learn(self, level: int):
        """
        Generator function
            paladin_spells_template table is as follows:
            ID, Name of Spell, Rank of Spell, Level Required for said Rank, Damage1, Damage2, Damage3, Heal1, Heal2, Heal3, Comment
            1,Seal of Righteousness,       1,                            1,       2,       0,       0,     0,     0,     0, Seal of Righteousness
            :return: A dictionary holding keys for each row (rank, damage1, damage2 etc.)
        """

        with sqlite3.connect(DB_PATH) as connection:
            cursor = connection.cursor()
            # this will return a list of tuples holding information about each spell we have the req level to learn

            spell_reader = cursor.execute("SELECT * FROM paladin_spells_template WHERE level_required = ?", [level])

            for line in spell_reader:
                spell = {}
                name = line[DBINDEX_PALADIN_SPELLS_TEMPLATE_NAME]
                rank = int(line[DBINDEX_PALADIN_SPELLS_TEMPLATE_RANK])
                level_req = int(line[DBINDEX_PALADIN_SPELLS_TEMPLATE_LEVEL_REQUIRED])
                damage_1 = int(line[DBINDEX_PALADIN_SPELLS_TEMPLATE_DAMAGE1])
                damage_2 = int(line[DBINDEX_PALADIN_SPELLS_TEMPLATE_DAMAGE2])
                damage_3 = int(line[DBINDEX_PALADIN_SPELLS_TEMPLATE_DAMAGE3])
                heal_1 = int(line[DBINDEX_PALADIN_SPELLS_TEMPLATE_HEAL1])
                heal_2 = int(line[DBINDEX_PALADIN_SPELLS_TEMPLATE_HEAL2])
                heal_3 = int(line[DBINDEX_PALADIN_SPELLS_TEMPLATE_HEAL3])
                mana_cost = int(line[DBINDEX_PALADIN_SPELLS_TEMPLATE_MANA_COST])

                spell['name'] = name
                spell['rank'] = rank
                spell['damage_1'] = damage_1
                spell['damage_2'] = damage_2
                spell['damage_3'] = damage_3
                spell['heal_1'] = heal_1
                spell['heal_2'] = heal_2
                spell['heal_3'] = heal_3
                spell['mana_cost'] = mana_cost

                yield spell

    def update_spell(self, spell: dict):
        spell_name = spell['name']

        if spell_name == 'Seal of Righteousness':
            self._update_seal_of_righteousness(spell)

    # SPELLS
    def spell_handler(self, command: str) -> bool:
        """

        :param command: Command telling you which spell to use
        :return: Returns a boolean indicating if the cast was successful or not
        """
        if command == 'sor':
            return self.spell_seal_of_righteousness()
        elif command == 'fol':
            return self.spell_flash_of_light()

        print("Unsuccessful cast")
        return False  # if we do not go into any spell

    def spell_seal_of_righteousness(self):
        """
         When activated adds X Spell Damage to each attack
         Lasts for three turns
        :return: boolean indicating if the cast was successful or not
        """
        cast_is_successful = self._check_enough_mana(self.learned_spells['Seal of Righteousness']["mana_cost"])

        if cast_is_successful:
            self.SOR_ACTIVE = True
            self.SOR_TURNS = 3
            print("{0} activates Seal of Righteousness!".format(self.name))
        return cast_is_successful

    def _spell_seal_of_righteousness_attack(self):
        if self.SOR_TURNS == 0:  # fade spell
            self.SOR_ACTIVE = False
            print("Seal of Righteousness has faded from {}".format(self.name))
            return 0
        else:
            self.SOR_TURNS -= 1
            # TODO: Load damage from DB
            return self.learned_spells['Seal of Righteousness']['damage_on_swing']  # damage from SOR

    def _update_seal_of_righteousness(self, new_rank: dict):
        """ Updates the values of the spell in the learned_spells dictionary"""
        damage_on_swing = new_rank['damage_1']
        rank = new_rank['rank']
        mana_cost = new_rank['mana_cost']
        self.learned_spells['Seal of Righteousness']['damage_on_swing'] = damage_on_swing
        self.learned_spells['Seal of Righteousness']['rank'] = rank
        self.learned_spells['Seal of Righteousness']['mana_cost'] = mana_cost

        print("Spell Seal of Righteousness has been updated to rank {}!".format(rank))
        print("*"*20)

    def spell_flash_of_light(self):
        """
        Heals the paladin for a certain amount
        :return successful cast or not
        """
        mana_cost = self.learned_spells['Flash of Light']['mana_cost']
        heal_amount = self.learned_spells['Flash of Light']['heal_1']

        cast_is_successful = self._check_enough_mana(mana_cost)

        if cast_is_successful:
            self.health += heal_amount
            self.mana -= mana_cost

            if self.health > self.max_health: # check for overheal
                overheal = self.health - self.max_health
                self.health = self.max_health
                print("Flash of Light healed {0} for {1:.2f} ({2:.2f} Overheal).".format(self.name, heal_amount - overheal, overheal))
            else:
                print("Flash of Light healed {0} for {1:.2f}.".format(self.name, heal_amount))

        return cast_is_successful
    # SPELLS

    def auto_attack(self, target_level: int):
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
        attacker_swing = self.auto_attack(victim.level)  # tuple holding auto attack and seal damage (if active)

        auto_attack = attacker_swing[0]
        sor_damage = attacker_swing[1]  # if the seal isn't active the damage will be 0

        if sor_damage:
            print("{0} attacks {1} for {2:.2f} + {3:.2f} from Seal of Righteousness!".format(self.name, victim.name, auto_attack, sor_damage))
        else:
            print("{0} attacks {1} for {2:.2f} damage!".format(self.name, victim.name, auto_attack))

        victim.take_attack(auto_attack + sor_damage)

    def _check_enough_mana(self, mana_cost: int) -> bool:
        """
        Check if we have enough mana to cast the spell we want to cast and return the result.
        """
        if self.mana < mana_cost:
            return False
        else:
            return True

    def get_class(self):
        return 'paladin'
