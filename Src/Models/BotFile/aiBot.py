from pysc2.agents import base_agent
from pysc2.lib import actions, features, units

from Models.BuildOrders.BuildOrdersController import BuildOrdersController
from Models.BuildOrders.UnitBuildOrdersController import UnitBuildOrdersController
from Models.BuildOrders.ActionSingleton import ActionSingleton
from Models.BuildOrders.DistributeSCV import DistributeSCV
from Models.ArmyControl.ArmyControlController import ArmyControlController
from Models.Predefines.Coordinates import Coordinates
from Models.Selector.selector import Selector
from Models.HelperClass.HelperClass import HelperClass
from Models.BotFile.State import State
from Models.Selector.HardCodedSelector import HardCodedSelector
from Models.MachineLearning.ImitationAgent import ImitationAgent
import keras
import tensorflow as tf
import os
import pickle
import numpy as np
import random


class AiBot(base_agent.BaseAgent):

    model = tf.keras.models.load_model("C:/Users/Claes/Desktop/DAT02X-19-03-MachineLearning-Starcraft2/Src/imitation_models/test.h5", compile=True)

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
        self.game_state = None
        self.game_state_updated = False
        self.action_finished = False
        self.attacking = False
        self.hasStarport = False
        self.hasTechlab = False
        self.hasFactory = False
        self.hasBarrack = False
        self.imitation_agent = None

    def save_game(self, path1, path2, path3, path4,
        path6, path7, path8, path9, path10, path11, path12, 
        path13, path14, path15, path16, path18,
        episode):
        offset = 0
      
        while os.path.exists(path1 + str(episode)+str(offset)+".txt"):
            offset += 1
        with open(path1 + str(episode)+str(offset)+".txt", 'wb') as filehandle:
            pickle.dump(self.game_state.get_state_no_op(), filehandle)
        
        while os.path.exists(path2 + str(episode)+str(offset)+".txt"):
            offset += 1
        with open(path2 + str(episode)+str(offset)+".txt", 'wb') as filehandle:
            pickle.dump(self.game_state.get_state_build_scv(), filehandle)
     
        
        while os.path.exists(path3 + str(episode)+str(offset)+".txt"):
            offset += 1
        with open(path3 + str(episode)+str(offset)+".txt", 'wb') as filehandle:
            pickle.dump(self.game_state.get_state_build_supply_depot(), filehandle)


        while os.path.exists(path4 + str(episode)+str(offset)+".txt"):
            offset += 1
        with open(path4 + str(episode)+str(offset)+".txt", 'wb') as filehandle:
            pickle.dump(self.game_state.get_state_build_marine(), filehandle)
        
        while os.path.exists(path6 + str(episode)+str(offset)+".txt"):
            offset += 1
        with open(path6 + str(episode)+str(offset)+".txt", 'wb') as filehandle:
            pickle.dump(self.game_state.get_state_build_reaper(), filehandle)


        while os.path.exists(path7 + str(episode)+str(offset)+".txt"):
            offset += 1
        with open(path7 + str(episode)+str(offset)+".txt", 'wb') as filehandle:
            pickle.dump(self.game_state.get_state_build_hellion(), filehandle)
        

        while os.path.exists(path8 + str(episode)+str(offset)+".txt"):
            offset += 1
        with open(path8 + str(episode)+str(offset)+".txt", 'wb') as filehandle:
            pickle.dump(self.game_state.get_state_build_medivac(), filehandle)
     
        
        while os.path.exists(path9 + str(episode)+str(offset)+".txt"):
            offset += 1
        with open(path9 + str(episode)+str(offset)+".txt", 'wb') as filehandle:
            pickle.dump(self.game_state.get_state_build_viking(), filehandle)


        while os.path.exists(path10 + str(episode)+str(offset)+".txt"):
            offset += 1
        with open(path10 + str(episode)+str(offset)+".txt", 'wb') as filehandle:
            pickle.dump(self.game_state.get_state_build_barracks(), filehandle)
        

        while os.path.exists(path11 + str(episode)+str(offset)+".txt"):
            offset += 1
        with open(path11 + str(episode)+str(offset)+".txt", 'wb') as filehandle:
            pickle.dump(self.game_state.get_state_build_refinery(), filehandle)
     
        
        while os.path.exists(path12 + str(episode)+str(offset)+".txt"):
            offset += 1
        with open(path12 + str(episode)+str(offset)+".txt", 'wb') as filehandle:
            pickle.dump(self.game_state.get_state_retreat(), filehandle)


        while os.path.exists(path13 + str(episode)+str(offset)+".txt"):
            offset += 1
        with open(path13 + str(episode)+str(offset)+".txt", 'wb') as filehandle:
            pickle.dump(self.game_state.get_state_return_scv(), filehandle)
        

        while os.path.exists(path14 + str(episode)+str(offset)+".txt"):
            offset += 1
        with open(path14 + str(episode)+str(offset)+".txt", 'wb') as filehandle:
            pickle.dump(self.game_state.get_state_expand(), filehandle)
     
        
        while os.path.exists(path15 + str(episode)+str(offset)+".txt"):
            offset += 1
        with open(path15 + str(episode)+str(offset)+".txt", 'wb') as filehandle:
            pickle.dump(self.game_state.get_state_build_factory(), filehandle)


        while os.path.exists(path16 + str(episode)+str(offset)+".txt"):
            offset += 1
        with open(path16 + str(episode)+str(offset)+".txt", 'wb') as filehandle:
            pickle.dump(self.game_state.get_state_build_starport(), filehandle)
        
        
        while os.path.exists(path18 + str(episode)+str(offset)+".txt"):
            offset += 1
        with open(path18 + str(episode)+str(offset)+".txt", 'wb') as filehandle:
            pickle.dump(self.game_state.get_state_attack(), filehandle)
     
      

    def step(self, obs):
        super(AiBot, self).step(obs)

        # first step
        if obs.first():
            # Räknaren resettas inte mellan games/episoder. Vet ej om detta är en bra lösning.
            self.steps = 0
            self.reward = 0
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

            self.game_state = State()
            # The command center isn't actually in the center of the screen!
            self.game_state.add_unit_in_progress(
                self, self.base_location, (42, 42), units.Terran.CommandCenter.value)

        action = [actions.FUNCTIONS.no_op()]

        if self.reqSteps == 0 or self.reqSteps == -1:
            self.earlier_action = self.next_action
            if self.reqSteps == 0 and not self.game_state_updated:
                self.next_action = "updateState"
            else:
                self.game_state_updated = False
                state = np.asarray(self.game_state.get_normalized_game_state(self, obs))
                prediction = self.model.predict(np.asarray([state]))[0]
                
                prediction_list = []
                for i in range(1): #if you want to random between highest predicted actions set range higher
                    index = np.argmax(prediction)
                    prediction_list.append(index)
                    prediction[index] = 0.0

                choice = random.choice(prediction_list)
                if choice == 0:
                    self.next_action = "attack"
                elif choice == 1:
                    self.next_action = "build_barracks"
                elif choice == 2:
                    self.next_action = "build_factory"
                elif choice == 3:
                    self.next_action = "build_hellion"
                elif choice == 4:
                    self.next_action = "build_marine"
                elif choice == 5:
                    self.next_action = "build_medivac"
                elif choice == 6:
                    self.next_action = "build_reaper"
                elif choice == 7:
                    self.next_action = "build_refinery"
                elif choice == 8:
                    self.next_action = "build_scv"
                elif choice == 9:
                    self.next_action = "build_starport"
                elif choice == 10:
                    self.next_action = "build_supply_depot"
                elif choice == 11:
                    self.next_action = "build_viking"
                elif choice == 12:
                    self.next_action = "expand"
                elif choice == 13:
                    self.next_action = "no_op"
                elif choice == 14:
                    self.next_action = "retreat"
                elif choice == 15:
                    self.next_action = "return_scv" 
                else:
                    print("no_op")
                    self.next_action = "no_op"

        if self.next_action == "updateState":
            self.game_state.update_state(self, obs)
            action = ActionSingleton().get_action()

        if self.next_action == "expand":
            BuildOrdersController.build_expand(self, obs)
            action = ActionSingleton().get_action()

        elif self.next_action == "build_scv": # build scv
            UnitBuildOrdersController.build_scv(self, obs)
            action = ActionSingleton().get_action()

        elif self.next_action == "distribute_scv":  # Har inte gjort någon controller än
            if self.reqSteps == 0:
                self.DistributeSCVInstance = DistributeSCV()
            self.DistributeSCVInstance.distribute_scv(self, obs, self.base_location)
            action = ActionSingleton().get_action()

        elif self.next_action == "build_supply_depot":  # build supply depot
            BuildOrdersController.build_supply_depot(self, obs)
            action = ActionSingleton().get_action()

        elif self.next_action == "build_barracks":
            BuildOrdersController.build_barracks(self, obs)
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
