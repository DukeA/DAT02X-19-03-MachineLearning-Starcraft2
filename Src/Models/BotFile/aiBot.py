import random
from pysc2.agents import base_agent
from pysc2.lib import actions, units, features


class aiBot(base_agent.BaseAgent):
    def __init__(self):
        super(aiBot, self).__init__()
        self.base_location = None
        self.attack_coordinates = None

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

        # Function for sending idle workers to mine
        action = random.randint(0, 1)

        free_supply = (obs.observation.player.food_cap -
                       obs.observation.player.food_used)
        # Function for building a supplyDepot on a Random Place
        # of the obeservable universe
        if action == 0:
            command_centers = self.get_units(obs, units.Terran.CommandCenter)
            if len(command_centers) > 0 and not self.select_unit(obs, units.Terran.CommandCenter):
                return actions.FUNCTIONS.select_point("select",
                                                      (self.sigma(command_centers[0].x), self.sigma(command_centers[0].y)))

            if self.select_unit(obs, units.Terran.CommandCenter):
                if self.do_action(obs, actions.FUNCTIONS.Train_SCV_quick.id
                                  ) and self.not_in_queue(obs, units.Terran.CommandCenter
                                                          ) and (command_centers[0].assigned_harvesters < command_centers[0].ideal_harvesters
                                                                 ) and free_supply > 2:
                    return actions.FUNCTIONS.Train_SCV_quick("now")

        elif action == 1:
            command_scv = self.get_units(obs, units.Terran.SCV)
            if len(command_scv) > 0 and not self.select_unit(obs, units.Terran.SCV):
                if(obs.observation.player.idle_worker_count > 0):
                    return actions.FUNCTIONS.select_idle_worker("select", obs, units.Terran.SCV)
                command = random.choice(command_scv)
                return actions.FUNCTIONS.select_point("select", (self.sigma(command.x), self.sigma(command.y)))

        barracks = self.get_units(obs, units.Terran.Barracks)
        if len(barracks) == 0:
            if self.select_unit(obs, units.Terran.SCV):
                if self.do_action(obs, actions.FUNCTIONS.Build_Barracks_screen.id):
                    x = random.randint(2, 81)
                    y = random.randint(2, 81)

                    return actions.FUNCTIONS.Build_Barracks_screen("now", (x, y))

        if free_supply <= 4 and self.not_in_progress(obs, units.Terran.SupplyDepot):
            if self.select_unit(obs, units.Terran.SCV):
                if self.do_action(obs, actions.FUNCTIONS.Build_SupplyDepot_screen.id):
                    x = random.randint(2, 81)
                    y = random.randint(2, 81)

                    return actions.FUNCTIONS.Build_SupplyDepot_screen("now", (x, y))

        if obs.observation.player.food_used >= 20:
            if self.select_unit(obs, units.Terran.SCV):
                if self.do_action(obs, actions.FUNCTIONS.Build_Refinery_screen.id):
                    geyser = self.get_units(obs, units.Neutral.VespeneGeyser)

                    return actions.FUNCTIONS.Build_Refinery_screen("now",
                                                                   (self.sigma(geyser[0].x), self.sigma(geyser[0].y)))

        if self.select_unit(obs, units.Terran.SCV):
            actions.FUNCTIONS.move_camera("now", obs, self.base_location)
            minerals = self.get_units(obs, units.Neutral.MineralField)
            return actions.FUNCTIONS.Harvest_Gather_screen(
                "now", (self.sigma(minerals[0].x), self.sigma(minerals[0].y)))

        return actions.FUNCTIONS.no_op()

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
