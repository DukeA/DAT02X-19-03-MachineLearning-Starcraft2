import random

from pysc2.agents import base_agent
from pysc2.lib import actions, units


class BuildOrders(base_agent.BaseAgent):
    def __init__(self):
        super(BuildOrders, self).__init__()
        self.base_location = None

    def build_barracks(self, obs):
        new_action = [actions.FUNCTIONS.no_op()]
        if self.reqSteps == 0:
            self.reqSteps = 2

        elif self.reqSteps == 2:
            self.reqSteps = 1
            command_scv = BuildOrders.get_units(self, obs, units.Terran.SCV)
            if len(command_scv) > 0 and not BuildOrders.select_unit(self, obs, units.Terran.SCV):
                if (obs.observation.player.idle_worker_count > 0):
                    new_action = [actions.FUNCTIONS.select_idle_worker(
                        "select", obs, units.Terran.SCV)]
                else:
                    command = random.choice(command_scv)
                    new_action = [actions.FUNCTIONS.select_point(
                        "select", (BuildOrders.sigma(self, command.x),
                                   BuildOrders.sigma(self, command.y)))]

        elif self.reqSteps == 1:
            self.reqSteps = 0
            barracks = BuildOrders.get_units(self, obs, units.Terran.Barracks)
            if len(barracks) < 3 and BuildOrders.not_in_progress(self, obs, units.Terran.Barracks):
                if BuildOrders.select_unit(self, obs, units.Terran.SCV):
                    if BuildOrders.do_action(self, obs, actions.FUNCTIONS.Build_Barracks_screen.id):
                        x = random.randint(2, 81)
                        y = random.randint(2, 81)

                        new_action = [actions.FUNCTIONS.Build_Barracks_screen("queued", (x, y))]

        return new_action

    def build_supply_depot(self, obs, free_supply):
        new_action = [actions.FUNCTIONS.no_op()]
        if self.reqSteps == 0:
            self.reqSteps = 2

        elif self.reqSteps == 2:
            self.reqSteps = 1
            command_scv = BuildOrders.get_units(self, obs, units.Terran.SCV)
            if len(command_scv) > 0 and not BuildOrders.select_unit(self, obs, units.Terran.SCV):
                if(obs.observation.player.idle_worker_count > 0):
                    new_action = [actions.FUNCTIONS.select_idle_worker(
                        "select", obs, units.Terran.SCV)]
                else:
                    command = random.choice(command_scv)
                    new_action = [actions.FUNCTIONS.select_point(
                        "select", (BuildOrders.sigma(self, command.x),
                                   BuildOrders.sigma(self, command.y)))]

        elif self.reqSteps == 1:
            self.reqSteps = 0
            if free_supply <= 4 and BuildOrders.not_in_progress(self, obs, units.Terran.SupplyDepot):
                if BuildOrders.select_unit(self, obs, units.Terran.SCV):
                    if BuildOrders.do_action(self, obs, actions.FUNCTIONS.Build_SupplyDepot_screen.id):
                        x = random.randint(2, 81)
                        y = random.randint(2, 81)

                        new_action = [actions.FUNCTIONS.Build_SupplyDepot_screen("now", (x, y))]

        return new_action

    def build_refinery(self, obs):
        new_action = [actions.FUNCTIONS.no_op()]
        if self.reqSteps == 0:
            self.reqSteps = 3

        elif self.reqSteps == 3:
            self.reqSteps = 2
            command_scv = BuildOrders.get_units(self, obs, units.Terran.SCV)
            if len(command_scv) > 0 and not BuildOrders.select_unit(self, obs, units.Terran.SCV):
                if (obs.observation.player.idle_worker_count > 0):
                    new_action = [actions.FUNCTIONS.select_idle_worker(
                        "select", obs, units.Terran.SCV)]
                else:
                    command = random.choice(command_scv)
                    new_action = [actions.FUNCTIONS.select_point(
                        "select", (BuildOrders.sigma(self, command.x),
                                   BuildOrders.sigma(self, command.y)))]

        elif self.reqSteps == 2:
            self.reqSteps = 1
            new_action = [
                actions.FUNCTIONS.move_camera(self.base_location)]

        elif self.reqSteps == 1:
            self.reqSteps = 0
            if obs.observation.player.food_used >= 20:
                if BuildOrders.select_unit(self, obs, units.Terran.SCV):
                    if BuildOrders.do_action(self, obs, actions.FUNCTIONS.Build_Refinery_screen.id):
                        geyser = BuildOrders.get_units(self, obs, units.Neutral.VespeneGeyser)

                        new_action = [actions.FUNCTIONS.Build_Refinery_screen("now",
                                                                              (BuildOrders.sigma(self, geyser[0].x),
                                                                               BuildOrders.sigma(self, geyser[0].y)))]
        return new_action

    def build_scv(self, obs, free_supply):
        new_action = [actions.FUNCTIONS.no_op()]
        command_centers = BuildOrders.get_units(self, obs, units.Terran.CommandCenter)
        if self.reqSteps == 0:
            self.reqSteps = 3

        elif (self.reqSteps == 3):
            self.reqSteps = 2
            new_action = [
                actions.FUNCTIONS.move_camera(self.base_location)
            ]

        elif self.reqSteps == 2:
            self.reqSteps = 1
            if len(command_centers) > 0:
                new_action = [actions.FUNCTIONS.select_point("select",
                                                             (BuildOrders.sigma(self, command_centers[0].x),
                                                              BuildOrders.sigma(self, command_centers[0].y)))]

        elif self.reqSteps == 1:
            self.reqSteps = 0
            if BuildOrders.select_unit(self, obs, units.Terran.CommandCenter):
                if BuildOrders.do_action(self, obs, actions.FUNCTIONS.Train_SCV_quick.id
                                         ) and BuildOrders.not_in_queue(self, obs, units.Terran.CommandCenter
                                                                        ) and free_supply > 0 and command_centers[0].assigned_harvesters < command_centers[0].ideal_harvesters:
                    new_action = [actions.FUNCTIONS.Train_SCV_quick("now")]

        return new_action

    def return_scv(self, obs):
        new_action = [actions.FUNCTIONS.no_op()]
        if self.reqSteps == 0:
            self.reqSteps = 3

        elif self.reqSteps == 3:
            self.reqSteps = 2
            if(obs.observation.player.idle_worker_count > 0):
                new_action = [actions.FUNCTIONS.select_idle_worker(
                    "select", obs, units.Terran.SCV)]

        elif self.reqSteps == 2:
            self.reqSteps = 1
            new_action = [
                actions.FUNCTIONS.move_camera(self.base_location)]

        elif self.reqSteps == 1:
            self.reqSteps = 0
            if BuildOrders.select_unit(self, obs, units.Terran.SCV):
                minerals = BuildOrders.get_units(self, obs, units.Neutral.MineralField)
                new_action = [actions.FUNCTIONS.Harvest_Gather_screen(
                    "now", (BuildOrders.sigma(self, minerals[0].x),
                            BuildOrders.sigma(self, minerals[0].y)))]

        return new_action

    def sigma(self, num):
        if num <= 0:
            return 0
        elif num >= 83:
            return 83
        else:
            return num

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
        units = BuildOrders.get_units(self, obs, unit_type)
        for unit in units:
            if (unit.build_progress != 100):
                return False
        return True

    def get_units(self, obs, unit_type):
        return [unit for unit in obs.observation.feature_units
                if unit.unit_type == unit_type]

    def select_unit(self, obs, unit_type):
        if (len(obs.observation.single_select) > 0 and
                obs.observation.single_select[0].unit_type == unit_type):
            return True

        if (len(obs.observation.multi_select) > 0 and
                obs.observation.multi_select[0].unit_type == unit_type):
            return True

        return False