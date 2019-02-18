from pysc2.agents import base_agent
from pysc2.lib import actions, units, features


class Attack(base_agent.BaseAgent):
    def __init__(self):
        super(Attack, self).__init__()
        self.reqSteps = 0

    def attack(self, obs, reqSteps):
        new_action = [actions.FUNCTIONS.no_op()]
        if reqSteps == 0:
            self.reqSteps = 2

        elif reqSteps == 2:
            self.reqSteps = 1
            if actions.FUNCTIONS.select_army.id in obs.observation.available_actions:
                new_action = actions.FUNCTIONS.select_army("select")

        elif reqSteps == 1:
            self.reqSteps = 0
            if actions.FUNCTIONS.Attack_minimap.id in obs.observation.available_actions:
                new_action = actions.FUNCTIONS.Attack_minimap("now", [0, 0])

        return new_action

    #def get_closest_enemy(self, obs):
