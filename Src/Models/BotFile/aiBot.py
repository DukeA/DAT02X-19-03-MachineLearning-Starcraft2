import random
import statistics

from pysc2.agents import base_agent
from pysc2.lib import actions, units, features

from Models.BuildOrders.BuildOrderController import BuildOrderController
from Models.BuildOrders.BuildOrders import BuildOrders
from Models.BuildOrders.UnitBuildOrdersController import UnitBuildOrdersController
from Models.BuildOrders.ActionSingelton import ActionSingelton
from Models.ArmyControl.ArmyControlController import ArmyControlController
from Models.Predefines.Coordinates import Coordinates


selectors = ['buildSelector', 'attackSelector']
attackSelector = ['attack', 'retreat']
buildSelector = ['build_scv', 'build_supply_depot',"build_marine",
                 'build_barracks', 'build_refinery', 'return_scv', 'expand']


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
        self.new_action=None


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
                self.attack_coordinates = (12, 16)

        free_supply = (obs.observation.player.food_cap -
                       obs.observation.player.food_used)
        action = [actions.FUNCTIONS.no_op()]
        if self.reqSteps == 0:
            if self.steps < 16*60*6/5*1.4:  # 16 steps per sekund, men kompenserar också för att step_mul = 5. 1.4 kompenserar för in-game time.
                self.selector = 'buildSelector'
            else:
                self.selector = random.choice(selectors)

        if self.selector == "buildSelector":

            if self.reqSteps == 0:
                self.doBuild = random.choice(buildSelector)

            if self.doBuild == "expand":
                BuildOrderController.build_expand(self,obs,self.start_top)
                action = ActionSingelton().get_action()

            elif self.doBuild == "build_scv":  # build scv
                BuildOrderController.build_scv(self,obs,free_supply)
                action = ActionSingelton().get_action()

            elif self.doBuild == "build_supply_depot":  # build supply depot
                BuildOrderController.build_supplaydepot(self,obs,free_supply)
                action = ActionSingelton().get_action()

            elif self.doBuild == "build_barracks":
                BuildOrderController.build_barracks(self,obs)
                action = ActionSingelton().get_action()

            elif self.doBuild == "build_refinery":
                BuildOrderController.build_refinary(self,obs)
                action = ActionSingelton().get_action()

            elif self.doBuild == "return_scv":
                BuildOrderController.return_scv(self,obs)
                action = ActionSingelton().get_action()

            elif self.doBuild =="build_marine":
                UnitBuildOrdersController.train_marines(self,obs,free_supply)
                action = ActionSingelton().get_action()

        elif self.selector == "attackSelector":
            if self.reqSteps == 0:
                self.doAttack = random.choice(attackSelector)
                self.doAttack = "attack"

            if self.doAttack == "attack":
                ArmyControlController.attack(self, obs, self.attack_coordinates) # Det tar tid att hitta närmaste fienden
                action = ActionSingelton().get_action()

            if self.doAttack == "retreat":
                ArmyControlController.retreat(self, obs)
                action = ActionSingelton().get_action()

        return action[0]

