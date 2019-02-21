import random

from pysc2.agents import base_agent
from pysc2.lib import actions, features

from Models.BuildOrders.BuildOrderController import BuildOrderController
from Models.BuildOrders.UnitBuildOrdersController import UnitBuildOrdersController
from Models.BuildOrders.ActionSingelton import ActionSingelton


class AiBot(base_agent.BaseAgent):
    def __init__(self):
        super(AiBot, self).__init__()
        self.base_location = None
        self.attack_coordinates = None
        self.reqSteps = 0
        self.currAct = 0
        self.queued = False

    def step(self, obs):
        super(AiBot, self).step(obs)

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
            self.currAct = random.randint(0, 5)

        free_supply = (obs.observation.player.food_cap -
                       obs.observation.player.food_used)

        if self.currAct == 0:  # build scv
            BuildOrderController.build_scv(self,obs,free_supply)
            action = ActionSingelton().get_action()

        elif self.currAct == 1:  # build supply depot
            BuildOrderController.build_supplaydepot(self, obs, free_supply)
            action = ActionSingelton().get_action()

        elif self.currAct == 2:
            BuildOrderController.build_barracks(self, obs)
            action = ActionSingelton().get_action()

        elif self.currAct == 3:
            BuildOrderController.build_refinary(self, obs)
            action = ActionSingelton().get_action()

        elif self.currAct == 4:
            BuildOrderController.return_scv(self, obs)
            action = ActionSingelton().get_action()

        elif self.currAct == 5:
            UnitBuildOrdersController.train_marines(self, obs, free_supply)
            action = ActionSingelton().get_action()

        else:
            action = [actions.FUNCTIONS.no_op()]

        return action[0]
