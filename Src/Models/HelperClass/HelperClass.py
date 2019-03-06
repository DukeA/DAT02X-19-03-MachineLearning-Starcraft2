from pysc2.agents import base_agent
from pysc2.lib import actions, units, features
import numpy as np
from Models.BuildOrders.ActionSingelton import ActionSingelton
from Models.Predefines.Coordinates import Coordinates
import random

class HelperClass(base_agent.BaseAgent):

    #Moves to camera to a self.base_location
    def move_camera_to_base_location(self, obs):
        return actions.FUNCTIONS.move_camera(self.base_location)

    def sigma(self, num):
        if num <= 0:
            return 0
        elif num >= 83:
            return 83
        else:
            return num

    def select_scv(self, obs):
        new_action = [actions.FUNCTIONS.no_op()]
        command_scv = HelperClass.get_units(self, obs, units.Terran.SCV)
        if len(command_scv) > 0 and not HelperClass.is_unit_selected(self, obs, units.Terran.SCV):
            if obs.observation.player.idle_worker_count > 0:
                new_action = [actions.FUNCTIONS.select_idle_worker(
                    "select", obs, units.Terran.SCV)]
            else:
                command = random.choice(command_scv)
                new_action = [actions.FUNCTIONS.select_point(
                    "select", (HelperClass.sigma(self, command.x),
                               HelperClass.sigma(self, command.y)))]
        return new_action

    def is_unit_selected(self, obs, unit_type):
        if (len(obs.observation.single_select) > 0 and
                obs.observation.single_select[0].unit_type == unit_type):
            return True

        if (len(obs.observation.multi_select) > 0 and
                obs.observation.multi_select[0].unit_type == unit_type):
            return True

        return False

    def not_in_queue(self, obs, unit_type):
        queues = obs.observation.build_queue
        if len(queues) > 0:
            for queue in queues:
                if queue[0] == unit_type:
                    return False
        return True

    def do_action(self, obs, action):
        return action in obs.observation.available_actions

    def not_in_progress(self, obs, unit_type):
        units = HelperClass.get_units(self, obs, unit_type)
        for unit in units:
            if (unit.build_progress != 100):
                return False
        return True

    def get_units(self, obs, unit_type):
        return [unit for unit in obs.observation.feature_units
                if unit.unit_type == unit_type]

    def no_op(self, obs):

        new_action = [actions.FUNCTIONS.no_op()]

        if self.reqSteps == 0:
            self.reqSteps = 2

        if self.reqSteps == 2:
            self.reqSteps = 1

        elif self.reqSteps == 1:
            self.reqSteps = 0

        ActionSingelton().set_action(new_action)

    def place_building(self, obs, building_type, *coordinates):

        new_action = [actions.FUNCTIONS.no_op()]

        if len(coordinates) == 0:
            coordinates = (random.randint(2, 81), random.randint(2, 81))

        action_types = {
            units.Terran.Barracks: actions.FUNCTIONS.Build_Barracks_screen,
            units.Terran.SupplyDepot: actions.FUNCTIONS.Build_SupplyDepot_screen,
            units.Terran.Refinery: actions.FUNCTIONS.Build_Refinery_screen,
            units.Terran.CommandCenter: actions.FUNCTIONS.Build_CommandCenter_screen,
            units.Terran.Factory: actions.FUNCTIONS.Build_Factory_screen,
            units.Terran.Starport: actions.FUNCTIONS.Build_Starport_screen
        }

        build_screen_action = action_types.get(building_type, actions.FUNCTIONS.Build_SupplyDepot_screen)

        if HelperClass.not_in_progress(self, obs, building_type):
            if HelperClass.is_unit_selected(self, obs, units.Terran.SCV):
                if HelperClass.do_action(self, obs, build_screen_action.id):
                    new_action = [build_screen_action("now",
                                                      (HelperClass.sigma(self, coordinates[0]),
                                                       HelperClass.sigma(self, coordinates[1])))]

        return new_action
