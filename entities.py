"""
This holds the classes for every entity in the game: Monsters and Characters currently
"""

import random

from items import Weapon
from loader import (load_creature_xp_rewards, load_character_level_stats,
                    load_character_xp_requirements, load_creature_gold_reward)
from quest import Quest

# dictionary that holds information about how much XP a monster of a certain level should award the player.
# key: level(int), value: xp reward(int)
CREATURE_XP_REWARD_DICTIONARY = load_creature_xp_rewards()
CREATURE_GOLD_REWARD_DICTIONARY = load_creature_gold_reward()


def lookup_xp_reward(level: int) -> int:
    """ Return the appropriate XP reward associated with the given level"""
    return CREATURE_XP_REWARD_DICTIONARY[level]


def lookup_gold_reward(level: int) -> int:
    """ Return the appropriate gold reward associated with the given level"""
    return CREATURE_GOLD_REWARD_DICTIONARY[level]


class LivingThing:
    """
    This is the base class for all things _alive - characters, monsters and etc.
    """

    def __init__(self, name: str, health: int = 1, mana: int = 1):
        self.name = name
        self.health = health
        self.max_health = health
        self.mana = mana
        self.max_mana = mana
        self._alive = True
        self._in_combat = False

    def is_alive(self):
        return self._alive

    def is_in_combat(self):
        return self._in_combat

    def enter_combat(self):
        self._in_combat = True

    def leave_combat(self):
        self._in_combat = False
        self._regenerate()

    def _regenerate(self):
        self.health = self.max_health
        self.mana = self.max_mana

    def check_if_dead(self):
        if self.health <= 0:
            self._die()

    def _die(self):
        self._alive = False

    def revive(self):
        self._regenerate()
        self._alive = True


class Monster(LivingThing):
    def __init__(self, monster_id: int, name: str, health: int = 1, mana: int = 1, level: int = 1, min_damage: int = 0,
                 max_damage: int = 1, quest_relation_id=0):
        super().__init__(name, health, mana)
        self.monster_id = monster_id
        self.level = level
        self.min_damage = min_damage
        self.max_damage = max_damage
        self.xp_to_give = lookup_xp_reward(self.level)
        self.gold_to_give = lookup_gold_reward(self.level)
        self.quest_relation_ID = quest_relation_id

    def __str__(self):
        return "Creature Level {level} {name} - {hp}/{max_hp} HP | {mana}/{max_mana} Mana | " \
               "{min_dmg}-{max_dmg} Damage".format(level=self.level, name=self.name,
                                                   hp=self.health, max_hp=self.max_health,
                                                   mana=self.mana, max_mana=self.max_mana,
                                                   min_dmg=self.min_damage, max_dmg=self.max_damage)

    def get_auto_attack_damage(self, target_level: int):
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

    def attack(self, victim):  # victim: Character
        monster_swing = self.get_auto_attack_damage(victim.level)  # an integer representing the damage

        print("{0} attacks {1} for {2:.2f} damage!".format(self.name, victim.name, monster_swing))

        victim.take_attack(monster_swing)

    def take_attack(self, damage: int):
        self.health -= damage
        self.check_if_dead()

    def _die(self):
        super()._die()
        print("Creature {} has died!".format(self.name))


