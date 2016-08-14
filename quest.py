class Quest:
    """
    Standard kill X of Y quest
    """
    def __init__(self, quest_name: str, quest_id, creature_name: str, required_kills: int, xp_reward: int,
                 level_required: int, is_completed: bool = False):
        self.name = quest_name
        self.ID = quest_id
        self.monster_to_kill = creature_name
        self.required_kills = required_kills
        self.kills = 0
        self.xp_reward = xp_reward
        self.is_completed = is_completed
        self.required_level = level_required

    def update_kills(self):
        self.kills += 1
        print("Quest {0}: {1}/{2} {3} slain.".format(self.name, self.kills, self.required_kills, self.monster_to_kill))
        self._check_if_complete()

    def _check_if_complete(self):
        if self.kills == self.required_kills:
            self._quest_complete()

    def _quest_complete(self):
        self.is_completed = True

    def give_reward(self):
        return self.xp_reward
