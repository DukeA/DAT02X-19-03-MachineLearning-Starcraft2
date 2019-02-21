from pysc2.agents import base_agent
from pysc2.lib import actions, units, features
import numpy as np


class Attack(base_agent.BaseAgent):
    def __init__(self):
        super(Attack, self).__init__()
        self.reqSteps = 0
        self.minimap_size = 64

    def attack(self, obs, location=None):
        """Selects all army units and issues an attack order on the closest enemy.
                It checks for enemies using the minimap.

                :param obs: The observer.
                :param location: The desired location to attack [x, y] in minimap coordinates.
                                   If None, it attacks the closest enemy
                :return: Returns an action (either select_army or Attack_minimap).
                """
        new_action = actions.FUNCTIONS.no_op()

        if location is None:
            enemy_x = []
            enemy_y = []
            distance = []

            for x in range(self.minimap_size):
                for y in range(self.minimap_size):
                    if obs.observation.feature_minimap[5][x][y] == 4:  # Finds enemy units on minimap
                        enemy_x.append(x)
                        enemy_y.append(y)
                        distance.append(np.power(x - self.base_location[0], 2) + np.power(y - self.base_location[1], 2))

            if len(distance) > 0:
                index_min = min(range(len(distance)), key=distance.__getitem__)
                location = [enemy_x[index_min], enemy_y[index_min]]

            else:
                location = self.base_location

        if self.reqSteps == 0:
            self.reqSteps = 2

        elif self.reqSteps == 2:
            self.reqSteps = 1
            if actions.FUNCTIONS.select_army.id in obs.observation.available_actions:
                new_action = actions.FUNCTIONS.select_army("select")

        elif self.reqSteps == 1:
            self.reqSteps = 0
            if actions.FUNCTIONS.Attack_minimap.id in obs.observation.available_actions:
                new_action = actions.FUNCTIONS.Attack_minimap("now", [location[1], location[0]])

        return new_action
