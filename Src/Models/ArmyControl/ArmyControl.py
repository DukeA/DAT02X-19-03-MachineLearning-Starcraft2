from pysc2.agents import base_agent
from pysc2.lib import actions, units, features
import numpy as np
from Models.BuildOrders.ActionSingleton import ActionSingleton
from Models.Predefines.Coordinates import Coordinates
from Models.HelperClass.HelperClass import HelperClass
import random


"""
This class manages the army and scouting.
"""


class ArmyControl(base_agent.BaseAgent):
    def __init__(self):
        super(ArmyControl, self).__init__()
        self.reqSteps = 0

    def attack(self, obs, location=None):
        """Selects all army units and issues an attack order on the closest enemy.
                It checks for enemies using the minimap. It also counts the army.

                :param obs: The observer.
                :param location: The desired location to attack [x, y] in minimap coordinates.
                                   If None, it attacks the closest enemy
                """
        new_action = [actions.FUNCTIONS.no_op()]

        if self.reqSteps == 0:
            self.reqSteps = 4

        if self.reqSteps == 4:
            if actions.FUNCTIONS.select_army.id in obs.observation.available_actions:
                new_action = [actions.FUNCTIONS.select_army("select")]

        if self.reqSteps == 3:
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

        if self.reqSteps == 2:
            has_attack_point = False
            screen_location = [0, 0]

            while not has_attack_point:
                x = random.randint(20, 60)
                y = random.randint(20, 60)
                if obs.observation.feature_screen[5][y][x] == 0:  # Finds a point without any units
                    screen_location = [x, y]
                    has_attack_point = True

            if actions.FUNCTIONS.Attack_screen.id in obs.observation.available_actions:
                self.action_finished = True
                new_action = [actions.FUNCTIONS.Attack_screen("now", screen_location)]

        # One step is being intentionally left blank.
        self.reqSteps -= 1
        ActionSingleton().set_action(new_action)

    def retreat(self, obs, location=None):
        """Selects all army units and issues a move order.

                :param obs: The observer.
                :param location: The desired location to move to [y, x] in minimap coordinates.
                                   If None, it defaults to base_location.
                """
        new_action = [actions.FUNCTIONS.no_op()]

        if location is None:
            location = [32, 32]

        if self.reqSteps == 0:
            self.reqSteps = 4

        if self.reqSteps == 3:
            if actions.FUNCTIONS.select_army.id in obs.observation.available_actions:
                new_action = [actions.FUNCTIONS.select_army("select")]

        if self.reqSteps == 2:
            if actions.FUNCTIONS.Move_minimap.id in obs.observation.available_actions:
                self.action_finished = True
                new_action = [actions.FUNCTIONS.Move_minimap("now", [location[0], location[1]])]

        # One step is being intentionally left blank.
        self.reqSteps -= 1
        ActionSingleton().set_action(new_action)

    def scout(self, obs):
        """Selects a random SCV and issues a move order to an enemy base.
                :param obs: The observer.
        """
        new_action = [actions.FUNCTIONS.no_op()]
        if self.reqSteps == 0:
            self.reqSteps = 4

        if self.reqSteps == 4:
            if obs.observation.player.idle_worker_count > 0:
                new_action = [actions.FUNCTIONS.select_idle_worker(
                    "select", obs, units.Terran.SCV)]
            elif actions.FUNCTIONS.move_camera.id in obs.observation.available_actions:
                new_action = [HelperClass.move_camera_to_base_location(self, obs)]

        if self.reqSteps == 3:
            if not HelperClass.is_unit_selected(self, obs, units.Terran.SCV):
                new_action = HelperClass.select_scv(self, obs)

        if self.reqSteps == 2:
            if HelperClass.is_unit_selected(self, obs, units.Terran.SCV):
                if actions.FUNCTIONS.Move_minimap.id in obs.observation.available_actions:
                    if self.start_top:
                        self.scout_loc = random.choice(
                            Coordinates.EXPO_LOCATIONS2+[Coordinates.START_LOCATIONS[1]])
                    else:
                        self.scout_loc = random.choice(
                            Coordinates.EXPO_LOCATIONS2+[Coordinates.START_LOCATIONS[0]])

                    self.last_scout = self.steps
                    self.action_finished = True
                    new_action = [actions.FUNCTIONS.Move_minimap("now", self.scout_loc)]

        # One step is being intentionally left blank.
        self.reqSteps -= 1
        ActionSingleton().set_action(new_action)

    def transform_vikings_to_ground(self, obs):
        """ Transforms all available Vikings to their ground mode (Assault mode)
                :param obs: The observer.
        """
        new_action = [actions.FUNCTIONS.no_op()]
        if self.reqSteps == 0:
            self.reqSteps = 4

        if self.reqSteps == 4:
            if actions.FUNCTIONS.select_army.id in obs.observation.available_actions:
                new_action = [actions.FUNCTIONS.select_army("select")]

        if self.reqSteps == 3:
            vikings_air = [vikings for vikings in obs.observation.multi_select
                           if vikings.unit_type == units.Terran.VikingFighter]
            if len(vikings_air) > 0:
                if HelperClass.do_action(self, obs, actions.FUNCTIONS.select_unit.id):
                    for i in range(len(obs.observation.multi_select)):
                        if obs.observation.multi_select[i].unit_type == units.Terran.VikingFighter:
                            new_action = [actions.FUNCTIONS.select_unit("select_all_type", i)]
                            break

        if self.reqSteps == 2:
            if HelperClass.do_action(self, obs, actions.FUNCTIONS.Morph_VikingAssaultMode_quick.id):
                new_action = [actions.FUNCTIONS.Morph_VikingAssaultMode_quick("now")]
                self.action_finished = True

        # One step is being intentionally left blank.
        self.reqSteps -= 1
        ActionSingleton().set_action(new_action)

    def transform_vikings_to_air(self, obs):
        """ Transforms all available Vikings to their air mode (Fighter mode)
                :param obs: The observer.
        """
        new_action = [actions.FUNCTIONS.no_op()]
        if self.reqSteps == 0:
            self.reqSteps = 4

        if self.reqSteps == 4:
            if actions.FUNCTIONS.select_army.id in obs.observation.available_actions:
                new_action = [actions.FUNCTIONS.select_army("select")]

        if self.reqSteps == 3:
            vikings_ground = [vikings for vikings in obs.observation.multi_select
                              if vikings.unit_type == units.Terran.VikingAssault]
            if len(vikings_ground) > 0:
                if HelperClass.do_action(self, obs, actions.FUNCTIONS.select_unit.id):
                    for i in range(len(obs.observation.multi_select)):
                        if obs.observation.multi_select[i].unit_type == units.Terran.VikingAssault:
                            new_action = [actions.FUNCTIONS.select_unit("select_all_type", i)]
                            break

        if self.reqSteps == 2:
            if HelperClass.do_action(self, obs, actions.FUNCTIONS.Morph_VikingFighterMode_quick.id):
                new_action = [actions.FUNCTIONS.Morph_VikingFighterMode_quick("now")]
                self.action_finished = True

        # One step is being intentionally left blank.
        self.reqSteps -= 1
        ActionSingleton().set_action(new_action)

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
                # Fulhack, men detta gör så att attack selector alltid kan göra detta först.
                self.reqSteps = -1

        elif self.reqSteps == 1:
            if HelperClass.is_unit_selected(self, obs, units.Terran.Marine):
                self.marine_count = 0
                for i in range(len(obs.observation.multi_select)):
                    if obs.observation.multi_select[i].unit_type == units.Terran.Marine:
                        self.marine_count += 1

            # Fulhack, men detta gör så att attack selector alltid kan göra detta först.
            self.reqSteps = -1

        ActionSingleton().set_action(new_action)
