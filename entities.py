"""
This holds the classes for every entity in the game: Monsters and Characters currently
"""

from items import Weapon
import csv


def load_xp_reward() -> dict:
    """
    Load the default XP that is to be given from the creature.
    The .csv file's contents are as follows:
    Level, Experience to give
    1,     50 Meaning a creature that is level 1 will give 50 XP
    2,     75 Gives 75 XP
    etc...

    Because the Monster class will be called upon a number of times, it would be inefficient to read the whole file
    on every monster creation. That's why this is outside of the class, to read the file only once.

    :return: A dictionary as follows: Key: Level, Value: XP Reward
                                            1   , 50
    """

    xp_reward_dict = {}

    with open('creature_default_xp_rewards.csv') as _:
        def_xp_rewards_reader = csv.reader(_)

        for line in def_xp_rewards_reader:
            level = int(line[0])
            xp_reward = int(line[1])

            xp_reward_dict[level] = xp_reward

    return xp_reward_dict


CREATURE_XP_REWARD_DICTIONARY = load_xp_reward()


def lookup_xp_reward(level: int) -> int: # the method that is going to be used by the Monster class
    return CREATURE_XP_REWARD_DICTIONARY[level]


class LivingThing:
    """
    This is the base class for all things alive - characters, monsters and etc.
    """
    def __init__(self, name: str, health: int=1, mana: int=1):
        self.name = name
        self.health = health
        self.max_health = health
        self.mana = mana
        self.max_mana = mana
        self.alive = True
        self.in_combat = False

    def is_alive(self):
        return self.alive

    def enter_combat(self):
        self.in_combat = True

    def leave_combat(self):
        self.in_combat = False

    def check_if_dead(self):
        if self.health <= 0:
            self.alive = False
            self.die()

    def die(self):
        pass


class Monster(LivingThing):
    def __init__(self, monster_id: int, name: str, health: int=1, mana: int=1, level: int=1, min_damage: int=0, max_damage: int=1):
        super().__init__(name, health, mana)
        self.monster_id = monster_id
        self.level = level
        self.min_damage = min_damage
        self.max_damage = max_damage
        self.xp_to_give = lookup_xp_reward(self.level)

    def __str__(self):
        return "Creature Level {level} {name} - {hp}/{max_hp} HP | {mana}/{max_mana} Mana".format(level = self.level, name = self.name,
                                                                                                  hp = self.health, max_hp = self.max_health,
                                                                                                  mana = self.mana, max_mana = self.max_mana)

    def deal_damage(self, target_level: int):
        import random
        level_difference = self.level - target_level
        percentage_mod = (abs(level_difference) * 0.1)  # calculates by how many % we're going to increase/decrease dmg

        damage_to_deal = random.randint(int(self.min_damage), int(self.max_damage) + 1)
        # 10% more or less damage for each level that differs
        if level_difference == 0:
            pass
        elif level_difference < 0:  # character is bigger level
            damage_to_deal -= damage_to_deal * percentage_mod  # -X%
        elif level_difference > 0:  # monster is bigger level
            damage_to_deal += damage_to_deal * percentage_mod  # +X%

        return damage_to_deal

    def take_attack(self, damage: int):
        self.health -= damage
        self.check_if_dead()

    def die(self):
        print("Creature {} has been slain!".format(self.name))

    def leave_combat(self):
        super().leave_combat()
        self.health = self.max_health # reset the health




