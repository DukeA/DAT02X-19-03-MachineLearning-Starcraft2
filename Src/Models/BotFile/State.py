import random
import numpy as np
import statistics

from pysc2.lib import actions, units, features
from collections import defaultdict

from Models.BuildOrders.ActionSingleton import ActionSingleton


class State:
    def __init__(self):

        # Game state

        self.units_amount = defaultdict(lambda: 0)  # Amount of each unit. Set to 0 by default
        self.minerals = 0
        self.vespene = 0
        self.score = 0
        self.reward = 0

        # Variables required for updating the game state

        # Information about buildings placed but not yet found is stored here on the form
        # [coordinate, unit_type, step it was created, if it has been found]
        self.units_in_progress = []
        self.update_steps_per_unit = 4  # Steps required to add each unit in units_in_progress to a control group
        self.update_building_step_threshold = 400  # Threshold steps for finding a building before it's removed from
        self.units_amounts_updated = False
        self.unit_weight = 50

    def update_state(self, bot_obj, obs):
        new_action = [actions.FUNCTIONS.no_op()]  # No action by default

        if bot_obj.reqSteps == 0:
            # Update any state that doesn't require actions
            self.minerals = obs.observation.player.minerals
            self.vespene = obs.observation.player.vespene
            self.units_amount[units.Terran.Marine.value] = obs.observation.player.army_count  # Temporary solution

            # Update the score and reward
            oldScore = self.score
            self.score = self.minerals + self.vespene + sum(self.units_amount.values()) * self.unit_weight
            self.reward = self.score - oldScore

            # Check if the total amount of units stored is the same as the amount seen in control group 9
            if obs.observation.control_groups[9][1] != \
                    sum(self.units_amount.values()) - obs.observation.player.army_count:
                new_action = [actions.FUNCTIONS.select_control_group("recall", 9)]
                bot_obj.reqSteps = 1
            else:
                if not self.units_amounts_updated:
                    self.units_amounts_updated = True

                # Check if there are buildings queued that need to be found.
                if len(self.units_in_progress) > 0:
                    bot_obj.reqSteps = len(self.units_in_progress)*self.update_steps_per_unit
                else:
                    bot_obj.game_state_updated = True

        elif bot_obj.reqSteps > 0:  # Check if method needs to perform actions
            bot_obj.reqSteps -= 1

            # Section for adding units from the queue units_in_progress to control group 9
            if len(self.units_in_progress) > 0 and self.units_amounts_updated:
                index = bot_obj.reqSteps // self.update_steps_per_unit  # Current index in units_in_progress queue
                curr_unit = self.units_in_progress[index]

                if bot_obj.reqSteps % self.update_steps_per_unit == 3:
                    new_action = [actions.FUNCTIONS.select_control_group("recall", 9)]  # Select control group

                elif bot_obj.reqSteps % self.update_steps_per_unit == 2:
                    new_action = [actions.FUNCTIONS.move_camera(curr_unit[0])]  # Move camera

                elif bot_obj.reqSteps % self.update_steps_per_unit == 1:
                    # Look for units of the right type that aren't already in the selected control group.
                    found_units = [unit for unit in obs.observation.feature_units
                                   if unit.unit_type == curr_unit[1] and not unit.is_selected]
                    if len(found_units) > 0:  # If units are found, select the first one (arbitrarily, could choose any)
                        selected_unit = found_units[0]
                        curr_unit[3] = True  # Set the unit as "found" so it can be added in the next step
                        self.units_in_progress[index] = curr_unit
                        # Select the unit. Random perturbation added so a slightly different point is
                        # selected each time, in case some other unit is blocking the unit found.
                        new_action = [actions.FUNCTIONS.select_point("select", (selected_unit.x+random.randint(0, 3),
                                                                                selected_unit.y+random.randint(0, 3)))]
                elif bot_obj.reqSteps % self.update_steps_per_unit == 0:
                    if curr_unit[3]:  # Check if the current unit was found in the previous step
                        # If it was found but the type is wrong, go back to the previous step and select again
                        if obs.observation.single_select[0][0] != curr_unit[1]:
                            bot_obj.reqSteps += 2
                        else:  # If the unit found is of the right type, add it to control group 9
                            self.units_amount[curr_unit[1]] = self.units_amount[curr_unit[1]] + 1
                            new_action = [actions.FUNCTIONS.select_control_group("append", 9)]
                            del self.units_in_progress[index]  # Remove if from the queue
                    # If the unit wasn't found and the amount of steps passed since it was queued is above the
                    # threshold, remove it from the queue. Something likely interrupted the building process
                    elif not curr_unit[3] and bot_obj.steps - curr_unit[2] > self.update_building_step_threshold:
                        del self.units_in_progress[index]

            # Section that runs on the last step of a series of actions
            # (this part won't be reached unless reqSteps was previously > 0 during this method call).
            if bot_obj.reqSteps == 0:  # Everything has been checked. Set game state to updated
                if self.units_amounts_updated:
                    bot_obj.game_state_updated = True
                    self.units_amounts_updated = False
                # If this step is reached, the total unit amount stored doesn't correspond to the control
                # group amount. Therefore, update all unit amounts from the control group
                else:
                    units_selected = obs.observation.multi_select
                    units_selected_types = [unit.unit_type for unit in units_selected]
                    unit_types, unit_type_counts = np.unique(np.array(units_selected_types), return_counts=True)
                    for (unit_type, unit_type_count) in zip(unit_types, unit_type_counts):
                        self.units_amount[unit_type] = unit_type_count

        ActionSingleton().set_action(new_action)

    # Method for adding placed buildings to the building queue units_in_progress. Takes current camera_coordinate
    # and the unit type of the building placed.
    def add_unit_in_progress(self, bot_obj, camera_coordinate, screen_coordinate, unit_type):
        # Check if variable types are correct
        if not isinstance(camera_coordinate, list) and not isinstance(camera_coordinate, tuple):
            print("Type of camera_coordinate must be a list or tuple.")
            return False
        elif not isinstance(unit_type, int):
            print("Type of unit_type must be an integer.")
            return False
        else:  # Everything of correct type. Add to building queue
            if screen_coordinate[1] > 42:
                old_camera_coordinate = camera_coordinate
                camera_coordinate = [coord for coord in old_camera_coordinate]
                camera_coordinate[1] = camera_coordinate[1] + 3
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
