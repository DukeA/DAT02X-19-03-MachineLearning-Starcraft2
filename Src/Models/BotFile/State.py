import random
import numpy as np
import statistics

from pysc2.lib import actions, units, features
from collections import defaultdict

from Models.BuildOrders.ActionSingleton import ActionSingleton
from Models.HelperClass.HelperClass import HelperClass


class State:
    def __init__(self):

        # Game state

        self.units_amount = defaultdict(lambda: 0)  # Amount of each unit. Set to 0 by default
        self.units_amount[units.Terran.SCV] = 12
        self.units_amount[units.Terran.CommandCenter] = 1
        self.enemy_units_amount = defaultdict(lambda: 0)
        self.enemy_units_amount[units.Terran.SCV] = 12
        self.enemy_units_amount[units.Terran.CommandCenter] = 1
        self.minerals = 50
        self.vespene = 0
        self.food_used = 12
        self.food_cap = 15
        self.idle_workers = 0

        self.score = 0
        self.reward = 0
        self.action_issued = None
        self.state_tuple = []

        # Variables required for updating the game state

        # Information about buildings placed but not yet found is stored here on the form
        # [coordinate, unit_type, step it was created, if it has been found]
        self.units_in_progress = []
        self.update_steps_per_unit = 4  # Steps required to add each unit in units_in_progress to a control group
        self.update_building_step_threshold = 400  # Threshold steps for finding a building before it's removed from
        self.units_amounts_updated = False
        self.unit_weight = 50
        self.current_unit = None

        # Constants
        # Action space of actions whose success is easily evaluated with observation.last_actions[0].
        self.action_space = {
            42: "build_barracks",
            91: "build_supply_depot",
            79: "build_refinery",
            44: "expand",
            76: "build_factory",
            89: "build_starport",
            94: "build_tech_lab_barracks",
            477: "build_marine",
            476: "build_marauder",
            488: "build_reaper",
            470: "build_hellion",
            478: "build_medivac",
            498: "build_viking",
            490: "build_scv",
            0: "no_op"
        }
        # For reference, the rest of the action space is:
        # {attack, retreat, scout, distribute_scv, return_scv, transform_vikings_to_ground, transform_vikings_to_air}

    def get_state(self):
        """
        :return: A list containing all the tuples (minerals, vespene, unit_amount, action_issued, bot_obj.steps)
         since the start of the game
        """
        return self.state_tuple

    def update_state(self, bot_obj, obs):
        """
        Updates the state and adds up to 1 production facility to control group. Always takes 4 steps to execute.
        :param bot_obj: The agent
        :param obs: The observation
        :return: Actions
        """
        new_action = [actions.FUNCTIONS.no_op()]  # No action by default

        if bot_obj.reqSteps == 0:
            bot_obj.reqSteps = 3

            # Find latest issued action
            if bot_obj.action_finished:
                # This catches everything in ArmyControl, return_scv() and distribute_scv()
                bot_obj.action_finished = False
                self.action_issued = bot_obj.earlier_action
            else:
                # This catches the rest
                if len(obs.observation.last_actions) > 0:
                    self.action_issued = self.action_space.get(obs.observation.last_actions[0], "no_op")
                else:
                    self.action_issued = "no_op"

            # Saves last state and last action in a tuple
            self.state_tuple.append((self.minerals, self.vespene, self.food_used, self.food_cap, self.idle_workers,
                                     dict(self.units_amount), dict(self.enemy_units_amount),
                                     self.action_issued, bot_obj.steps))

            # Update any state that doesn't require actions
            self.minerals = obs.observation.player.minerals
            self.vespene = obs.observation.player.vespene
            self.food_used = obs.observation.player.food_used
            self.food_cap = obs.observation.player.food_cap
            self.idle_workers = obs.observation.player.idle_worker_count
            self.units_amount[units.Terran.SCV] = obs.observation.player.food_workers
            # Filter out SCVs before updating units_amount because they disappear when they go into refineries
            own_units = [u for u in obs.observation.raw_units
                         if u.alliance == 1 and u.unit_type != units.Terran.SCV]
            # Quickly checks if the state has changed. Not sure if actually faster.
            if len(own_units) != sum(self.units_amount.values())-self.units_amount[units.Terran.SCV]:
                own_unit_types = [u.unit_type for u in own_units]
                unit_types, unit_type_counts = np.unique(np.array(own_unit_types), return_counts=True)
                for (unit_type, unit_type_count) in zip(unit_types, unit_type_counts):
                    self.units_amount[unit_type] = unit_type_count

            # Counts enemy units
            enemy_units = [u for u in obs.observation.raw_units
                           if u.alliance == 4]
            enemy_unit_types = [u.unit_type for u in enemy_units]
            unit_types, unit_type_counts = np.unique(np.array(enemy_unit_types), return_counts=True)
            for (unit_type, unit_type_count) in zip(unit_types, unit_type_counts):
                self.enemy_units_amount[unit_type] = unit_type_count

            # Update the score and reward
            oldScore = self.score
            self.score = self.minerals + self.vespene + sum(self.units_amount.values()) * self.unit_weight
            self.reward = self.score - oldScore

            bot_obj.game_state_updated = True

            # Selects control group 9
            new_action = [actions.FUNCTIONS.select_control_group("recall", 9)]

        # Section for adding unselected production building to control group 9.
        # It only adds one building per state update to keep state update lengths consistent.
        # When at this stage, control group 9 should be selected.
        # This section should be ran even when the control group is correct.
        elif bot_obj.reqSteps == 3:
            unselected_production = self.get_unselected_production_buildings(obs, on_screen=False)
            if len(unselected_production) > 0:
                unit = random.choice(unselected_production)
                new_action = HelperClass.move_screen(obs, (unit.x, unit.y))
            bot_obj.reqSteps = 2

        elif bot_obj.reqSteps == 2:
            unselected_production = self.get_unselected_production_buildings(obs, on_screen=True)
            if len(unselected_production) > 0:
                unit = random.choice(unselected_production)
                new_action = [actions.FUNCTIONS.select_point(
                    "select",
                    (HelperClass.sigma(unit.x+random.randint(0, 3)),
                     HelperClass.sigma(unit.y+random.randint(0, 3))))]
            bot_obj.reqSteps = 1

        elif bot_obj.reqSteps == 1:
            # single_select is an array of zeros if nothing is selected.
            # The following line checks for when hp > 0 (i.e. a unit is actually selected)
            if obs.observation.single_select[0][2] > 0:
                if (obs.observation.single_select[0].unit_type == units.Terran.CommandCenter or
                        obs.observation.single_select[0].unit_type == units.Terran.Barracks or
                        obs.observation.single_select[0].unit_type == units.Terran.Factory or
                        obs.observation.single_select[0].unit_type == units.Terran.Starport):
                    new_action = [actions.FUNCTIONS.select_control_group("append", 9)]
            bot_obj.reqSteps = 0

        ActionSingleton().set_action(new_action)

    @staticmethod
    def get_unselected_production_buildings(obs, on_screen=False):
        """
        This methods returns a list of production buildings (buildings capable of producing units) that aren't
        in currently selected. Note that it doesn't count Barracks with tech labs.
        :param obs:
        :param on_screen: Whether or not the list should only contain units visible on the screen
        :return:
        """
        if on_screen:
            return [u for u in obs.observation.feature_units
                    if u.alliance == 1 and not u.is_selected
                    and (
                            u.unit_type == units.Terran.CommandCenter or
                            u.unit_type == units.Terran.Barracks or
                            u.unit_type == units.Terran.Factory or
                            u.unit_type == units.Terran.Starport
                    )]
        else:
            return [u for u in obs.observation.raw_units
                    if u.alliance == 1 and not u.is_selected
                    and (
                       u.unit_type == units.Terran.CommandCenter or
                       u.unit_type == units.Terran.Barracks or
                       u.unit_type == units.Terran.Factory or
                       u.unit_type == units.Terran.Starport
                    )]

    # Method for adding placed buildings to the building queue units_in_progress. Takes current camera_coordinate
    # and the unit type of the building placed.
    # Obsolete with raw_units.
    def add_unit_in_progress(self, bot_obj, camera_coordinate, screen_coordinate, unit_type):
        # Check if variable types are correct
        if not isinstance(camera_coordinate, list) and not isinstance(camera_coordinate, tuple):
            print("Type of camera_coordinate must be a list or tuple.")
            return False
        elif not isinstance(unit_type, int):
            print("Type of unit_type must be an integer.")
            return False
        else:  # Everything of correct type. Add to building queue
            old_camera_coordinate = camera_coordinate
            camera_coordinate = [coord for coord in old_camera_coordinate]
            camera_coordinate[0] = camera_coordinate[0] + (screen_coordinate[0]-42) / 84 * 7
            camera_coordinate[1] = camera_coordinate[1] + (screen_coordinate[1] - 42) / 84 * 7
            self.units_in_progress.append([camera_coordinate, unit_type, bot_obj.steps, False])
            return True

    # Method not finished. Supposed to check minimap for units
    def check_building_states_from_minimap(self, obs, building_type):
        building_states = self.get_building_states(building_type)

        found_states = []
        if len(building_states) != 0:
            for building in building_states:
                building_coordinate = building[0]
                player_relative_value = obs.observation.feature_minimap.player_relative[
                    int(round(building_coordinate[1]))][int(round(building_coordinate[0]))]
                if player_relative_value == 1:
                    found_states.append(building)
            self.set_building_states(building_type, found_states)
        else:
            print("No states for building type " + str(building_type) + ".")
            return False

        return True
