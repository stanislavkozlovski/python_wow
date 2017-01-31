class Quest:
    def __init__(self, quest_name: str, quest_id, xp_reward: int, item_reward_dict: dict, reward_choice_enabled: bool,
                 level_required: int, is_completed: bool = False):
        self.name = quest_name
        self.ID = quest_id
        self.xp_reward = xp_reward
        self.is_completed = is_completed
        self.required_level = level_required
        self.item_rewards: {str: 'Item'} = item_reward_dict
        self.reward_choice_enabled: bool = reward_choice_enabled

    def __eq__(self, other):
        return self.ID == other.ID

    def update_kills(self):
        """ This method updates the required kills if the quest is a KillQuest"""
        pass

    def check_if_complete(self, character: 'Character'=None):
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
        if self.reward_choice_enabled:
            from command_handler import handle_quest_item_choice

            return handle_quest_item_choice(self.item_rewards)
        else:
            # return a list of all the instances of Item
            return [item for item in self.item_rewards.values() if item is not None]


class KillQuest(Quest):
    """
    Standard kill X of Y quest
    """
    def __init__(self, quest_name: str, quest_id, required_monster: str, xp_reward: int, item_reward_dict: dict,
                 reward_choice_enabled: bool, level_required: int, required_kills: int, is_completed: bool = False):
        super().__init__(quest_name, quest_id, xp_reward, item_reward_dict, reward_choice_enabled, level_required,
                         is_completed)
        self.required_monster: str = required_monster  # name of the monster
        self.required_kills: int = required_kills
        self.kills = 0

    def __str__(self):
        return (f'{self.name} - Requires {self.required_kills} {self.required_monster} kills.'
                f' Rewards {self.xp_reward} experience.')

    def update_kills(self):
        self.kills += 1
        print(f'Quest {self.name}: {self.kills}/{self.required_kills} {self.required_monster} slain.')
        self.check_if_complete()

    def check_if_complete(self, character: 'Character'=None):
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
        self.required_item: str = required_item
        self.required_item_count = required_item_count

    def __str__(self):
        return (f'{self.name} - Obtain {self.required_item_count} {self.required_item}. '
                f'Rewards {self.xp_reward} experience.')

    def check_if_complete(self, character: 'Character'=None):
        """ Given the player's inventory, check if he has enough to complete the quest"""
        if character is None or not hasattr(character, 'inventory'):
            raise Exception('The FetchQuest check_if_complete method requires  that a character object is passed to it!')
        _, item_count = character.inventory.get(self.required_item, (self.required_item, 0))

        if item_count:
            print(f'Quest {self.name}: {item_count}/{self.required_item_count} {self.required_item} obtained.')

        if item_count >= self.required_item_count:
            self._quest_complete()
