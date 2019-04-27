import random
from pysc2.agents import base_agent
from pysc2.lib import actions, units
from Models.Predefines.Coordinates import Coordinates
from Models.BuildOrders.ActionSingleton import ActionSingleton
from Models.HelperClass.HelperClass import HelperClass

"""
The Class belongs to the Build Order request
to build certain elements such as supply depots and
refineries.
"""


class BuildOrders(base_agent.BaseAgent):
    def __init__(self):
        super(BuildOrders, self).__init__()
        self.base_location = None
        self.expo_loc = None
        self.new_action = None

        """
            @Author:Arvid , revised :Adam Grandén
            @:param The parameter would be  self which is a aibot
            @:param The other would be the observable universe
            This method would be the barracks which builds the barrack from the start of the base_location
            and gets an instance where to build that barrack on that location.

        """

    def build_barracks(self, obs, build_location):
        """
            Builds a barracks.
        """
        new_action = [actions.FUNCTIONS.no_op()]

        if self.reqSteps == 0:
            self.reqSteps = 4

        if self.reqSteps == 4:
            new_action = [actions.FUNCTIONS.move_camera(self.base_location)]

        elif self.reqSteps == 3:
            new_action = HelperClass.select_scv(self, obs)

        elif self.reqSteps == 2:  # Moves camera twice because select_scv can also move camera
            new_action = [actions.FUNCTIONS.move_camera(self.base_location)]

        elif self.reqSteps == 1:
            coordinates = BuildOrders.find_placement(
                self, obs, building_radius=6, maximum_searches=1000, sampling_size=1)

            if coordinates is not None:
                new_action = HelperClass.place_building(self, obs, units.Terran.Barracks, build_location[0],
                                                        build_location[1])

        self.reqSteps -= 1
        ActionSingleton().set_action(new_action)

    def build_supply_depot(self, obs, build_location):
        """
            Builds a supply depot.
        """
        new_action = [actions.FUNCTIONS.no_op()]

        if self.reqSteps == 0:
            self.reqSteps = 4

        if self.reqSteps == 4:
            new_action = [actions.FUNCTIONS.move_camera(self.base_location)]

        if self.reqSteps == 3:
            HelperClass.get_current_minimap_location(obs)
            new_action = HelperClass.select_scv(self, obs)

        if self.reqSteps == 2:
            new_action = [actions.FUNCTIONS.move_camera(self.base_location)]

        if self.reqSteps == 1:
            for loop in range(20):
                x = build_location[0]
                y = build_location[1]
                if BuildOrders.is_valid_placement(self, obs, (x, y), building_radius=2):
                    new_action = HelperClass.place_building(
                        self, obs, units.Terran.SupplyDepot, x, y)
                    break

        self.reqSteps -= 1
        ActionSingleton().set_action(new_action)

    def build_refinery(self, obs):
        """
            Builds a refinery in any base with a command center.
        """
        # TODO: Maybe should check for depleted geysers
        # TODO: Once stumbled upon a bug where it started to build refineries in the middle of the map. Haven't tried
        # to fix it.
        new_action = [actions.FUNCTIONS.no_op()]

        if self.reqSteps == 0:
            self.reqSteps = 4

        if self.reqSteps == 4:
            new_action = [actions.FUNCTIONS.move_camera(self.base_location)]

        if self.reqSteps == 3:
            new_action = HelperClass.select_scv(self, obs)

        # This step finds a vacant vespene geyser near a command center and moves the camera there.
        # The center of a Command Center must be about 8 in-game units away from a geyser.
        # The feature screen is 24x24 in-game units or 84x84 screen units.
        # With a margin, a geyser will be less than 9.5 * 84/24 screen units from its Command Center (or half a screen)
        # That's how this code judges if a geyser belongs to a base.
        if self.reqSteps == 2:
            geyser_distance = (9.5 * 84 / 24) ** 2
            all_geysers = [u for u in obs.observation.raw_units
                           if u.unit_type == units.Neutral.VespeneGeyser]
            all_refineries = [u for u in obs.observation.raw_units
                              if u.unit_type == units.Terran.Refinery
                              and u.alliance == 1]
            all_command_centers = [u for u in obs.observation.raw_units
                                   if u.unit_type == units.Terran.CommandCenter
                                   and u.alliance == 1]
            selected_geyser = []

            if len(all_command_centers) > 0:
                cc_pos = [(cc.x, cc.y) for cc in all_command_centers]
                if len(all_refineries) > 0:
                    refinery_pos = [(ref.x, ref.y) for ref in all_refineries]
                    # Find CCs with at least one vacant geyser
                    for i in range(len(all_command_centers)):
                        cc = cc_pos[i]
                        base_refineries = 0
                        # Finds the number of refineries belonging to a CC
                        for j in range(len(all_refineries)):
                            if (cc[0] - refinery_pos[j][0]) ** 2 + (cc[1] - refinery_pos[j][1]) ** 2 < geyser_distance:
                                base_refineries += 1
                                if base_refineries == 2:
                                    break
                        # Equivalent to there being a vacant geyser near the CC
                        if base_refineries < 2:
                            geyser_pos = [(geyser.x, geyser.y) for geyser in all_geysers]
                            for j in range(len(all_geysers)):
                                if (cc[0] - geyser_pos[j][0]) ** 2 + (cc[1] - geyser_pos[j][1]) ** 2 < geyser_distance:
                                    selected_geyser = geyser_pos[j]
                                    break
                        if selected_geyser:
                            break

                # Trivial case: there are no refineries so just pick any suitable geyser
                else:
                    cc = random.choice(cc_pos)
                    if len(all_geysers) > 0:
                        geyser_pos = [(geyser.x, geyser.y) for geyser in all_geysers]
                        for i in range(len(all_geysers)):
                            if (cc[0] - geyser_pos[i][0]) ** 2 + (cc[1] - geyser_pos[i][1]) ** 2 < geyser_distance:
                                selected_geyser = geyser_pos[i]

            if selected_geyser:
                new_action = HelperClass.move_screen(obs, selected_geyser)

        # At this point there should be a vacant geyser on the screen (or none at all if last step failed).
        if self.reqSteps == 1:
            geysers = [u for u in obs.observation.feature_units
                       if u.unit_type == units.Neutral.VespeneGeyser]
            refineries = [u for u in obs.observation.feature_units
                          if u.unit_type == units.Terran.Refinery
                          and u.alliance == 1]
            if len(refineries) == 0 and len(geysers) > 0:
                new_action = HelperClass.place_building(
                    self, obs, units.Terran.Refinery, geysers[0].x, geysers[0].y)
            elif len(refineries) == 1 and len(geysers) == 2:
                geyser_loc_1 = (geysers[0].x, geysers[0].y)
                geyser_loc_2 = (geysers[1].x, geysers[1].y)
                if geyser_loc_1[0] == refineries[0].x and geyser_loc_1[1] == refineries[0].y:
                    new_action = HelperClass.place_building(
                        self, obs, units.Terran.Refinery, geyser_loc_2[0], geyser_loc_2[1])
                else:
                    new_action = HelperClass.place_building(
                        self, obs, units.Terran.Refinery, geyser_loc_1[0], geyser_loc_1[1])

        self.reqSteps -= 1
        ActionSingleton().set_action(new_action)

    def return_scv(self, obs):
        """
            Returns an idle SCV to mining. It tries to populate refineries first. Checks other bases if the main base
            has depleted its resources.
        """
        new_action = [actions.FUNCTIONS.no_op()]
        if self.reqSteps == 0:
            self.reqSteps = 4

        if self.reqSteps == 4:
            if obs.observation.player.idle_worker_count > 0:
                new_action = [actions.FUNCTIONS.select_idle_worker(
                    "select", obs, units.Terran.SCV)]

        # Finds a suitable base to send the SCV to.
        if self.reqSteps == 3:
            command_centers = [u for u in obs.observation.raw_units
                               if u.alliance == 1
                               and u.unit_type == units.Terran.CommandCenter
                               and u.build_progress == 100
                               and u.ideal_harvesters > 0]
            undermanned_command_centers = [u for u in command_centers
                                           if u.assigned_harvesters / u.ideal_harvesters < 0]
            undermanned_refineries = [u for u in obs.observation.raw_units
                                      if u.alliance == 1
                                      and u.unit_type == units.Terran.Refinery
                                      and u.build_progress == 100
                                      and u.assigned_harvesters < 3]
            if len(undermanned_refineries) > 0:
                refinery = random.choice(undermanned_refineries)
                new_action = HelperClass.move_screen(obs, (refinery.x, refinery.y))
            elif len(undermanned_command_centers) > 0:
                command_center = random.choice(undermanned_command_centers)
                new_action = HelperClass.move_screen(obs, (command_center.x, command_center.y))
            elif len(command_centers) > 0:
                command_center = random.choice(command_centers)
                new_action = HelperClass.move_screen(obs, (command_center.x, command_center.y))

        # Should be at a base now.
        if self.reqSteps == 2:
            undermanned_refineries = [u for u in obs.observation.feature_units
                                      if u.alliance == 1
                                      and u.unit_type == units.Terran.Refinery
                                      and u.build_progress == 100
                                      and u.assigned_harvesters < 3]
            minerals = [u for u in obs.observation.feature_units if
                        (u.unit_type == units.Neutral.MineralField
                         or u.unit_type == units.Neutral.MineralField750
                         or u.unit_type == units.Neutral.RichMineralField
                         or u.unit_type == units.Neutral.RichMineralField750)]
            if len(undermanned_refineries) > 0:
                refinery = undermanned_refineries[0]
                if HelperClass.do_action(self, obs, actions.FUNCTIONS.Harvest_Gather_screen.id):
                    new_action = [actions.FUNCTIONS.Harvest_Gather_screen(
                        "now", (HelperClass.sigma(refinery.x),
                                HelperClass.sigma(refinery.y)))]
                    self.action_finished = True
            elif len(minerals) > 0:
                mineral = minerals[0]
                if HelperClass.do_action(self, obs, actions.FUNCTIONS.Harvest_Gather_screen.id):
                    new_action = [actions.FUNCTIONS.Harvest_Gather_screen(
                        "now", (HelperClass.sigma(mineral.x),
                                HelperClass.sigma(mineral.y)))]
                    self.action_finished = True

        # There's one step left (reqSteps == 1) that's intentionally being left blank.
        self.reqSteps -= 1

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
        """
            Builds a factory.
        """
        new_action = [actions.FUNCTIONS.no_op()]

        if self.reqSteps == 0:
            self.reqSteps = 4

        if self.reqSteps == 4:
            new_action = [actions.FUNCTIONS.move_camera(self.base_location)]

        elif self.reqSteps == 3:
            new_action = HelperClass.select_scv(self, obs)

        elif self.reqSteps == 2:  # Moves camera twice because select_scv can also move camera
            new_action = [actions.FUNCTIONS.move_camera(self.base_location)]

        elif self.reqSteps == 1:
            coordinates = BuildOrders.find_placement(
                self, obs, building_radius=6, maximum_searches=10, sampling_size=9)

            if coordinates is not None:
                new_action = HelperClass.place_building(
                    self, obs, units.Terran.Factory, coordinates[0], coordinates[1])

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
        """
            Builds a starport.
        """
        new_action = [actions.FUNCTIONS.no_op()]

        if self.reqSteps == 0:
            self.reqSteps = 4

        if self.reqSteps == 4:
            new_action = [actions.FUNCTIONS.move_camera(self.base_location)]

        elif self.reqSteps == 3:
            new_action = HelperClass.select_scv(self, obs)

        elif self.reqSteps == 2:  # Moves camera twice because select_scv can also move camera
            new_action = [actions.FUNCTIONS.move_camera(self.base_location)]

        elif self.reqSteps == 1:
            coordinates = BuildOrders.find_placement(
                self, obs, building_radius=6, maximum_searches=10, sampling_size=9)

            if coordinates is not None:
                new_action = HelperClass.place_building(
                    self, obs, units.Terran.Starport, coordinates[0], coordinates[1])

        self.reqSteps -= 1
        ActionSingleton().set_action(new_action)
        """
            @Author Adam Grandén
            @:param self- Object aibot
            @:param obs - the observable universe
            This code takes the  barracks which are located and then adds
            an  techlab when the building is built.
        """

    def build_tech_lab_barracks(self, obs):
        """
            Builds a tech lab addon at a barracks.
        """
        new_action = [actions.FUNCTIONS.no_op()]
        barracks = HelperClass.get_units(self, obs, units.Terran.Barracks)

        if self.reqSteps == 0:
            self.reqSteps = 4

        elif self.reqSteps == 4:
            new_action = [
                actions.FUNCTIONS.move_camera(self.base_location)]

        elif self.reqSteps == 3:
            if len(barracks) > 0 and HelperClass.not_in_progress(self, obs, units.Terran.Barracks):
                new_action = [actions.FUNCTIONS.select_point("select",
                                                             (HelperClass.sigma(barracks[0].x),
                                                              HelperClass.sigma(barracks[0].y)))]
        elif self.reqSteps == 2:
            if len(barracks) > 0:
                if HelperClass.is_unit_selected(self, obs, units.Terran.Barracks):
                    if HelperClass.do_action(self, obs, actions.FUNCTIONS.Build_TechLab_Barracks_quick.id):
                        new_action = [actions.FUNCTIONS.Build_TechLab_Barracks_quick("now")]
        self.reqSteps -= 1
        ActionSingleton().set_action(new_action)

    def expand(self, obs):
        """
            Builds a command center at a suitable, empty base. Doesn't build in the main bases.
        """
        new_action = [actions.FUNCTIONS.no_op()]
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
                        "select", (HelperClass.sigma(command.x),
                                   HelperClass.sigma(command.y)))]

        # This part finds a vacant expansion location
        if self.reqSteps == 2:
            camera_pos = HelperClass.get_current_minimap_location(obs)
            if self.start_top is not None and not self.start_top:
                expansions_minimap = Coordinates.EXPO_LOCATIONS2
                expansions_screen = Coordinates.CC_LOCATIONS2
            else:
                expansions_minimap = Coordinates.EXPO_LOCATIONS
                expansions_screen = Coordinates.CC_LOCATIONS
            # This should be compatible with the coordinates gotten from raw_units
            expansions_relative_screen = [((a[0][0] - camera_pos[0]) * (200 * 84 / (24 * 64)) + a[1][0],
                                           (a[0][1] - camera_pos[1]) * (200 * 84 / (24 * 64)) + a[1][1])
                                          for a in list(zip(expansions_minimap, expansions_screen))]

            cc = [u for u in obs.observation.raw_units
                  if (u.unit_type == units.Terran.CommandCenter or
                      u.unit_type == units.Terran.OrbitalCommand or
                      u.unit_type == units.Terran.PlanetaryFortress)]

            for i in range(len(expansions_relative_screen)):
                if len(cc) > 0:
                    vacant = True
                    for j in range(len(cc)):
                        # 10 is an arbitrary screen length.
                        if (abs(cc[j].x - expansions_relative_screen[i][0]) < 10 and
                                abs(cc[j].y - expansions_relative_screen[i][1]) < 10):
                            vacant = False
                            break
                    if vacant:
                        new_action = [actions.FUNCTIONS.move_camera(expansions_minimap[i])]
                        self.expo_loc = i
                        break

        if self.reqSteps == 1:
            if self.expo_loc is not None:
                if self.start_top:
                    t = Coordinates.CC_LOCATIONS[self.expo_loc]
                else:
                    t = Coordinates.CC_LOCATIONS2[self.expo_loc]
                if HelperClass.do_action(self, obs, actions.FUNCTIONS.Build_CommandCenter_screen.id):
                    new_action = HelperClass.place_building(
                        self, obs, units.Terran.CommandCenter, t[0], t[1])

                self.expo_loc = None

        self.reqSteps -= 1
        ActionSingleton().set_action(new_action)

    def is_valid_placement(self, obs, screen_coordinates, building_radius):
        """Checks if a location and a radius around it is a suitable place to build a building.
            Note: Air units in the desired location will return
                :param obs: The observer.
                :param screen_coordinates: The desired location to check for building placement in screen coordinates.
                :param building_radius: The radius (in screen coordinates) of the area to be checked.

                :return Boolean
        """
        x = screen_coordinates[1]
        y = screen_coordinates[0]
        if x - building_radius < 0 or x + building_radius > 84 or y - building_radius < 0 or y + building_radius > 84:
            return False
        height = obs.observation.feature_screen[0][x][y]
        for i in range(2 * building_radius):
            for j in range(2 * building_radius):
                if (height <= 10 or  # Godtyckligt vald (botten av kartan är unpathable)
                        obs.observation.feature_screen[5][x - building_radius + i][y - building_radius + j] != 0 or
                        obs.observation.feature_screen[0][x - building_radius + i][y - building_radius + j] != height):
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
            for x in range(int(size / sampling_size)):
                for y in range(int(size / sampling_size)):
                    if obs.observation.feature_screen[5][sampling_size * y][sampling_size * x] == 0:
                        coordinates.append((sampling_size * x, sampling_size * y))
        else:
            return None

        random.shuffle(coordinates)
        if maximum_searches is None or maximum_searches > len(coordinates):
            maximum_searches = len(coordinates)
        for location_tuple in range(maximum_searches):
            if BuildOrders.is_valid_placement(self, obs, coordinates[location_tuple], building_radius):
                return coordinates[location_tuple]
        return None
