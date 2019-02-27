from pysc2.agents import base_agent
from pysc2.lib import actions, units, features
import numpy as np
from Models.BuildOrders.ActionSingelton import ActionSingelton
import random

class ArmyControl(base_agent.BaseAgent):
    def __init__(self):
        super(Attack, self).__init__()
        self.reqSteps = 0

    def attack(self, obs, location=None):
        """Selects all army units and issues an attack order on the closest enemy.
                It checks for enemies using the minimap.

                :param obs: The observer.
                :param location: The desired location to attack [y, x] in minimap coordinates.
                                   If None, it attacks the closest enemy
                :return: Returns an action (either select_army or Attack_minimap).
                """
        new_action = [actions.FUNCTIONS.no_op()]
        screen_location = [0, 0]
        if location is None:
            enemy_x = []
            enemy_y = []
            distance = []

            for x in range(64):    # minimap_size = 64
                for y in range(64): # minimap_size = 64
                    if obs.observation.feature_minimap[5][y][x] == 4:  # Finds enemy units on minimap
                        enemy_x.append(x)
                        enemy_y.append(y)
                        distance.append(np.power(x - self.base_location[1], 2) + np.power(y - self.base_location[0], 2))

            if len(distance) > 0:
                index_min = min(range(len(distance)), key=distance.__getitem__)
                location = [enemy_x[index_min], enemy_y[index_min]]

            else:
                location = self.base_location

        if self.reqSteps == 0:
            self.reqSteps = 3

        elif self.reqSteps == 3:
            self.reqSteps = 2
            if actions.FUNCTIONS.select_army.id in obs.observation.available_actions:
                new_action = [actions.FUNCTIONS.select_army("select")]
            else:
                self.reqSteps = 0

        elif self.reqSteps == 2:
            self.reqSteps = 1
            if actions.FUNCTIONS.move_camera.id in obs.observation.available_actions:
                new_action = [actions.FUNCTIONS.move_camera(location)]
            else:
                self.reqSteps = 0

        elif self.reqSteps == 1:
            self.reqSteps = 0
            has_attack_point = False

            while not has_attack_point:
                x = random.randint(2, 81)
                y = random.randint(2, 81)
                if obs.observation.feature_screen[5][y][x] == 0:  # Finds a point without any units
                    screen_location = [y, x]
                    has_attack_point = True

            if actions.FUNCTIONS.Attack_screen.id in obs.observation.available_actions:
                new_action = [actions.FUNCTIONS.Attack_screen("now", screen_location)]

        ActionSingelton().set_action(new_action)

    def retreat(self, obs, location=None):
        """Selects all army units and issues a move order.

                :param obs: The observer.
                :param location: The desired location to move to [y, x] in minimap coordinates.
                                   If None, it defaults to base_location.
                :return: Returns an action (either select_army or Move_minimap).
                """
        new_action = [actions.FUNCTIONS.no_op()]

        if location is None:
            location = self.base_location

        if self.reqSteps == 0:
            self.reqSteps = 2

        elif self.reqSteps == 2:
            self.reqSteps = 1
            if actions.FUNCTIONS.select_army.id in obs.observation.available_actions:
                new_action = [actions.FUNCTIONS.select_army("select")]

        elif self.reqSteps == 1:
            self.reqSteps = 0
            if actions.FUNCTIONS.Move_minimap.id in obs.observation.available_actions:
                new_action = [actions.FUNCTIONS.Move_minimap("now", [location[0], location[1]])]

        ActionSingelton().set_action(new_action)
