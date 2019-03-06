import random

from pysc2.agents import base_agent
from pysc2.lib import actions, units

from Models.Predefines.Coordinates import Coordinates
from Models.BuildOrders.ActionSingleton import ActionSingleton
from Models.HelperClass.HelperClass import HelperClass
from Models.HelperClass.IsPossible import IsPossible

"""
The Class belongs to the Build Order request
to build certain elements such as supply depots and
refineries.
"""


class BuildOrders(base_agent.BaseAgent):
    def __init__(self):
        super(BuildOrders, self).__init__()
        self.base_location = None
        self.expo_loc = 0
        self.new_action = None

        """
            @Author:Arvid , revised :Adam Grandén
            @:param The parameter would be  self which is a aibot
            @:param The other would be the observable universe
            This method would be the barracks which builds the barrack from the start of the base_location
            and gets an instance where to build that barrack on that location.

        """

    def build_barracks(self, obs):
        new_action = [actions.FUNCTIONS.no_op()]

        if IsPossible.build_barracks_possible(self, obs):
            if self.reqSteps == 0:
                self.reqSteps = 3

            if self.reqSteps == 3:
                new_action = [actions.FUNCTIONS.move_camera(self.base_location)]

            elif self.reqSteps == 2:
                new_action = HelperClass.select_scv(self, obs)

            elif self.reqSteps == 1:
                coordinates = BuildOrders.find_placement(self, obs, 6, maximum_searches=10, sampling_size=9)

                if coordinates is not None:
                    new_action = HelperClass.place_building(self, obs, units.Terran.Barracks, coordinates[0], coordinates[1])

            self.reqSteps -= 1
        ActionSingleton().set_action(new_action)

    def build_supply_depot(self, obs, free_supply):
        new_action = [actions.FUNCTIONS.no_op()]

        if IsPossible.build_supply_depot_possible(self, obs):
            if self.reqSteps == 0:
                self.reqSteps = 3

            if self.reqSteps == 3:
                new_action = [actions.FUNCTIONS.move_camera(self.base_location)]

            if self.reqSteps == 2:
                new_action = HelperClass.select_scv(self, obs)

            elif self.reqSteps == 1:
                new_action = HelperClass.place_building(self, obs, units.Terran.SupplyDepot)

            self.reqSteps -= 1
        ActionSingleton().set_action(new_action)

    def build_refinery(self, obs):
        new_action = [actions.FUNCTIONS.no_op()]

        if IsPossible.build_refinery_possible(self, obs):
            if self.reqSteps == 0:
                self.reqSteps = 3

            if self.reqSteps == 3:
                new_action = [actions.FUNCTIONS.move_camera(self.base_location)]

            elif self.reqSteps == 2:
                new_action = HelperClass.select_scv(self, obs)

            elif self.reqSteps == 1:
                geyser = HelperClass.get_units(self, obs, units.Neutral.VespeneGeyser)
                new_action = HelperClass.place_building(self, obs, units.Terran.Refinery, geyser[0].x, geyser[0].y)

            self.reqSteps -= 1
        ActionSingleton().set_action(new_action)

    def return_scv(self, obs):
        new_action = [actions.FUNCTIONS.no_op()]
        if self.reqSteps == 0:
            self.reqSteps = 3

        elif self.reqSteps == 3:
            self.reqSteps = 2
            if(obs.observation.player.idle_worker_count > 0):
                new_action = [actions.FUNCTIONS.select_idle_worker(
                    "select", obs, units.Terran.SCV)]

        elif self.reqSteps == 2:
            self.reqSteps = 1
            new_action = [
                HelperClass.move_camera_to_base_location(self, obs)]

        elif self.reqSteps == 1:
            self.reqSteps = 0
            if HelperClass.is_unit_selected(self, obs, units.Terran.SCV):
                minerals = HelperClass.get_units(self, obs, units.Neutral.MineralField)
                new_action = [actions.FUNCTIONS.Harvest_Gather_screen(
                    "now", (HelperClass.sigma(self, minerals[0].x),
                            HelperClass.sigma(self, minerals[0].y)))]
        ActionSingleton().set_action(new_action)

    """
        @Author Adam Grandén
        @:param self- Object aibot
        @:param obs - the observable universe
        The following code is the action for building an factory this is made from taking the builder
        then move to the loaction and then get if there was any  other factories being built and return
        a new build for factory.
    """

    def build_factory(self, obs):
        new_action = [actions.FUNCTIONS.no_op()]

        if IsPossible.build_factory_possible(self, obs):
            if self.reqSteps == 0:
                self.reqSteps = 3

            elif self.reqSteps == 3:
                new_action = [actions.FUNCTIONS.move_camera(self.base_location)]

            elif self.reqSteps == 2:
                new_action = HelperClass.select_scv(self, obs)

            elif self.reqSteps == 1:
                new_action = HelperClass.place_building(self, obs, units.Terran.Factory)
            self.reqSteps -= 1
        ActionSingleton().set_action(new_action)

        """
            @Author Adam Grandén
            @:param self-Object aibot
            @:param obs - the observable universe
            The following code is the action for building an Starport this is made from taking the builder
            then move to the loaction and then get if there was any  other factories being built and return
            a new build for starport.
        """

    def build_starport(self, obs):
        new_action = [actions.FUNCTIONS.no_op()]

        if IsPossible.build_starport_possible(self, obs):
            if self.reqSteps == 0:
                self.reqSteps = 3

            elif self.reqSteps == 3:
                new_action = [actions.FUNCTIONS.move_camera(self.base_location)]

            elif self.reqSteps == 2:
                new_action = HelperClass.select_scv(self, obs)

            elif self.reqSteps == 1:
                new_action = HelperClass.place_building(self, obs, units.Terran.Starport)

            self.reqSteps -= 1
        ActionSingleton().set_action(new_action)

        """
            @Author Adam Grandén
            @:param self- Object aibot
            @:param obs - the observable universe
            This code takes the  barracks which are located and then adds
            an  techlab when the building is built.
        """

    def upgrade_barracks(self, obs):
        new_action = [actions.FUNCTIONS.no_op()]
        barracks = HelperClass.get_units(self, obs, units.Terran.Barracks)

        if IsPossible.upgrade_barracks_possible(self, obs):
            if self.reqSteps == 0:
                self.reqSteps = 3

            elif self.reqSteps == 3:
                new_action = [
                    actions.FUNCTIONS.move_camera(self.base_location)]

            elif self.reqSteps == 2:
                if len(barracks) > 0 and HelperClass.not_in_progress(self, obs, units.Terran.Barracks):
                    new_action = [actions.FUNCTIONS.select_point("select",
                                                                 (HelperClass.sigma(self, barracks[0].x),
                                                                  HelperClass.sigma(self, barracks[0].y)))]
            elif self.reqSteps == 1:
                if len(barracks) > 0:
                    if HelperClass.is_unit_selected(self, obs, units.Terran.Barracks):
                        if HelperClass.do_action(self, obs, actions.FUNCTIONS.Build_TechLab_quick.id):
                            new_action = [actions.FUNCTIONS.Build_TechLab_quick("now")]
            self.reqSteps -= 1
        ActionSingleton().set_action(new_action)

    def expand(self, obs, top_start):
        new_action = [actions.FUNCTIONS.no_op()]
        if IsPossible.build_command_center_possible(self, obs):  # check if it is possible
            if self.reqSteps == 0:
                self.expo_loc = 0
                self.reqSteps = 4

            if self.reqSteps == 4:  # move to base
                new_action = [
                    HelperClass.move_camera_to_base_location(self, obs)]

            if self.reqSteps == 3:  # select scv
                command_scv = HelperClass.get_units(self, obs, units.Terran.SCV)
                if len(command_scv) > 0 and not HelperClass.is_unit_selected(self, obs, units.Terran.SCV):
                    if (obs.observation.player.idle_worker_count > 0):
                        new_action = [actions.FUNCTIONS.select_idle_worker(
                            "select", obs, units.Terran.SCV)]
                    else:
                        command = random.choice(command_scv)
                        new_action = [actions.FUNCTIONS.select_point(
                            "select", (HelperClass.sigma(self, command.x),
                                       HelperClass.sigma(self, command.y)))]

            if self.reqSteps == 2:  # move to expansion location
                target = BuildOrders.choose_location(self, top_start)
                new_action = [
                    actions.FUNCTIONS.move_camera(target)]

            if self.reqSteps == 1:  # check if there is a commandcenter there if there is move to the next location or build one
                command_center = HelperClass.get_units(self, obs, units.Terran.CommandCenter)
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
                    new_action = HelperClass.place_building(self, obs, units.Terran.CommandCenter, target[0], target[1])
                    if self.base_location[0] < 32:
                        expo_target = Coordinates.EXPO_LOCATIONS[self.expo_loc]
                    else:
                        expo_target = Coordinates.EXPO_LOCATIONS2[self.expo_loc]
                    self.game_state.add_unit_in_progress(self, expo_target, (42, 42),
                                                                 units.Terran.CommandCenter.value)
            self.reqSteps -= 1
        ActionSingleton().set_action(new_action)

    def choose_screen_location(self, top_start):  # returns a location based on the start location
        if top_start:
            return Coordinates().CC_LOCATIONS[self.expo_loc]
        else:
            return Coordinates().CC_LOCATIONS2[self.expo_loc]

    def choose_location(self, top_start):
        value = self.expo_loc
        # returns a location based on the start location
        if top_start:
            return Coordinates().EXPO_LOCATIONS[self.expo_loc]
        else:
            return Coordinates().EXPO_LOCATIONS2[self.expo_loc]

    def check_placement(self, obs, screen_coordinates, building_radius):
        """Checks if a location and a radius around it is a suitable place to build a building.
            Note: Air units in the desired location will return
                :param obs: The observer.
                :param screen_coordinates: The desired location to check for building placement in screen coordinates.
                :param building_radius: The radius (in screen coordinates) of the area to be checked.

                :return Boolean
        """
        x = screen_coordinates[1]
        y = screen_coordinates[0]
        if x-building_radius < 0 or x+building_radius > 84 or y-building_radius < 0 or y+building_radius > 84:
            return False
        height = obs.observation.feature_screen[0][x][y]
        for i in range(2*building_radius):
            for j in range(2*building_radius):
                if (height <= 10 or    # Godtyckligt vald (botten av kartan är unpathable)
                        obs.observation.feature_screen[5][x-building_radius+i][y-building_radius+j] != 0 or
                        obs.observation.feature_screen[0][x-building_radius+i][y-building_radius+j] != height):
                    return False
        return True

    def find_placement(self, obs, building_radius, maximum_searches=None, sampling_size=None):
        """Finds a suitable location to place a building on a grid on the current screen.
            Note: It will be computationally expensive if maximum_searches is high and/or
                    if sampling_size is close to 1.

                :param obs: The observer.
                :param building_radius: The radius (in screen coordinates) of the building (e.g. Barracks' is 6 or 7).
                :param maximum_searches: The maximum amount of searches before giving up. If None, it equals the number
                                            of grid points. It won't be higher than the number of grid points.
                :param sampling_size: How many screen points to skip before evaluating the next location. Essentially
                                        the density of the grid (lower => more dense). If None, it defaults to 7.

                :return coordinates (x, y) or None
        """
        coordinates = []
        size = len(obs.observation.feature_screen[5][0])
        if sampling_size is None:
            sampling_size = 7
        elif sampling_size < 1:
            sampling_size = 1
        if size > 0:
            for x in range(int(size/sampling_size)):
                for y in range(int(size/sampling_size)):
                    if obs.observation.feature_screen[5][sampling_size*y][sampling_size*x] == 0:
                        coordinates.append((sampling_size*x, sampling_size*y))
        else:
            return None

        random.shuffle(coordinates)
        if maximum_searches is None or maximum_searches > len(coordinates):
            maximum_searches = len(coordinates)
        for location_tuple in range(maximum_searches):
            if BuildOrders.check_placement(self, obs, coordinates[location_tuple], building_radius):
                return coordinates[location_tuple]
        return None

        if (len(obs.observation.multi_select) > 0 and
                obs.observation.multi_select[0].unit_type == unit_type):
            return True

        return False