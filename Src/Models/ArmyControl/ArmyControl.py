from pysc2.agents import base_agent
from pysc2.lib import actions, units, features
import numpy as np
from Models.BuildOrders.ActionSingleton import ActionSingelton
from Models.Predefines.Coordinates import Coordinates
import random

"""
This class manages the army and scouting.
"""

class ArmyControl(base_agent.BaseAgent):
    def __init__(self):
        super(Attack, self).__init__()
        self.reqSteps = 0

    def attack(self, obs, location=None):
        """Selects all army units and issues an attack order on the closest enemy.
                It checks for enemies using the minimap. It also counts the army.

                :param obs: The observer.
                :param location: The desired location to attack [y, x] in minimap coordinates.
                                   If None, it attacks the closest enemy
                """
        new_action = [actions.FUNCTIONS.no_op()]
        screen_location = [0, 0]

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
            if location is None:
                distance = []

                enemy_y, enemy_x = (obs.observation.feature_minimap.player_relative
                                    == features.PlayerRelative.ENEMY).nonzero()
                if len(enemy_y) > 0:
                    for i in range(len(enemy_y)):
                        distance.append(
                            np.power(enemy_x[i] - self.base_location[1], 2) +
                            np.power(enemy_y[i] - self.base_location[0], 2)
                        )

                    index_min = min(range(len(distance)), key=distance.__getitem__)
                    location = [enemy_x[index_min], enemy_y[index_min]]

                else:
                    location = self.attack_coordinates

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
                self.action_finished = True
                new_action = [actions.FUNCTIONS.Attack_screen("now", screen_location)]

        ActionSingelton().set_action(new_action)

    def retreat(self, obs, location=None):
        """Selects all army units and issues a move order.

                :param obs: The observer.
                :param location: The desired location to move to [y, x] in minimap coordinates.
                                   If None, it defaults to base_location.
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
                self.action_finished = True
                new_action = [actions.FUNCTIONS.Move_minimap("now", [location[0], location[1]])]

        ActionSingelton().set_action(new_action)

    def scout(self, obs):
        """Selects a random SCV and issues a move order to an enemy base.
                :param obs: The observer.
        """
        new_action = [actions.FUNCTIONS.no_op()]
        if self.reqSteps == 0:
            self.reqSteps = 3

        if self.reqSteps == 3:
            self.reqSteps = 2
            if actions.FUNCTIONS.move_camera.id in obs.observation.available_actions:
                new_action = [actions.FUNCTIONS.move_camera(self.base_location)]
            else:
                self.reqSteps = 0

        elif self.reqSteps == 2:
            self.reqSteps = 1
            new_action = ArmyControl.select_scv(self, obs)

        elif self.reqSteps == 1:
            self.reqSteps = 0
            if ArmyControl.select_unit(self, obs, units.Terran.SCV):
                if actions.FUNCTIONS.Move_minimap.id in obs.observation.available_actions:
                    if self.start_top:
                        self.scout_location = random.choice(Coordinates.EXPO_LOCATIONS2+[Coordinates.START_LOCATIONS[1]])
                    else:
                        self.scout_location = random.choice(Coordinates.EXPO_LOCATIONS2+[Coordinates.START_LOCATIONS[0]])

                    self.last_scout = self.steps
                    self.action_finished = True
                    new_action = [actions.FUNCTIONS.Move_minimap("now", self.scout_location)]

        ActionSingelton().set_action(new_action)

    def count_army(self, obs):
        """Selects all army units and counts them. Currently only counts marines.
                :param obs: The observer.
        """
        new_action = [actions.FUNCTIONS.no_op()]

        if self.reqSteps == 0:
            self.reqSteps = 2

        if self.reqSteps == 2:
            self.reqSteps = 1
            if actions.FUNCTIONS.select_army.id in obs.observation.available_actions:
                new_action = [actions.FUNCTIONS.select_army("select")]
            else:
                self.reqSteps = -1    # Fulhack, men detta gör så att attack selector alltid kan göra detta först.

        if self.reqSteps == 1:
            if ArmyControl.select_unit(self, obs, units.Terran.Marine):
                self.marine_count = 0
                for i in range(len(obs.observation.multi_select)):
                    if obs.observation.multi_select[i].unit_type == units.Terran.Marine:
                        self.marine_count += 1

            self.reqSteps = -1    # Fulhack, men detta gör så att attack selector alltid kan göra detta först.

        ActionSingelton().set_action(new_action)

    def temp_no_op(self, obs):
        """Temporary no_op until a help class with no_op gets added. Doesn't do anything.
                :param obs: The observer.
        """
        new_action = [actions.FUNCTIONS.no_op()]

        if self.reqSteps == 0:
            self.reqSteps = 2

        if self.reqSteps == 2:
            self.reqSteps = 1
        elif self.reqSteps == 1:
            self.reqSteps = 0

        ActionSingelton().set_action(new_action)



    # The following lines of code should be in a help class.

    def sigma(self, num):
        if num <= 0:
            return 0
        elif num >= 83:
            return 83
        else:
            return num

    def get_units(self, obs, unit_type):
        return [unit for unit in obs.observation.feature_units
                if unit.unit_type == unit_type]

    def select_scv(self, obs):
        new_action = [actions.FUNCTIONS.no_op()]
        command_scv = ArmyControl.get_units(self, obs, units.Terran.SCV)
        if len(command_scv) > 0 and not ArmyControl.select_unit(self, obs, units.Terran.SCV):
            if obs.observation.player.idle_worker_count > 0:
                new_action = [actions.FUNCTIONS.select_idle_worker(
                    "select", obs, units.Terran.SCV)]
            else:
                command = random.choice(command_scv)
                new_action = [actions.FUNCTIONS.select_point(
                    "select", (ArmyControl.sigma(self, command.x),
                               ArmyControl.sigma(self, command.y)))]
        return new_action

    def select_unit(self, obs, unit_type):
        if (len(obs.observation.single_select) > 0 and
                obs.observation.single_select[0].unit_type == unit_type):
            return True

        if (len(obs.observation.multi_select) > 0 and
                obs.observation.multi_select[0].unit_type == unit_type):
            return True

        return False
