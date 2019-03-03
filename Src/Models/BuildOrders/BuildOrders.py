import random

from pysc2.agents import base_agent
from pysc2.lib import actions, units

from Models.Predefines.Coordinates import Coordinates
from Models.BuildOrders.ActionSingleton import ActionSingelton
from Models.BuildOrders.IsPossible import IsPossible

"""
The Class belongs to the Build Order request 
to build certain elements such as supply depots and
refinarys.  
"""


class BuildOrders(base_agent.BaseAgent):
    def __init__(self):
        super(BuildOrders, self).__init__()
        self.expo_loc = 0
        self.new_action = None

    def build_barracks(self, obs):

        new_action = [actions.FUNCTIONS.no_op()]

        if IsPossible.build_barracks_possible(self, obs):
            if self.reqSteps == 0:
                self.reqSteps = 3

            if self.reqSteps == 3:
                new_action = [
                    actions.FUNCTIONS.move_camera(self.base_location)]

            elif self.reqSteps == 2:
                new_action = BuildOrders.select_scv(self, obs)

            elif self.reqSteps == 1:
                new_action = BuildOrders.place_building(self, obs, units.Terran.Barracks)

            self.reqSteps -= 1

        ActionSingelton().set_action(new_action)

    def build_supply_depot(self, obs, free_supply):

        new_action = [actions.FUNCTIONS.no_op()]

        if IsPossible.build_supply_depot_possible(self, obs):
            if self.reqSteps == 0:
                self.reqSteps = 3

            if self.reqSteps == 3:
                new_action = [
                    actions.FUNCTIONS.move_camera(self.base_location)]

            elif self.reqSteps == 2:
                new_action = BuildOrders.select_scv(self, obs)

            elif self.reqSteps == 1:
                new_action = BuildOrders.place_building(self, obs, units.Terran.SupplyDepot)

            self.reqSteps -= 1

        ActionSingelton().set_action(new_action)

    def build_refinery(self, obs):

        new_action = [actions.FUNCTIONS.no_op()]

        if IsPossible.build_refinery_possible(self, obs):

            if self.reqSteps == 0:
                self.reqSteps = 3

            if self.reqSteps == 3:
                new_action = [
                    actions.FUNCTIONS.move_camera(self.base_location)]

            elif self.reqSteps == 2:
                new_action = BuildOrders.select_scv(self, obs)

            elif self.reqSteps == 1:
                geyser = BuildOrders.get_units(self, obs, units.Neutral.VespeneGeyser)

                new_action = BuildOrders.place_building(self, obs, units.Terran.Refinery, geyser[0].x, geyser[0].y)

            self.reqSteps -= 1
        ActionSingelton().set_action(new_action)

    def return_scv(self, obs):
        new_action = [actions.FUNCTIONS.no_op()]
        if self.reqSteps == 0:
            self.reqSteps = 3

        elif self.reqSteps == 3:
            if obs.observation.player.idle_worker_count > 0:
                new_action = [actions.FUNCTIONS.select_idle_worker(
                    "select", obs, units.Terran.SCV)]

        elif self.reqSteps == 2:
            new_action = [
                actions.FUNCTIONS.move_camera(self.base_location)]

        elif self.reqSteps == 1:
            if BuildOrders.is_unit_selected(self, obs, units.Terran.SCV):
                minerals = BuildOrders.get_units(self, obs, units.Neutral.MineralField)
                new_action = [actions.FUNCTIONS.Harvest_Gather_screen(
                    "now", (BuildOrders.sigma(self, minerals[0].x),
                            BuildOrders.sigma(self, minerals[0].y)))]

        self.reqSteps -= 1
        ActionSingelton().set_action(new_action)

    def expand(self, obs, top_start):

        new_action = [actions.FUNCTIONS.no_op()]

        if IsPossible.build_command_center_possible(self, obs):  # check if it is possible

            if self.reqSteps == 0:
                self.expo_loc = 0
                self.reqSteps = 4

            if self.reqSteps == 4:  # move to base
                new_action = [
                    actions.FUNCTIONS.move_camera(self.base_location)]

            elif self.reqSteps == 3:  # select scv
                new_action = BuildOrders.select_scv(self, obs)

            elif self.reqSteps == 2:  # move to expansion location
                target = BuildOrders.choose_location(self, top_start)
                new_action = [
                    actions.FUNCTIONS.move_camera(target)]

            elif self.reqSteps == 1:  # check if there is a commandcenter there if there is move to the next location or build one
                command_center = BuildOrders.get_units(self, obs, units.Terran.CommandCenter)
                if len(command_center) > 0:
                    if len(Coordinates.EXPO_LOCATIONS) >= self.expo_loc+1:
                        self.reqSteps = 2
                        self.expo_loc += 1
                        if self.expo_loc < len(Coordinates.CC_LOCATIONS):
                            target = BuildOrders.choose_location(self, top_start)
                            new_action = [
                                actions.FUNCTIONS.move_camera(target)]
                        else:
                            self.reqSteps = 1
                else:
                    target = BuildOrders.choose_screen_location(self, top_start)
                    new_action = BuildOrders.place_building(self, obs, units.Terran.CommandCenter, target[0], target[1])

            self.reqSteps -= 1

        ActionSingelton().set_action(new_action)

    def choose_screen_location(self, top_start):  # returns a location based on the start location
        if top_start:
            return Coordinates().CC_LOCATIONS[self.expo_loc]
        else:
            return Coordinates().CC_LOCATIONS2[self.expo_loc]

    def choose_location(self, top_start):
        # returns a location based on the start location
        if top_start:
            return Coordinates().EXPO_LOCATIONS[self.expo_loc]
        else:
            return Coordinates().EXPO_LOCATIONS2[self.expo_loc]

    def sigma(self, num):
        if num <= 0:
            return 0
        elif num >= 83:
            return 83
        else:
            return num

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
        units = BuildOrders.get_units(self, obs, unit_type)
        for unit in units:
            if unit.build_progress != 100:
                return False
        return True

    def get_units(self, obs, unit_type):
        return [unit for unit in obs.observation.feature_units
                if unit.unit_type == unit_type]

    def is_unit_selected(self, obs, unit_type):
        if (len(obs.observation.single_select) > 0 and
                obs.observation.single_select[0].unit_type == unit_type):
            return True

        if (len(obs.observation.multi_select) > 0 and
                obs.observation.multi_select[0].unit_type == unit_type):
            return True

        return False

    def select_scv(self, obs):

        new_action = [actions.FUNCTIONS.no_op()]
        command_scv = BuildOrders.get_units(self, obs, units.Terran.SCV)

        if len(command_scv) > 0 and not BuildOrders.is_unit_selected(self, obs, units.Terran.SCV):

            if obs.observation.player.idle_worker_count > 0:
                new_action = [actions.FUNCTIONS.select_idle_worker(
                    "select", obs, units.Terran.SCV)]

            else:
                command = random.choice(command_scv)
                new_action = [actions.FUNCTIONS.select_point(
                    "select", (BuildOrders.sigma(self, command.x),
                               BuildOrders.sigma(self, command.y)))]

        return new_action

    def place_building(self, obs, building_type, *coordinates):

        new_action = [actions.FUNCTIONS.no_op()]

        if len(coordinates) == 0:
            coordinates = (random.randint(2, 81), random.randint(2, 81))

        action_types = {
            units.Terran.Barracks: actions.FUNCTIONS.Build_Barracks_screen,
            units.Terran.SupplyDepot: actions.FUNCTIONS.Build_SupplyDepot_screen,
            units.Terran.Refinery: actions.FUNCTIONS.Build_Refinery_screen,
            units.Terran.CommandCenter: actions.FUNCTIONS.Build_CommandCenter_screen
        }

        build_screen_action = action_types.get(building_type, actions.FUNCTIONS.Build_SupplyDepot_screen)

        if BuildOrders.not_in_progress(self, obs, building_type):
            if BuildOrders.is_unit_selected(self, obs, units.Terran.SCV):
                if BuildOrders.do_action(self, obs, build_screen_action.id):

                    new_action = [build_screen_action("now",
                                                      (BuildOrders.sigma(self, coordinates[0]),
                                                       BuildOrders.sigma(self, coordinates[1])))]

        return new_action
