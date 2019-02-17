import random
from pysc2.agents import base_agent
from pysc2.lib import actions, units, features


class aiBot(base_agent.BaseAgent):
    def __init__(self):
        super(aiBot, self).__init__()
        self.base_location = None
        self.attack_coordinates = None
        self.reqSteps = 0
        self.currAct = 0
        self.queued = False

    def step(self, obs):
        super(aiBot, self).step(obs)

        # first step
        if obs.first():
            start_y, start_x = (obs.observation.feature_minimap.player_relative
                                == features.PlayerRelative.SELF).nonzero()
            xmean = start_x.mean()
            ymean = start_y.mean()

            self.base_location = (xmean, ymean)
            if xmean <= 31 and ymean <= 31:
                self.attack_coordinates = (47, 47)
            else:
                self.attack_coordiantes = (12, 16)

        if self.reqSteps == 0:
            self.currAct = random.randint(0, 4)

        free_supply = (obs.observation.player.food_cap -
                       obs.observation.player.food_used)

        if self.currAct == 0:  # build scv
            action = self.build_scv(obs, free_supply)

        elif self.currAct == 1:  # build supply depot
            action = self.build_supply_depot(obs, free_supply)

        elif self.currAct == 2:
            action = self.build_barracks(obs)

        elif self.currAct == 3:
            action = self.build_refinery(obs)

        elif self.currAct == 4:
            action = self.return_scv(obs)

        else:
            action = [actions.FUNCTIONS.no_op()]

        return action[0]

    def sigma(self, num):
        if num <= 0:
            return 0
        elif num >= 83:
            return 83
        else:
            return num

    def not_in_progress(self, obs, unit_type):
        units = self.get_units(obs, unit_type)
        for unit in units:
            if (unit.build_progress != 100):
                return False
        return True

    def not_in_queue(self, obs, unit_type):
        queues = obs.observation.build_queue
        if len(queues) > 0:
            for queue in queues:
                if queue[0] == unit_type:
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

    def do_action(self, obs, action):
        return action in obs.observation.available_actions

    def build_scv(self, obs, free_supply):
        new_action = [actions.FUNCTIONS.no_op()]
        command_centers = self.get_units(obs, units.Terran.CommandCenter)
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
                                                             (self.sigma(command_centers[0].x), self.sigma(command_centers[0].y)))]

        elif self.reqSteps == 1:
            self.reqSteps = 0
            if self.select_unit(obs, units.Terran.CommandCenter):
                if self.do_action(obs, actions.FUNCTIONS.Train_SCV_quick.id
                                  ) and self.not_in_queue(obs, units.Terran.CommandCenter
                                                          ) and free_supply > 0 and command_centers[0].assigned_harvesters < command_centers[0].ideal_harvesters:
                    new_action = [actions.FUNCTIONS.Train_SCV_quick("now")]

        return new_action

    def build_supply_depot(self, obs, free_supply):
        new_action = [actions.FUNCTIONS.no_op()]
        if self.reqSteps == 0:
            self.reqSteps = 2

        elif self.reqSteps == 2:
            self.reqSteps = 1
            command_scv = self.get_units(obs, units.Terran.SCV)
            if len(command_scv) > 0 and not self.select_unit(obs, units.Terran.SCV):
                if(obs.observation.player.idle_worker_count > 0):
                    new_action = [actions.FUNCTIONS.select_idle_worker(
                        "select", obs, units.Terran.SCV)]
                else:
                    command = random.choice(command_scv)
                    new_action = [actions.FUNCTIONS.select_point(
                        "select", (self.sigma(command.x), self.sigma(command.y)))]

        elif self.reqSteps == 1:
            self.reqSteps = 0
            if free_supply <= 4 and self.not_in_progress(obs, units.Terran.SupplyDepot):
                if self.select_unit(obs, units.Terran.SCV):
                    if self.do_action(obs, actions.FUNCTIONS.Build_SupplyDepot_screen.id):
                        x = random.randint(2, 81)
                        y = random.randint(2, 81)

                        new_action = [actions.FUNCTIONS.Build_SupplyDepot_screen("now", (x, y))]

        return new_action

    def build_barracks(self, obs):
        new_action = [actions.FUNCTIONS.no_op()]
        if self.reqSteps == 0:
            self.reqSteps = 2

        elif self.reqSteps == 2:
            self.reqSteps = 1
            command_scv = self.get_units(obs, units.Terran.SCV)
            if len(command_scv) > 0 and not self.select_unit(obs, units.Terran.SCV):
                if(obs.observation.player.idle_worker_count > 0):
                    new_action = [actions.FUNCTIONS.select_idle_worker(
                        "select", obs, units.Terran.SCV)]
                else:
                    command = random.choice(command_scv)
                    new_action = [actions.FUNCTIONS.select_point(
                        "select", (self.sigma(command.x), self.sigma(command.y)))]

        elif self.reqSteps == 1:
            self.reqSteps = 0
            barracks = self.get_units(obs, units.Terran.Barracks)
            if len(barracks) < 3 and self.not_in_progress(obs, units.Terran.Barracks):
                if self.select_unit(obs, units.Terran.SCV):
                    if self.do_action(obs, actions.FUNCTIONS.Build_Barracks_screen.id):
                        x = random.randint(2, 81)
                        y = random.randint(2, 81)

                        new_action = [actions.FUNCTIONS.Build_Barracks_screen("queued", (x, y))]

        return new_action

    def build_refinery(self, obs):
        new_action = [actions.FUNCTIONS.no_op()]
        if self.reqSteps == 0:
            self.reqSteps = 3

        elif self.reqSteps == 3:
            self.reqSteps = 2
            command_scv = self.get_units(obs, units.Terran.SCV)
            if len(command_scv) > 0 and not self.select_unit(obs, units.Terran.SCV):
                if(obs.observation.player.idle_worker_count > 0):
                    new_action = [actions.FUNCTIONS.select_idle_worker(
                        "select", obs, units.Terran.SCV)]
                else:
                    command = random.choice(command_scv)
                    new_action = [actions.FUNCTIONS.select_point(
                        "select", (self.sigma(command.x), self.sigma(command.y)))]

        elif self.reqSteps == 2:
            self.reqSteps = 1
            new_action = [
                actions.FUNCTIONS.move_camera(self.base_location)]

        elif self.reqSteps == 1:
            self.reqSteps = 0
            if obs.observation.player.food_used >= 20:
                if self.select_unit(obs, units.Terran.SCV):
                    if self.do_action(obs, actions.FUNCTIONS.Build_Refinery_screen.id):
                        geyser = self.get_units(obs, units.Neutral.VespeneGeyser)

                        new_action = [actions.FUNCTIONS.Build_Refinery_screen("now",
                                                                              (self.sigma(geyser[0].x), self.sigma(geyser[0].y)))]
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
            if self.select_unit(obs, units.Terran.SCV):
                minerals = self.get_units(obs, units.Neutral.MineralField)
                new_action = [actions.FUNCTIONS.Harvest_Gather_screen(
                    "now", (self.sigma(minerals[0].x), self.sigma(minerals[0].y)))]

        return new_action
