from Models.BuildOrders.DistributeSCV import DistributeSCV
from pysc2.agents import base_agent
from pysc2.lib import actions, features, units

from Models.BuildOrders.BuildOrdersController import BuildOrdersController
from Models.BuildOrders.UnitBuildOrdersController import UnitBuildOrdersController
from Models.BuildOrders.ActionSingleton import ActionSingleton
from Models.BuildNetwork.BuildFacade import BuildFacade
from Models.BuildNetwork.Network.BuildNetwork import BuildNetwork
from Models.BuildNetwork.Network.Buildsingelton import Buildsingelton
from Models.ArmyControl.ArmyControlController import ArmyControlController
from Models.Predefines.Coordinates import Coordinates
from Models.Selector.selector import Selector
from Models.HelperClass.HelperClass import HelperClass
from Models.BotFile.State import State
from Models.MachineLearning.ActorCriticAgent import ActorCriticAgent

import os
import pickle
import tensorflow as tf


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
        self.next_action = None
        self.earlier_action = None
        self.DistributeSCVInstance = None
        self.actor_critic_agent = None
        self.game_state = None
        self.game_state_updated = False

        # Basic game state test variables.

        self.last_scout = 0        # Maybe for ML
        self.marine_count = 0      # Maybe for ML
        self.action_finished = False
        self.attacking = False

        self.oldScore = 0
        self.epsilon = 0
        self.build_space = 0
        self.episodes = 0
        self.Batch_Size = 32
        self.action_state = []
        self.memory_Buffer = []
        self.prev_state = []
        self.prev_actions = []
        self.building_location = []
        self.sess = tf.Session()
        self.actions_softmax = 0
        self.build_location = ()


    def save_game(self, path, episode):
        offset = 0
        while os.path.exists(path + str(episode)+str(offset)+".txt"):
            offset += 1
        with open(path + str(episode)+str(offset)+".txt", 'wb') as filehandle:
            pickle.dump(self.game_state.get_state(), filehandle)

    def step(self, obs, epsilon, episode):
        super(AiBot, self).step(obs)
        self.epsilon = epsilon
        self.episode = episode


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
                self.base_location = Coordinates.START_LOCATIONS[0]
            else:
                self.start_top = False
                self.attack_coordinates = Coordinates.START_LOCATIONS[0]
                self.base_location = Coordinates.START_LOCATIONS[1]

            self.game_state = State(self)

        HelperClass.find_the_camera_postion(self, obs)

        if HelperClass.check_building_at_position(self,obs, Buildsingelton().get_location()):
            HelperClass.move_camera_to_base_location(self, obs)
            self.build_States = BuildFacade.set_up(self, obs, self.base_location)

            self.build_state_reward = self.build_States[0][0]
            self.build_state = self.build_States[0][1]
            Buildsingelton().set_location(self.build_state[0][0], self.build_state[0][1])

            self.action_state = self.build_States[0][2]

            self.old_score = self.build_States[1]

            self.build_state = self.build_States[2]
            self.build_space = len(self.build_state)



            #self.build_network = BuildNetwork(self.build_state_reward,self.build_state, self.action_state, epsilon)

            #BuildNetwork.predict_neural_network(self.build_network, self.build_States)



        self.build_location = Buildsingelton().get_location()

        action = [actions.FUNCTIONS.no_op()]

        if self.reqSteps == 0 or self.reqSteps == -1:
            self.earlier_action = self.next_action
            self.next_action = Selector.selector(self, obs)

        if self.next_action == "updateState":
            self.game_state.update_state(self, obs)
            action = ActionSingleton().get_action()

        if self.next_action == "expand":
            BuildOrdersController.build_expand(self, obs)
            action = ActionSingleton().get_action()

        elif self.next_action == "build_scv":  # build scv
            UnitBuildOrdersController.build_scv(self, obs)
            action = ActionSingleton().get_action()

        elif self.next_action == "distribute_scv":  # Har inte gjort någon controller än
            if self.reqSteps == 0:
                self.DistributeSCVInstance = DistributeSCV()
            self.DistributeSCVInstance.distribute_scv(self, obs, self.base_location)
            action = ActionSingleton().get_action()

        elif self.next_action == "build_supply_depot":  # build supply depot
            BuildOrdersController.build_supply_depot(self, obs,self.build_location)
            action = ActionSingleton().get_action()


        elif self.next_action == "build_barracks":
            BuildOrdersController.build_barracks(self, obs,self.build_location)
            action = ActionSingleton().get_action()


        elif self.next_action == "build_refinery":
            BuildOrdersController.build_refinery(self, obs)
            action = ActionSingleton().get_action()

        elif self.next_action == "return_scv":
            BuildOrdersController.return_scv(self, obs)
            action = ActionSingleton().get_action()

        elif self.next_action == "build_marine":
            UnitBuildOrdersController.train_marines(self, obs)
            action = ActionSingleton().get_action()

        elif self.next_action == "build_marauder":
            UnitBuildOrdersController.train_marauder(self, obs)
            action = ActionSingleton().get_action()

        elif self.next_action == "build_reaper":
            UnitBuildOrdersController.train_reaper(self, obs)
            action = ActionSingleton().get_action()

        elif self.next_action == "build_hellion":
            UnitBuildOrdersController.train_hellion(self, obs)
            action = ActionSingleton().get_action()

        elif self.next_action == "build_medivac":
            UnitBuildOrdersController.train_medivac(self, obs)
            action = ActionSingleton().get_action()

        elif self.next_action == "build_viking":
            UnitBuildOrdersController.train_viking(self, obs)
            action = ActionSingleton().get_action()

        elif self.next_action == "army_count":
            ArmyControlController.count_army(self, obs)
            action = ActionSingleton().get_action()

        elif self.next_action == "attack":
            ArmyControlController.attack(self, obs)
            action = ActionSingleton().get_action()

        elif self.next_action == "build_factory":
            BuildOrdersController.build_factory(self, obs)
            action = ActionSingleton().get_action()

        elif self.next_action == "build_starport":
            BuildOrdersController.build_starport(self, obs)
            action = ActionSingleton().get_action()

        elif self.next_action == "build_tech_lab_barracks":
            BuildOrdersController.build_tech_lab_barracks(self, obs)
            action = ActionSingleton().get_action()

        elif self.next_action == "retreat":
            ArmyControlController.retreat(self, obs)
            action = ActionSingleton().get_action()

        elif self.next_action == "scout":
            ArmyControlController.scout(self, obs)
            action = ActionSingleton().get_action()

        elif self.next_action == "transform_vikings_to_ground":
            ArmyControlController.transform_vikings_to_ground(self, obs)
            action = ActionSingleton().get_action()

        elif self.next_action == "transform_vikings_to_air":
            ArmyControlController.transform_vikings_to_air(self, obs)
            action = ActionSingleton().get_action()

        elif self.next_action == "no_op":
            HelperClass.no_op(self, obs)
            action = ActionSingleton().get_action()

        return action[0]
