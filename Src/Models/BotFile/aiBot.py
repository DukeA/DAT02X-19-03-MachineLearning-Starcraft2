import random

from pysc2.agents import base_agent
from pysc2.lib import actions, units, features

from Models.BuildOrders.BuildOrders import BuildOrders


class aiBot(base_agent.BaseAgent):
    def __init__(self):
        super(aiBot, self).__init__()
        self.base_location = None
        self.attack_coordinates = None
        self.reqSteps = 0
        self.currAct = 0
        self.queued = False

    def step(self, obs):
        super(aiBot, self).step(obs)

        # first step
        if obs.first():
            start_y, start_x = (obs.observation.feature_minimap.player_relative
                                == features.PlayerRelative.SELF).nonzero()
            xmean = start_x.mean()
            ymean = start_y.mean()

            self.base_location = (xmean, ymean)
            if xmean <= 31 and ymean <= 31:
                self.attack_coordinates = (47, 47)
            else:
                self.attack_coordiantes = (12, 16)

        if self.reqSteps == 0:
            self.currAct = random.randint(0, 4)

        free_supply = (obs.observation.player.food_cap -
                       obs.observation.player.food_used)

        if self.currAct == 0:  # build scv
            action = BuildOrders.build_scv(self,obs, free_supply)

        elif self.currAct == 1:  # build supply depot
            action = BuildOrders.build_supply_depot(self,obs,free_supply)

        elif self.currAct == 2:
            action = BuildOrders.build_barracks(self,obs,self.reqSteps)

        elif self.currAct == 3:
            action = BuildOrders.build_refinery(self,obs)

        elif self.currAct == 4:
            action = BuildOrders.return_scv(self,obs)

        else:
            action = [actions.FUNCTIONS.no_op()]

        return action[0]


