class Character(LivingThing):
    KEY_LEVEL_STATS_HEALTH = 'health'
    KEY_LEVEL_STATS_MANA = 'mana'
    KEY_LEVEL_STATS_STRENGTH = 'strength'

    def __init__(self, name: str, health: int=1, mana: int=1, strength: int=1):
        super().__init__(name, health, mana)
        self.strength = strength
        self.min_damage = 0
        self.max_damage = 1
        self.equipped_weapon = Weapon()
        self.level = 1
        self.experience = 0
        self.xp_req_to_level = 400
        self._LEVEL_STATS = self._load_levelup_stats()
        self._REQUIRED_XP_TO_LEVEL = self._load_xp_requirements()

    def equip_weapon(self, weapon: Weapon):
        self.equipped_weapon = weapon
        self._calculate_damage(self.equipped_weapon)

    def _calculate_damage(self, weapon: Weapon):
        # current formula for damage is: wep_dmg * 0.1 * strength
        self.min_damage = weapon.min_damage + (0.1 * self.strength)
        self.max_damage = weapon.max_damage + (0.1 * self.strength)

    def deal_damage(self, target_level: int):
        import random

        level_difference = self.level - target_level
        percentage_mod = (abs(level_difference) * 0.1)  # calculates by how many % we're going to increase/decrease dmg

        damage_to_deal = random.randint(int(self.min_damage), int(self.max_damage) + 1)
        # 10% more or less damage for each level that differs
        if level_difference == 0:
            pass
        elif level_difference < 0: # monster is bigger level
            damage_to_deal -= damage_to_deal * percentage_mod # -X%
        elif level_difference > 0: # character is bigger level
            damage_to_deal += damage_to_deal * percentage_mod # +X%

        return damage_to_deal

    def take_attack(self, damage: int):
        self.health -= damage
        self.check_if_dead()

    def die(self):
        print("Character {} has been slain!".format(self.name))

    def prompt_revive(self):
        print("Do you want to restart? Y/N")
        if input() in 'Yy':
            self.revive()
        else:
            exit()

    def revive(self):
        self._regenerate()
        self.alive = True

    def leave_combat(self):
        super().leave_combat()
        self._regenerate()

    def check_if_levelup(self):
        if self.experience >= self.xp_req_to_level:
            self._level_up()
            self.experience = 0
            self.xp_req_to_level = self._lookup_next_xp_level_req()

    def _lookup_next_xp_level_req(self):
        return self._REQUIRED_XP_TO_LEVEL[self.level]

    def award_monster_kill(self, xp_reward: int, monster_level: int):
        level_difference = self.level - monster_level
        xp_bonus_reward = 0
        if level_difference >= 5: # if the character is 5 levels higher, give no XP
            xp_reward = 0
        elif level_difference < 0: # monster is higher level
            percentage_mod = abs(level_difference) * 0.1  # 10% increase of XP for every level the monster has over player
            xp_bonus_reward += int(xp_reward*percentage_mod)  # convert to int


        if xp_bonus_reward:
            print("XP awarded: {0} + bonus {1} for the level difference!".format(xp_reward, xp_bonus_reward))
        else:
            print("XP awarded: {0}!".format(xp_reward))

        self.experience += xp_reward + xp_bonus_reward
        self.check_if_levelup()

    def _load_levelup_stats(self):
        # TODO: to be moved to a separate file sometime
        """
        Read the .csv file holding information about the amount of stats you should get according to the level you've attained
        1 - level; 2 - hp; 3 - mana; 4 - strength;
        """
        level_stats = {} # a dictionary of dictionaries. Key - level, value - dictionary holding values for hp,mana etc.
        with open('levelup_stats.csv') as _:
            lvl_stats_reader = csv.reader(_)
            for line in lvl_stats_reader:
                level_dict = {}

                level = int(line[0])
                hp = int(line[1])
                mana = int(line[2])
                strength = int(line[3])

                level_dict[self.KEY_LEVEL_STATS_HEALTH] = hp
                level_dict[self.KEY_LEVEL_STATS_MANA] = mana
                level_dict[self.KEY_LEVEL_STATS_STRENGTH] = strength
                level_stats[level] = level_dict

        return level_stats

    def _load_xp_requirements(self):
        # TODO: to be moved to a separate file sometime
        """
        Load the information about the necessary XP needed to reach a certain level.
        The .csv file's contents is like this:
        level, xp needed to reach the next one
        1,     400 meaning you need to have 400XP to reach level 2
        2,     800 800XP needed to reach level 3
        :return: A dictionary - Key: Level, Value: XP Needed
                                        1,  400
        """
        xp_req_dict = {}

        with open('level_xp_requirement.csv') as _:
            xp_req_reader = csv.reader(_)
            for line in xp_req_reader:
                level = int(line[0])
                xp_required = int(line[1])
                xp_req_dict[level] = xp_required

        return xp_req_dict


    def _level_up(self):
        self.level += 1
        dd = self._LEVEL_STATS[self.level]
        ddd = dd[self.KEY_LEVEL_STATS_HEALTH]
        # access the dictionary holding the appropriate value increases for each level
        hp_increase_amount = self._LEVEL_STATS[self.level][self.KEY_LEVEL_STATS_HEALTH]
        mana_increase_amount = self._LEVEL_STATS[self.level][self.KEY_LEVEL_STATS_MANA]
        strength_increase_amount = self._LEVEL_STATS[self.level][self.KEY_LEVEL_STATS_STRENGTH]

        self.max_health += hp_increase_amount
        self.max_mana += mana_increase_amount
        self.strength += strength_increase_amount
        self._regenerate() # get to full hp/mana
        print('*' * 20)
        print("Character {0} has leveled up to level {1}!".format(self.name, self.level))
        print("Health Points increased by {}".format(hp_increase_amount))
        print("Mana Points increased by {}".format(mana_increase_amount))
        print("Strength Points increased by {}".format(strength_increase_amount))
        print('*' * 20)

    def _regenerate(self):
        self.health = self.max_health
        self.mana = self.max_mana