class Character(LivingThing):
    # keys are used to access the level_stats dictionary that holds information on stats to update on each level up
    KEY_LEVEL_STATS_HEALTH = 'health'
    KEY_LEVEL_STATS_MANA = 'mana'
    KEY_LEVEL_STATS_STRENGTH = 'strength'

    def __init__(self, name: str, health: int = 1, mana: int = 1, strength: int = 1):
        super().__init__(name, health, mana)
        self.strength = strength
        self.min_damage = 0
        self.max_damage = 1
        self.equipped_weapon = Weapon()
        self.level = 1
        self.experience = 0
        self.gold = 0
        self.xp_req_to_level = 400
        self.current_zone = "Elwynn Forest"
        self.current_subzone = "Northshire Valley"
        # A dictionary of dictionaries. Key: level(int), Value: dictionary holding values for hp,mana,etc
        self._LEVEL_STATS = load_character_level_stats()
        self._REQUIRED_XP_TO_LEVEL = load_character_xp_requirements()
        self.quest_log = {}

    def equip_weapon(self, weapon: Weapon):
        self.equipped_weapon = weapon
        self._calculate_damage(self.equipped_weapon)

    def _calculate_damage(self, weapon: Weapon):
        # current formula for damage is: wep_dmg * 0.1 * strength
        self.min_damage = weapon.min_damage + (0.1 * self.strength)
        self.max_damage = weapon.max_damage + (0.1 * self.strength)

    def spell_handler(self, command: str):
        """
        Every class will have different spells, this method will make sure the proper spell is caster
        :param command: the spell name that is to be cast
        :return:
        """
        pass

    def get_auto_attack_damage(self, target_level: int):
        level_difference = self.level - target_level
        percentage_mod = (abs(level_difference) * 0.1)  # calculates by how many % we're going to increase/decrease dmg

        damage_to_deal = random.randint(int(self.min_damage), int(self.max_damage) + 1)
        # 10% more or less damage for each level that differs
        if level_difference == 0:
            pass
        elif level_difference < 0:  # monster is bigger level
            damage_to_deal -= damage_to_deal * percentage_mod  # -X%
        elif level_difference > 0:  # character is bigger level
            damage_to_deal += damage_to_deal * percentage_mod  # +X%

        return damage_to_deal

    def attack(self, victim: Monster):
        pass

    def take_attack(self, damage: int):
        self.health -= damage
        self.check_if_dead()

    def _die(self):
        super()._die()
        print("Character {} has died!".format(self.name))

    def prompt_revive(self):
        print("Do you want to restart? Y/N")
        if input() in 'Yy':
            self.revive()
            print("Character {} has been revived!".format(self.name))
        else:
            exit()

    def add_quest(self, quest: Quest):
        self.quest_log[quest.ID] = quest

    def _check_if_quest_completed(self, quest: Quest):
        if quest.is_completed:
            self._complete_quest(quest)

    def _complete_quest(self, quest: Quest):
        print("Quest {} is_completed! XP awarded: {}!".format(quest.name, xp_reward))
        xp_reward = quest.give_reward()

        del self.quest_log[quest.ID]  # remove from quest log

        self.experience += xp_reward
        self.check_if_levelup()

    def award_monster_kill(self, monster: Monster):
        monster_level = monster.level
        xp_reward = monster.xp_to_give
        gold_reward = monster.gold_to_give
        monster_quest_ID = monster.quest_relation_ID

        level_difference = self.level - monster_level
        xp_bonus_reward = 0
        if level_difference >= 5:  # if the character is 5 levels higher, give no XP
            xp_reward = 0
        elif level_difference < 0:  # monster is higher level
            percentage_mod = abs(
                level_difference) * 0.1  # 10% increase of XP for every level the monster has over player
            xp_bonus_reward += int(xp_reward * percentage_mod)  # convert to int

        if xp_bonus_reward:
            print("XP awarded: {0} + bonus {1} for the level difference!".format(xp_reward, xp_bonus_reward))
        else:
            print("XP awarded: {0}!".format(xp_reward))

        self.experience += xp_reward + xp_bonus_reward
        self.gold += gold_reward
        self.check_if_levelup()

        # If this monster is for a quest and we have that quest
        if monster_quest_ID and monster_quest_ID in self.quest_log:
            # TODO: Might want another way to handle this
            quest = self.quest_log[monster_quest_ID]
            quest.update_kills()
            self.quest_log[monster_quest_ID] = quest

            self._check_if_quest_completed(quest)

    def check_if_levelup(self):
        if self.experience >= self.xp_req_to_level:
            self._level_up()
            self.experience = 0
            self.xp_req_to_level = self._lookup_next_xp_level_req()

    def _level_up(self):
        self.level += 1

        current_level_stats = self._LEVEL_STATS[self.level]
        # access the dictionary holding the appropriate value increases for each level
        hp_increase_amount = current_level_stats[self.KEY_LEVEL_STATS_HEALTH]
        mana_increase_amount = current_level_stats[self.KEY_LEVEL_STATS_MANA]
        strength_increase_amount = current_level_stats[self.KEY_LEVEL_STATS_STRENGTH]

        self.max_health += hp_increase_amount
        self.max_mana += mana_increase_amount
        self.strength += strength_increase_amount
        self._regenerate()  # regen to full hp/mana

        print('*' * 20)
        print("Character {0} has leveled up to level {1}!".format(self.name, self.level))
        print("Health Points increased by {}".format(hp_increase_amount))
        print("Mana Points increased by {}".format(mana_increase_amount))
        print("Strength Points increased by {}".format(strength_increase_amount))
        print('*' * 20)

    def print_quest_log(self):
        print("Your quest log:")

        for _, quest in self.quest_log.items():
            print("\t{quest_name} - {monsters_killed}/{required_kills} {monster_name} slain.".format(
                quest_name=quest.name,
                monsters_killed=quest.kills,
                required_kills=quest.needed_kills,
                monster_name=quest.monster_to_kill))

        print()

    def _lookup_next_xp_level_req(self):
        return self._REQUIRED_XP_TO_LEVEL[self.level]

    def get_class(self) -> str:
        """Returns the class of the character as a string"""
        pass
