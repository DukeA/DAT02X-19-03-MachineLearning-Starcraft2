import random
import statistics

from pysc2.agents import base_agent
from pysc2.lib import actions, units, features

from Models.BuildOrders.BuildOrderController import BuildOrderController
from Models.BuildOrders.UnitBuildOrdersController import UnitBuildOrdersController
from Models.BuildOrders.ActionSingelton import ActionSingelton
from Models.ArmyControl.ArmyControlController import ArmyControlController
from Models.Predefines.Coordinates import Coordinates


selectors = ['buildSelector', 'attackSelector']
attackSelector = ['attack', 'retreat', 'scout', 'count_army', 'no_op']    # Might be unnecessary depending on implementation of randomness
buildSelector = ['build_scv', 'build_supply_depot',"build_marine",
                 'build_barracks', 'build_refinery', 'return_scv', 'expand', 'no_op']


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

        # Basic game state test variables.

        self.last_scout = 0        # Maybe for ML
        self.marine_count = 0      # Maybe for ML
        self.action_finished = False
        self.action_data = []    # Does this persist between loops? It's a tuple (selector, action, steps, marine_count)

        # End of basic game state test variables.

    def step(self, obs):
        super(AiBot, self).step(obs)

        # Basic game state test.

        if self.action_finished:
            self.action_finished = False
            if self.selector == "attackSelector":
                self.action_data.append((self.selector, self.doAttack, self.steps, self.marine_count))
                print((self.selector, self.doAttack, self.steps, self.marine_count))

        # End of basic game state test.

        # first step
        if obs.first():
            self.steps = 0    # Räknaren resettas inte mellan games/episoder. Vet ej om detta är en bra lösning.
            start_y, start_x = (obs.observation.feature_minimap.player_relative
                                == features.PlayerRelative.SELF).nonzero()
            xmean = start_x.mean()
            ymean = start_y.mean()

            self.base_location = (xmean, ymean)

            if xmean <= 31 and ymean <= 31:
                self.start_top = True
                self.attack_coordinates = Coordinates.START_LOCATIONS[1]
            else:
                self.start_top = False
                self.attack_coordinates = Coordinates.START_LOCATIONS[0]

        free_supply = (obs.observation.player.food_cap -
                       obs.observation.player.food_used)
        action = [actions.FUNCTIONS.no_op()]
        if self.reqSteps == 0:
            if self.steps < 16*60*5/5*1.4:  # 16 steps per sekund, men kompenserar också för att step_mul = 5. 1.4 kompenserar för in-game time.
                self.selector = 'buildSelector'
            else:
                self.selector = random.choice(selectors)

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

            elif self.doBuild == "no_op":
                BuildOrderController.no_op(self, obs, self.reqSteps)
                action = ActionSingelton().get_action()

        elif self.selector == "attackSelector":

            # Här kommer en bit kod som alltid räknar armén innan attackSelector väljer en action. Tar 2 steps.
            if self.reqSteps == 0:
                ArmyControlController.count_army(self, obs)    # count_army sets self.reqSteps = -1
                action = ActionSingelton().get_action()
            elif self.reqSteps == -1:    # Fulhackar lite med negativ reqSteps. Se ArmyControl.count_army.
                self.reqSteps = 0
                random_action = random.random()
                if random_action < 0.15:
                    self.doAttack = "attack"
                elif random_action < 0.16:
                    self.doAttack = "retreat"
                elif random_action < 0.16:    # Scouting is disabled
                    self.doAttack = "scout"
                else:
                    self.doAttack = "no_op"    # Kanske bra att vikta selectorn också.

            if self.doAttack == "attack":
                ArmyControlController.attack(self, obs)
                action = ActionSingelton().get_action()

            if self.doAttack == "retreat":
                ArmyControlController.retreat(self, obs)
                action = ActionSingelton().get_action()

            if self.doAttack == "scout":
                ArmyControlController.scout(self, obs)
                action = ActionSingelton().get_action()

            if self.doAttack == "no_op":
                ArmyControlController.no_op(self, obs, self.reqSteps)
                action = ActionSingelton().get_action()

        return action[0]

