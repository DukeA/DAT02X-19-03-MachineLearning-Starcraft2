import random
import statistics

from pysc2.agents import base_agent
from pysc2.lib import actions, units, features

from Models.BuildOrders.BuildOrders import BuildOrders
from Models.Attack.Attack import Attack


selectors = ['buildSelector', 'attackSelector']
attackSelector = ['attack']
buildSelector = ['build_scv', 'build_supply_depot',
                 'build_barracks', 'build_refinery', 'return_scv', 'expand']


class aiBot(base_agent.BaseAgent):
    def __init__(self):
        super(aiBot, self).__init__()
        self.base_location = None
        self.start_top = None
        self.attack_coordinates = None
        self.reqSteps = 0
        self.selector = None
        self.doBuild = None
        self.doAttack = None

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
                self.start_top = True
                self.attack_coordinates = (47, 47)
            else:
                self.start_top = False
                self.attack_coordiantes = (12, 16)

        free_supply = (obs.observation.player.food_cap -
                       obs.observation.player.food_used)
        action = [actions.FUNCTIONS.no_op()]
        if self.reqSteps == 0:
            if True:  # någon algoritm för att kolla så att tiden är mindre än 2 min
                self.selector = 'buildSelector'
            else:
                pass
                # ska vara men vet ej om attackers funkar än: self.selector = random.choice(selectors)

        if self.selector == "buildSelector":

            if self.reqSteps == 0:
                self.doBuild = random.choice(buildSelector)

            if self.doBuild == "expand":
                action = BuildOrders.expand(self, obs, self.start_top)

            elif self.doBuild == "build_scv":  # build scv
                action = BuildOrders.build_scv(self, obs, free_supply)

            elif self.doBuild == "build_supply_depot":  # build supply depot
                action = BuildOrders.build_supply_depot(self, obs, free_supply)

            elif self.doBuild == "build_barracks":
                action = BuildOrders.build_barracks(self, obs)

            elif self.doBuild == "build_refinery":
                action = BuildOrders.build_refinery(self, obs)

            elif self.doBuild == "return_scv":
                action = BuildOrders.return_scv(self, obs)

        elif self.selector == "attackSelector":
            if self.reqSteps == 0:
                self.doAttack = random.choice(attackSelector)

            if self.doAttack == "attack":
                action = Attack.attack(self, obs, self.base_location)

        return action[0]
