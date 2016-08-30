class Quest:
    def __init__(self, quest_name: str, quest_id, xp_reward: int, item_reward_dict: dict, reward_choice_enabled: bool,
                 level_required: int, is_completed: bool = False):
        self.name = quest_name
        self.ID = quest_id
        self.xp_reward = xp_reward
        self.is_completed = is_completed
        self.required_level = level_required

    def update_kills(self):
        """ This method updates the required kills if the quest is a KillQuest"""
        pass

    def _check_if_complete(self):
        """ This method checks if the quest is completed on each new addition and completes it if it is"""
        pass

    def _quest_complete(self):
        self.is_completed = True

    def give_reward(self):
        return self.xp_reward


class KillQuest(Quest):
    """
    Standard kill X of Y quest
    """
    def __init__(self, quest_name: str, quest_id, required_monster: str, xp_reward: int, item_reward_dict: dict,
                 reward_choice_enabled: bool, level_required: int, required_kills: int, is_completed: bool = False):
        super().__init__(quest_name, quest_id, xp_reward, item_reward_dict, reward_choice_enabled, level_required,
                         is_completed)
        self.required_monster = required_monster
        self.required_kills = required_kills
        self.kills = 0

    def __str__(self):
        return (
            "{quest_name} - Requires {required_kills} {monster_name} kills. Rewards {xp_reward} experience."
            .format(quest_name=self.name, required_kills=self.required_kills,
                    monster_name=self.required_monster, xp_reward=self.xp_reward)
                )

    def update_kills(self):
        self.kills += 1
        print("Quest {name}: {kills}/{required_kills} {monster_name} slain.".format(name=self.name,
                                                                                    kills=self.kills,
                                                                                    required_kills=self.required_kills,
                                                                                    monster_name=self.required_monster))
        self._check_if_complete()

    def _check_if_complete(self):
        if self.kills == self.required_kills:
            self._quest_complete()


class FetchQuest(Quest):
    """
    Standard obtain X of Y quest
    """
    def __init__(self, quest_name: str, quest_id, required_item: str, xp_reward: int, item_reward_dict: dict,
                 reward_choice_enabled: bool, level_required: int, required_item_count: int, is_completed: bool = False):
        super().__init__(quest_name, quest_id, xp_reward, item_reward_dict, reward_choice_enabled,
                         level_required, is_completed)
        self.required_item = required_item
        self.required_item_count = required_item_count

    def __str__(self):
        return (
            "{quest_name} - Obtain {amount_req} {item_name}. Rewards {xp_reward} experience."
            .format(quest_name=self.name, amount_req=self.required_item_count, item_name=self.required_item,
                    xp_reward=self.xp_reward)
            )

    def check_if_complete(self, inventory: dict):
        """ Given the player's inventory, check if he has enough to complete the quest"""
        _, item_count = inventory.get(self.required_item, (self.required_item, 0))

        if item_count:
            print("Quest {name}: {item_count}/{req_item_count} {item_name} obtained."
                  .format(name=self.name,
                          item_count=item_count,
                          req_item_count=self.required_item_count,
                          item_name=self.required_item))

        if item_count >= self.required_item_count:
            self._quest_complete()
