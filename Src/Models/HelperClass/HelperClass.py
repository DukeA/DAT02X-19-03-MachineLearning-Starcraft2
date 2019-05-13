from pysc2.agents import base_agent
from pysc2.lib import actions, units,features
import numpy as np
from Models.BuildOrders.ActionSingleton import ActionSingleton
import random


class HelperClass(base_agent.BaseAgent):
    All_Buildings = []
    Camera_Position =[]

    # Moves to camera to a self.base_location
    def move_camera_to_base_location(self, obs):
        return actions.FUNCTIONS.move_camera(self.base_location)

    @staticmethod
    def select_all_buildings(obs):
        if obs.observation.control_groups[9][1] > 0:
            return [actions.FUNCTIONS.select_control_group("recall", 9)]
        else:
            return [actions.FUNCTIONS.no_op()]

    @staticmethod
    def sigma(num):
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
                    "select", (HelperClass.sigma(command.x),
                               HelperClass.sigma(command.y)))]
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

    def check_building_at_position(self, obs, build_location):
        if build_location[0] == -1:
            return True
        unit_type = [units.Terran.Barracks, units.Terran.SupplyDepot]
        x = build_location[0]
        y = build_location[1]
        buildings = [unit for unit in obs.observation.feature_units
                     if unit.unit_type == unit_type[0] or unit.unit_type == unit_type[1]]
        if len(buildings) <= 0:
            return False
        Camera = obs.observation.camera_position
        new_building_found = False
        for building in buildings:
            value = building.owner
            if value != 1 :
                return False
            if building.build_progress != 100:
                return False
            exist = False
            for existing_building in HelperClass.All_Buildings:
                if existing_building[0] == building.x+ Camera[0] and existing_building[1] == building.y+Camera[1]:
                    exist = True
            if exist == False:
                new_building_found = True
                break
        if new_building_found == False:
            return False
        HelperClass.All_Buildings = []
        for building in buildings:
            value_x = building.x+Camera[0]
            value_y = building.y+Camera[1]
            HelperClass.All_Buildings.append([value_x,value_y])
        return True


    @staticmethod
    def get_current_minimap_location(obs):
        """
        Gets the current minimap location (which corresponds to the move_camera coordinate)
        """
        x = []
        y = []
        for i in range(64):
            for j in range(64):
                if obs.observation.feature_minimap.camera[j][i] == 1:
                    x.append(i)
                    y.append(j)

        # Why +4? Because move_camera(x, y) moves the camera so that it covers the minimap coordinates from
        # x-4 to x+2 and y-4 to y+2. Why? No idea.
        return min(x) + 4, min(y) + 4

    @staticmethod
    def move_screen(obs, relative_coordinates):
        """
        Moves the screen relative to the input coordinates
        :param obs:
        :param relative_coordinates: The relative screen coordinates
        """
        current_minimap_coordinates = HelperClass.get_current_minimap_location(obs)
        x, y = relative_coordinates
        # The map is 200x176 units, but the camera movement works better if it's treated as 200x200 for some reason.
        # The camera takes up 24 units.
        delta_x = round((x - 42) / (200 * 84 / (24 * 64)))
        delta_y = round((y - 42) / (200 * 84 / (24 * 64)))
        new_action = [actions.FUNCTIONS.move_camera((delta_x + current_minimap_coordinates[0],
                                                     delta_y + current_minimap_coordinates[1]))]

        return new_action

    def find_the_camera_postion(self, obs):
      Camera = obs.observation.camera_position
      HelperClass.Camera_Position = []
      value_x = Camera[0]
      value_y = Camera[1]
      HelperClass.Camera_Position.append([value_x,value_y])
      print (value_x, value_y)


    def no_op(self, obs):

        new_action = [actions.FUNCTIONS.no_op()]

        if self.reqSteps == 0:
            self.reqSteps = 4

        self.reqSteps -= 1
        ActionSingleton().set_action(new_action)

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

        build_screen_action = action_types.get(
            building_type, actions.FUNCTIONS.Build_SupplyDepot_screen)

        if HelperClass.is_unit_selected(self, obs, units.Terran.SCV):
            if HelperClass.do_action(self, obs, build_screen_action.id):
                coordinates = (HelperClass.sigma(coordinates[0]), HelperClass.sigma(coordinates[1]))
                new_action = [build_screen_action("now", coordinates)]

        return new_action

    def check_minimap_for_units(self, obs, camera_coordinate):
        camera_coordinate = [int(coord) for coord in camera_coordinate]
        minimap_player_relative = obs.observation.feature_minimap[5]
        minimap_screen_area_rows = minimap_player_relative[(
                                                                   camera_coordinate[1] - 4):(camera_coordinate[1] + 2)]
        minimap_screen_area = np.array(
            [row[(camera_coordinate[0] - 4):(camera_coordinate[0] + 2)] for row in minimap_screen_area_rows])
        friendly_unit_indexes = np.where(minimap_screen_area == 1)

        if len(friendly_unit_indexes[0]) > 0:
            return True
        else:
            return False
