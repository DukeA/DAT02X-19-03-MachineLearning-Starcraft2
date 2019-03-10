import random
import numpy as np

from pysc2.agents import base_agent
from pysc2.lib import actions, units, features

from Models.Predefines.Coordinates import Coordinates
from Models.BuildOrders.ActionSingleton import ActionSingleton


class DistributeSCV:

    def __init__(self):
        super(DistributeSCV, self).__init__()
        self.curr_CC = 0
        self.curr_step = 0
        self.min_num_mineral_harvesters = 4
        self.refinery_desired_harvesters = 3
        self.first_scv_selected = False
        self.camera_moved = False
        self.num_CC_refineries_checked = 0
        self.num_CC_minerals_checked = 0
        self.all_refineries_checked = False
        self.all_CC_checked = False
        self.num_CC_minerals_incremented = False
        self.num_command_centers = 0

    def distribute_scv(self, obj, obs, base_location, num_expansions):  # Use State class to get num expansions later
        new_action = [actions.FUNCTIONS.no_op()]  # No action by default
        steps_needed = 2  # Actions needed at each Command Center

        command_centers_pos = [base_location]

        if base_location[0] < 32:  # Check which side of the map the starting base is located
            command_centers_pos.extend(Coordinates.EXPO_LOCATIONS[0:num_expansions])
        else:
            command_centers_pos.extend(Coordinates.EXPO_LOCATIONS2[0:num_expansions])

        if obj.reqSteps == 0:
            obj.reqSteps = 1

        #if self.curr_step < 200:
        #    self.curr_step += 1
        #    new_action = [actions.FUNCTIONS.no_op()]
        #    ActionSingleton().set_action(new_action)
        #    return

        pos = command_centers_pos[self.curr_CC]

        command_centers = self.get_units_by_type(obs, units.Terran.CommandCenter)

        if self.curr_step % steps_needed == 0:  # If all actions for this Command Center are performed, move the
            if not self.camera_moved:               # camera and increment/reset required variables
                new_action = [actions.FUNCTIONS.move_camera(pos)]
                self.curr_step -= 1
                self.curr_CC -= 1
                self.camera_moved = True
                self.num_CC_minerals_incremented = False
                if not self.all_refineries_checked:
                    self.first_scv_selected = False
            elif self.camera_moved:
                self.camera_moved = False
                #  If on the first loop through expo locations and there is a command center, add this to the total num
                if self.curr_step < 2*len(command_centers_pos) and len(command_centers) > 0:
                    self.num_command_centers += 1

        elif self.curr_step % steps_needed == 1:  #

            if len(command_centers) > 0:  # Check that command center exists
                command_center = command_centers[0]

                refineries = self.get_units_by_type(obs, units.Terran.Refinery)

                refineries_not_ideal = [refinery for refinery in refineries  # Get refineries with non-desired amount of SCV:s
                                        if refinery.assigned_harvesters != self.refinery_desired_harvesters
                                        and refinery.build_progress == 100]

                if len(refineries_not_ideal) > 0:
                    refinery = refineries_not_ideal[0]  # Pick one of the refineries

                    #  Calculate the difference between the current amount of SCV:s and the desired amount
                    refinery_scv_ideal_diff = refinery.assigned_harvesters - self.refinery_desired_harvesters

                    #  Check how many units are selected currently
                    units_selected = [unit for unit in obs.observation.feature_units if unit.is_selected]
                    num_units_selected = len(units_selected)

                    #  Check if this refinery has too few SCV:s
                    if refinery_scv_ideal_diff < 0 and command_center.assigned_harvesters > self.min_num_mineral_harvesters:

                        #  If fewer than the number of SCV:s missing are selected, select from mineral line
                        if num_units_selected < abs(refinery_scv_ideal_diff) or not self.first_scv_selected:

                            #  Check if first SCV for this refinery has been selected.
                            #  If so, use "toggle", otherwise "select".
                            if not self.first_scv_selected:
                                action_type = "select"
                                self.first_scv_selected = True
                            else:
                                action_type = "toggle"

                            new_action = self.select_single_scv_at_minerals(obs, action_type, (refinery.x, refinery.y))

                        #  If more than the number of SCV:s missing are selected, deselect at index 0 (first position)
                        elif num_units_selected > abs(refinery_scv_ideal_diff):
                            new_action = self.deselect_at_index(obs, 0)
                            self.first_scv_selected = False

                        #  If the right amount of SCV:s are selected, assign these to harvest at the refinery
                        elif num_units_selected == abs(refinery_scv_ideal_diff):
                            if refinery.x > 0 and refinery.y > 0 and refinery.x < 84 and refinery.y < 84:
                                new_action = [actions.FUNCTIONS.Harvest_Gather_screen("now", (refinery.x, refinery.y))]
                                self.first_scv_selected = False

                    #  Check if this refinery has too many SCV:s
                    elif refinery_scv_ideal_diff > 0:

                        #  Check if the number of SCV:s selected is fewer than the amount too many.
                        #  Also check if the first SCV from this refinery has been selected, otherwise select it.
                        if num_units_selected < refinery_scv_ideal_diff or self.first_scv_selected:

                            #  To make sure SCV:s harvesting at the refinery are selected, select the closest SCV
                            scvs_on_screen = self.get_units_by_type(obs, units.Terran.SCV)
                            min_dist = 100
                            scv_selected = None
                            for scv in scvs_on_screen:
                                dist = (scv.x - refinery.x) ** 2 + (scv.y - refinery.y) ** 2
                                if dist < min_dist:
                                    min_dist = dist
                                    scv_selected = scv

                            #  Check if first SCV for this refinery has been selected.
                            #  If so, use "toggle", otherwise "select".
                            if not self.first_scv_selected:
                                action_type = "select"
                                self.first_scv_selected = True
                            else:
                                action_type = "toggle"
                            new_action = [actions.FUNCTIONS.select_point(action_type, (scv_selected.x, scv_selected.y))]
                        # Check if the number of SCV:s selected is more than the amount too many. If so, deselect.
                        elif num_units_selected > refinery_scv_ideal_diff:
                            new_action = self.deselect_at_index(obs, 0)
                            self.first_scv_selected = False
                        #  Check if the number of SCV:s selected is the amount too many. If so, send to harvest minerals
                        elif num_units_selected == refinery_scv_ideal_diff:
                            minerals_on_screen = self.get_units_by_type(obs, units.Neutral.MineralField)
                            mineral = random.choice(minerals_on_screen)
                            new_action = [actions.FUNCTIONS.Harvest_Gather_screen("now", (mineral.x, mineral.y))]
                            self.first_scv_selected = False
                    #  If refinery has the right amount of SCV:s, reset the first selected variable
                    else:
                        self.first_scv_selected = False

                    #  If code gets here, this section needs to be repeated at least one more time, so subtract 1
                    #  from the iteration variable
                    self.curr_step -= 1

                #  Check if all refineries are checked for the current Command Center
                elif len(refineries_not_ideal) == 0 and not self.all_refineries_checked:
                    self.num_CC_refineries_checked += 1

                #  Check if all refineries are checked for all Command Centers
                if len(refineries_not_ideal) == 0 and self.num_CC_refineries_checked == self.num_command_centers \
                        and not self.all_refineries_checked:
                    self.all_refineries_checked = True

                #  Check if all refineries for all Command Centers are checked. If so, start distributing mineral SCV:s
                if self.all_refineries_checked:

                    #  Check if all Command Centers have less than maximum amount of mineral harvesting SCV:s
                    if abs(self.num_CC_minerals_checked) != self.num_command_centers:

                        #  Calculate the difference between the assigned and ideal amount of mineral harvesting SCV:s
                        scv_ideal_diff = command_center.assigned_harvesters - command_center.ideal_harvesters

                        if obs.observation.single_select[0][0] != 0:
                            num_units_selected = 1
                        else:
                            num_units_selected = len(obs.observation.multi_select)

                        # Check if number of SCV:s is more than ideal
                        if scv_ideal_diff > 0:

                            if not self.num_CC_minerals_incremented:
                                if self.num_CC_minerals_checked < 0:
                                    self.num_CC_minerals_checked = 0
                                self.num_CC_minerals_checked += 1
                                self.num_CC_minerals_incremented = True

                            if not self.first_scv_selected:
                                action_type = "select"
                                self.first_scv_selected = True
                                new_action = self.select_single_scv_at_minerals(obs, action_type, "mean")
                            else:
                                action_type = "toggle"

                                if num_units_selected < scv_ideal_diff:
                                    new_action = self.select_single_scv_at_minerals(obs, action_type, "mean")
                                elif num_units_selected > scv_ideal_diff:
                                    new_action = self.deselect_at_index(obs, 0)

                            if num_units_selected != scv_ideal_diff:  # If the right amount is not selected, loop again
                                self.curr_step -= 1

                        elif scv_ideal_diff <= 0:  # Check if number of SCV:s is less than or equal to ideal amount

                            if not self.num_CC_minerals_incremented:
                                if self.num_CC_minerals_checked > 0:
                                    self.num_CC_minerals_checked = 0
                                self.num_CC_minerals_checked -= 1
                                self.num_CC_minerals_incremented = True

                            #  Check if number of SCV:s is less than ideal
                            if scv_ideal_diff < 0 and self.first_scv_selected:

                                #  Check if number selected is more than the amount missing. If so, deselect.
                                if num_units_selected > abs(scv_ideal_diff):
                                    new_action = self.deselect_at_index(obs, 0)
                                    self.curr_step -= 1
                                #  If the amount selected is not more than the amount missing but more than 1, send
                                #  these SCV:s to harvest at this Command Center
                                elif num_units_selected > 0:

                                    minerals_on_screen = self.get_units_by_type(obs, units.Neutral.MineralField)
                                    mineral = random.choice(minerals_on_screen)

                                    new_action = [
                                        actions.FUNCTIONS.Harvest_Gather_screen("now", [mineral.x, mineral.y])]

                                    self.first_scv_selected = False

                    #  Check if all Command Centers have less than maximum amount of mineral harvesting SCV:s
                    elif abs(self.num_CC_minerals_checked) == self.num_command_centers\
                            and self.curr_step >= 2*len(command_centers_pos):
                        self.all_CC_checked = True

        self.curr_step += 1

        if self.curr_step % steps_needed == 0:
            self.curr_CC += 1
            if self.curr_CC == len(command_centers_pos):
                self.curr_CC = 0

        if self.all_CC_checked:  # or self.curr_step > 600
            new_action = [actions.FUNCTIONS.no_op()]
            obj.action_finished = True
            obj.reqSteps = 0

        ActionSingleton().set_action(new_action)
        return

    def get_units_by_type(self, obs, unit_type):
        return [unit for unit in obs.observation.feature_units
                if unit.unit_type == unit_type]

    def select_single_scv_at_minerals(self, obs, select_type, closest_to_point):
        action = [actions.FUNCTIONS.no_op()]

        minerals_on_screen = self.get_minerals_on_screen(obs)

        if len(minerals_on_screen) > 0:
            x_min = min(o.x for o in minerals_on_screen)
            x_max = max(o.x for o in minerals_on_screen)
            y_min = min(o.y for o in minerals_on_screen)
            y_max = max(o.y for o in minerals_on_screen)

            if x_min > 0 and y_min > 0 and x_max < 84 and y_max < 84:
                scvs_on_screen = self.get_units_by_type(obs, units.Terran.SCV)

                scvs_at_minerals = [scv for scv in scvs_on_screen if
                                    scv.x > x_min and scv.x < x_max and scv.y > y_min and scv.y < y_max and not scv.is_selected]
                if closest_to_point == "any":
                    scv = random.choice(scvs_at_minerals)
                else:
                    if closest_to_point == "mean":
                        point = [np.mean([o.x for o in minerals_on_screen]), np.mean([o.y for o in minerals_on_screen])]
                    else:
                        point = closest_to_point
                    min_dist = 84 ** 2
                    closest_scv = random.choice(scvs_at_minerals)
                    for scv in scvs_at_minerals:
                        scv_dist = (scv.x - point[0]) ** 2 + (scv.y - point[1]) ** 2
                        if scv_dist < min_dist:
                            # if scv.is_selected == 0:
                            min_dist = scv_dist
                            closest_scv = scv
                    scv = closest_scv

                action = [actions.FUNCTIONS.select_point(select_type, (scv.x, scv.y))]

        return action

    def get_minerals_on_screen(self, obs):
        return [unit for unit in obs.observation.feature_units
                if unit.unit_type == units.Neutral.MineralField
                or unit.unit_type == units.Neutral.MineralField750
                or unit.unit_type == units.Neutral.RichMineralField
                or unit.unit_type == units.Neutral.RichMineralField750
                or unit.unit_type == units.Neutral.PurifierMineralField
                or unit.unit_type == units.Neutral.PurifierMineralField750]

    def select_all_scv_at_minerals(self, obs):
        action = [actions.FUNCTIONS.no_op()]

        minerals_on_screen = self.get_units_by_type(obs, units.Neutral.MineralField)
        if len(minerals_on_screen) > 0:
            x_min = min(o.x for o in minerals_on_screen)
            x_max = max(o.x for o in minerals_on_screen)
            y_min = min(o.y for o in minerals_on_screen)
            y_max = max(o.y for o in minerals_on_screen)

            if x_min > 0 and y_min > 0 and x_max < 84 and y_max < 84:
                action = [actions.FUNCTIONS.select_rect("select", (x_min, y_min), (x_max, y_max))]

        return action

    def deselect_at_index(self, obs, index):

        action = [actions.FUNCTIONS.select_unit(
            "deselect",
            index
        )]
        return action

    def select_num_workers_around_base(self, obs, unit_type, num, command_center_pos):
        action = [actions.FUNCTIONS.no_op()]
        units_on_screen = self.get_units_by_type(obs, unit_type)

        if len(units_on_screen) > 0:
            units_selected = obs.observation.multi_select
            num_units_selected = len(units_selected)
            # print('Num selected:' + str(current_excess_scvs))
            if num_units_selected < num:
                unit = units_on_screen[0]
                print(unit)
                if unit.x > 0 and unit.y > 0 and unit.x < 84 and unit.y < 84:
                    action = [actions.FUNCTIONS.select_point(
                        "select_all_type", (
                            unit.x,
                            unit.y
                        ))]
            elif num_units_selected > num:

                action = [actions.FUNCTIONS.select_unit(
                    "deselect",
                    0
                )]

        return action
