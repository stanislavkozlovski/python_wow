from entities import Character, Monster
import sqlite3
DB_PATH = "./python_wowDB.db"

class Paladin(Character):
    """
    Paladin spells:
        Spells every paladin starts with:
            Seal of Righteousness
                Deals X damage on each attack, needs to be activated first
    """
    learned_spells = {"Seal of Righteousness": {"damage_on_swing": 2, "mana_cost": 4, "rank": 1}}
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

        for available_spell in self._lookup_available_spells_to_learn(self.level):

            # update spell rank
            if available_spell['name'] in self.learned_spells:
                self.update_spell(available_spell)
            # learn new spell
            else:
                # TODO: Learn new spell prompt
                pass
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
                name = line[1]
                rank = int(line[2])
                level_req = int(line[3])
                damage_1 = int(line[4])
                damage_2 = int(line[5])
                damage_3 = int(line[6])
                heal_1 = int(line[7])
                heal_2 = int(line[8])
                heal_3 = int(line[9])
                mana_cost = int(line[10])

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

        return False  # if we do not go into any spell

    def spell_seal_of_righteousness(self):
        """
         When activated adds X Spell Damage to each attack
         Lasts for three turns
        :return: boolean indicating if the cast was successful or not
        """
        if self.mana < self.learned_spells['Seal of Righteousness']['mana_cost']:
            print("Not enough mana!")
            return False

        self.SOR_ACTIVE = True
        self.SOR_TURNS = 3
        print("{0} activates Seal of Righteousness!".format(self.name))
        return True

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


    # This is useless, come to think about it

    # def _load_paladin_spells(self):
    #     """

    def get_class(self):
        return 'paladin'