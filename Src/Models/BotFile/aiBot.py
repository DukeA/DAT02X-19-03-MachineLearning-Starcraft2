

from pysc2.agents import base_agent
from pysc2.lib import actions, features

from Models.BuildOrders.BuildOrderController import BuildOrderController
from Models.BuildOrders.UnitBuildOrdersController import UnitBuildOrdersController
from Models.BuildOrders.ActionSingelton import ActionSingelton
from Models.ArmyControl.ArmyControlController import ArmyControlController
from Models.Predefines.Coordinates import Coordinates
from Models.Selector.selector import Selector
from Models.HelperClass.HelperClass import HelperClass

selectors = ['buildSelector', 'attackSelector']
# Might be unnecessary depending on implementation of randomness
attackSelector = ['attack', 'retreat', 'scout', 'count_army', 'no_op']
buildSelector = ['build_scv', 'build_supply_depot', "build_marine",
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
        # Does this persist between loops? It's a tuple (selector, action, steps, marine_count)
        self.action_data = []

        # End of basic game state test variables.

    def step(self, obs):
        super(AiBot, self).step(obs)

        # Basic game state test.

        if self.action_finished:
            self.action_finished = False
            if self.selector == "attackSelector":
                self.action_data.append((self.selector, self.doAttack,
                                         self.steps, self.marine_count))
                print((self.selector, self.doAttack, self.steps, self.marine_count))

        # End of basic game state test.

        # first step
        if obs.first():
            # Räknaren resettas inte mellan games/episoder. Vet ej om detta är en bra lösning.
            self.steps = 0
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

        if self.reqSteps == 0 or self.reqSteps == -1:
            self.next_action = Selector.selector(self)

        print(self.reqSteps)
        print(self.next_action)
        if self.next_action == "expand":
            BuildOrderController.build_expand(self, obs, self.start_top)
            action = ActionSingelton().get_action()

        elif self.next_action == "build_scv":  # build scv
            BuildOrderController.build_scv(self, obs, free_supply)
            action = ActionSingelton().get_action()

        elif self.next_action == "build_supply_depot":  # build supply depot
            BuildOrderController.build_supplaydepot(self, obs, free_supply)
            action = ActionSingelton().get_action()

        elif self.next_action == "build_barracks":
            BuildOrderController.build_barracks(self, obs)
            action = ActionSingelton().get_action()

        elif self.next_action == "build_refinery":
            BuildOrderController.build_refinary(self, obs)
            action = ActionSingelton().get_action()

        elif self.next_action == "return_scv":
            BuildOrderController.return_scv(self, obs)
            action = ActionSingelton().get_action()

        elif self.next_action == "build_marine":
            UnitBuildOrdersController.train_marines(self, obs, free_supply)
            action = ActionSingelton().get_action()

        elif self.next_action == "build_marauder":
            UnitBuildOrdersController.train_marauder(self, obs, free_supply)
            action = ActionSingelton().get_action()

        elif self.next_action == "build_medivac":
            UnitBuildOrdersController.train_medivac(self, obs, free_supply)
            action = ActionSingelton().get_action()

        elif self.next_action == "army_count":
            ArmyControlController.count_army(self, obs)
            action = ActionSingelton().get_action()

        elif self.next_action == "attack":
            ArmyControlController.attack(self, obs)
            action = ActionSingelton().get_action()

        elif self.next_action == "retreat":
            ArmyControlController.retreat(self, obs)
            action = ActionSingelton().get_action()

        elif self.next_action == "scout":
            ArmyControlController.scout(self, obs)
            action = ActionSingelton().get_action()

        elif self.next_action == "no_op":
            HelperClass.no_op(self, obs)
            action = ActionSingelton().get_action()

        return action[0]
