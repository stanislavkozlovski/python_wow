class Quest:
    def __init__(self, quest_name: str, quest_id, xp_reward: int, item_reward_dict: dict, reward_choice_enabled: bool,
                 level_required: int, is_completed: bool = False):
        self.name = quest_name
        self.ID = quest_id
        self.xp_reward = xp_reward
        self.is_completed = is_completed
        self.required_level = level_required
        self.item_rewards = item_reward_dict  # dictionary for the rewards key: item name, value: item object
        self.reward_choice_enabled = reward_choice_enabled  # type: bool

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

    def give_item_rewards(self):
        """ this method gives the player his items, or if he has to choose one, opens up the window where
        he makes the choice and gives him that item.
        This method is called from the Character class in entities.py"""
        from command_handler import handle_quest_item_choice

        if self.reward_choice_enabled:
            return handle_quest_item_choice(self.item_rewards)
        else:
            # return a list of all the instances of Item
            return list(filter(lambda x: x is not None,  self.item_rewards.values()))


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
        return (f'{self.name} - Requires {self.required_kills} {self.required_monster} kills.'
                f' Rewards {self.xp_reward} experience.')

    def update_kills(self):
        self.kills += 1
        print(f'Quest {self.name}: {self.kills}/{self.required_kills} {self.required_monster} slain.')
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
        return (f'{self.name} - Obtain {self.required_item_count} {self.required_item}. '
                f'Rewards {self.xp_reward} experience.')

    def check_if_complete(self, inventory: dict):
        """ Given the player's inventory, check if he has enough to complete the quest"""
        _, item_count = inventory.get(self.required_item, (self.required_item, 0))

        if item_count:
            print(f'Quest {self.name}: {item_count}/{self.required_item_count} {self.required_item} obtained.')

        if item_count >= self.required_item_count:
            self._quest_complete()
