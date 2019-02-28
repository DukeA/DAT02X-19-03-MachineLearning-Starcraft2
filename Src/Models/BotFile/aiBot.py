import random
import statistics

from pysc2.agents import base_agent
from pysc2.lib import actions, units, features

from Models.BuildOrders.BuildOrderController import BuildOrderController
from Models.BuildOrders.BuildOrders import BuildOrders
from Models.BuildOrders.UnitBuildOrdersController import UnitBuildOrdersController
from Models.BuildOrders.ActionSingelton import ActionSingelton
from Models.ArmyControl.ArmyControl import ArmyControl


selectors = ['buildSelector', 'attackSelector']
attackSelector = ['attack']
buildSelector = ['build_scv', 'build_supply_depot', "build_marine",
                 'build_barracks', 'build_refinery', 'return_scv', 'expand']


class State:
    def __init__(self):
        self.armySupply = 0
        self.workerSupply = 0
        self.freeSupply = 0
        self.barracks = 0
        self.factories = 0
        self.commandcenters = 1
        self.refineries = 0


class AiBot(base_agent.BaseAgent):
    def __init__(self):
        super(AiBot, self).__init__()
        self.base_location = None
        self.start_top = None
        self.attack_coordinates = None
        self.reqSteps = 0
        self.selector = None
        self.doBuild = None
        self.doAttack = None
        self.new_action = None
        self.state = State()

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
                self.start_top = True
                self.attack_coordinates = (47, 47)
            else:
                self.start_top = False
                self.attack_coordiantes = (12, 16)

        free_supply = (obs.observation.player.food_cap -
                       obs.observation.player.food_used)
        action = [actions.FUNCTIONS.no_op()]
        self.state.freeSupply = free_supply
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
                BuildOrderController.build_expand(self, obs, self.start_top)
                action = ActionSingelton().get_action()

            elif self.doBuild == "build_scv":  # build scv
                BuildOrderController.build_scv(self, obs, free_supply)
                action = ActionSingelton().get_action()

            elif self.doBuild == "build_supply_depot":  # build supply depot
                BuildOrderController.build_supplaydepot(self, obs, free_supply)
                action = ActionSingelton().get_action()

            elif self.doBuild == "build_barracks":
                BuildOrderController.build_barracks(self, obs)
                action = ActionSingelton().get_action()

            elif self.doBuild == "build_refinery":
                BuildOrderController.build_refinary(self, obs)
                action = ActionSingelton().get_action()

            elif self.doBuild == "return_scv":
                BuildOrderController.return_scv(self, obs)
                action = ActionSingelton().get_action()

            elif self.doBuild == "build_marine":
                UnitBuildOrdersController.train_marines(self, obs, free_supply)
                action = ActionSingelton().get_action()

        elif self.selector == "attackSelector":
            if self.reqSteps == 0:
                self.doAttack = random.choice(attackSelector)

            if self.doAttack == "attack":
                action = ArmyControl.attack(self, obs, self.base_location)

            if self.doAttack == "retreat":
                action = ArmyControl.retreat(self, obs, self.base_location)
        return action[0]
