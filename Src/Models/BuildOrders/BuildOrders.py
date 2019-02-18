import random

from pysc2.agents import base_agent
from pysc2.lib import actions, units, features

class BuildOrders(base_agent.BaseAgent):
    def __init__(self):
        super(BuildOrders, self).__init__()
        self.reqSteps=0


    def build_barracks(self,obs,reqSteps):
        new_action = [actions.FUNCTIONS.no_op()]
        if reqSteps == 0:
            self.reqSteps = 2

        elif reqSteps == 2:
            self.reqSteps = 1
            command_scv = self.get_units(obs, units.Terran.SCV)
            if len(command_scv) > 0 and not self.select_unit(obs, units.Terran.SCV):
                if (obs.observation.player.idle_worker_count > 0):
                    new_action = [actions.FUNCTIONS.select_idle_worker(
                        "select", obs, units.Terran.SCV)]
                else:
                    command = random.choice(command_scv)
                    new_action = [actions.FUNCTIONS.select_point(
                        "select", (self.sigma(command.x), self.sigma(command.y)))]

        elif reqSteps == 1:
            self.reqSteps = 0
            barracks = self.get_units(obs, units.Terran.Barracks)
            if len(barracks) < 3 and self.not_in_progress(obs, units.Terran.Barracks):
                if self.select_unit(obs, units.Terran.SCV):
                    if self.do_action(obs, actions.FUNCTIONS.Build_Barracks_screen.id):
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

    def build_refinery(self, obs):
        new_action = [actions.FUNCTIONS.no_op()]
        if self.reqSteps == 0:
            self.reqSteps = 3

        elif self.reqSteps == 3:
            self.reqSteps = 2
            command_scv = self.get_units(obs, units.Terran.SCV)
            if len(command_scv) > 0 and not self.select_unit(obs, units.Terran.SCV):
                if (obs.observation.player.idle_worker_count > 0):
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
                                                                              (self.sigma(geyser[0].x),
                                                                               self.sigma(geyser[0].y)))]
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
        units = self.get_units(obs, unit_type)
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