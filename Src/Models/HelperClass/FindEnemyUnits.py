from pysc2.agents import base_agent
from pysc2.lib import actions, units, features
import numpy as np
from Models.BuildOrders.ActionSingleton import ActionSingleton
from Models.Predefines.Coordinates import Coordinates
import random

_PLAYER_ENEMY = features.PlayerRelative.ENEMY
_MARINE = [48]
_MARAUDER = [51]

class FindEnemyUnits:

    def count_enemy_army(self, obs):

        new_action = [actions.FUNCTIONS.no_op()]

        if self.reqSteps > 0:
            FindEnemyUnits.add_units_on_screen(self, obs)
            FindEnemyUnits.remove_screen_enemies(self, obs)
            FindEnemyUnits.find_next_screen(self, obs)

        if self.reqSteps == 0:
            self.enemy_units = 0
            FindEnemyUnits.find_minimap_locations(self, obs)
            sorted(self.minimap_locations, key=lambda k: [k[1], k[0]])
            self.top_enemy_screen_location = self.minimap_locations[0]
            self.left_jumps = 1
            self.reqSteps = 2

        if len(self.minimap_locations) is 0:
            self.reqSteps = 0
            if self.enemy_units is not 0:
                print(self.enemy_units)

        elif self.reqSteps > 0:
            new_action = FindEnemyUnits.move_efficient_camera(self, obs)

        ActionSingleton().set_action(new_action)


    def find_minimap_locations(self, obs):

        _ENEMY_INDEX = 4
        _PLAYER_RELATIVE = features.MINIMAP_FEATURES.player_relative.index
        player_relative = obs.observation['feature_minimap'][_PLAYER_RELATIVE]
        cc_y, cc_x = (player_relative == _ENEMY_INDEX).nonzero()

        self.minimap_locations = list(zip(cc_x, cc_y))


    def move_efficient_camera(self, obs):
        new_center = FindEnemyUnits.find_bottom_right_corner(self, self.top_enemy_screen_location)

        new_action = [actions.FUNCTIONS.move_camera(new_center)]

        return new_action

    def remove_screen_enemies(self, obs):
        temp_minimap_locations = []

        for (x, y) in self.minimap_locations:
            if FindEnemyUnits.coordinate_outside_of_screen(self, x, y):
                temp_minimap_locations.append((x, y))

        self.minimap_locations = temp_minimap_locations

    def find_bottom_right_corner(self, point):
        new_x = point[0] + 3
        new_y = point[1] + 3

        return (new_x, new_y)

    def add_units_on_screen(self, obs):

        units = [[unit.unit_type] for unit in obs.observation.feature_units
                    if unit.alliance == _PLAYER_ENEMY]

        for unit in units:
            if unit == _MARINE or unit == _MARAUDER:
                self.enemy_units += 1


    def find_next_screen(self, obs):
        if self.minimap_locations:
            if self.minimap_locations[0][1] > self.top_enemy_screen_location[1] + self.camera_height:
                self.top_enemy_screen_location = self.minimap_locations[0]
                self.left_jumps = 1

            else:
                if FindEnemyUnits.unit_left_of_screen(self, obs):
                    tmplst = list(self.top_enemy_screen_location)
                    tmplst[0] = self.top_enemy_screen_location[0] - self.camera_width
                    self.top_enemy_screen_location = tuple(tmplst)
                    self.left_jumps += 1

                else:
                    tmplst = list(self.top_enemy_screen_location)
                    tmplst[0] = self.top_enemy_screen_location[0] + self.camera_width*self.left_jumps
                    self.top_enemy_screen_location = tuple(tmplst)
                    self.left_jumps = 1

    def unit_left_of_screen(self, obs):
        temp_minimap_locations = []

        for (x, y) in self.minimap_locations:
            if y < self.top_enemy_screen_location[1] + self.camera_height:
                if x < self.top_enemy_screen_location[0]:
                    temp_minimap_locations.append((x, y))

        return temp_minimap_locations

    def coordinate_outside_of_screen(self, x, y):
        below_screen = y > self.top_enemy_screen_location[1] + self.camera_height
        right_of_screen = x < self.top_enemy_screen_location[0]
        left_of_screen = x > self.top_enemy_screen_location[0] + self.camera_width

        return below_screen or right_of_screen or left_of_screen
