class Quest:
    """
    Standard kill X of Y quest
    """
    def __init__(self, quest_name: str, quest_id, creature_name: str, kill_amount: int, xp_reward: int):
        self.name = quest_name
        self.ID = quest_id
        self.monster_to_kill = creature_name
        self.needed_kills = kill_amount
        self.kills = 0
        self.xp_to_give = xp_reward
        self.completed = False

    def add_kill(self):
        self.kills += 1
        print("Quest {0}: {1}/{2} {3} slain.".format(self.name, self.kills, self.needed_kills, self.monster_to_kill))
        self.check_if_complete()

    def check_if_complete(self):
        if self.kills == self.needed_kills:
            self.quest_complete()
        else:
            pass
    def quest_complete(self):
        self.completed = True

    def reward(self):
        return self.xp_to_give