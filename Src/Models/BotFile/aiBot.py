import random
import statistics

from pysc2.agents import base_agent
from pysc2.lib import actions, units, features

from Models.BuildOrders.BuildOrders import BuildOrders
from Models.Attack.Attack import Attack


selectors = ['buildSelector', 'attackSelector']
attackSelector = ['attack']
buildSelector = ['build_scv', 'build_supply_depot',
                 'build_barracks', 'build_refinery', 'return_scv', 'expand']


class aiBot(base_agent.BaseAgent):
    def __init__(self):
        super(aiBot, self).__init__()
        self.base_location = None
        self.start_top = None
        self.attack_coordinates = None
        self.reqSteps = 0
        self.selector = None
        self.doBuild = None
        self.doAttack = None

    def step(self, obs):
        super(aiBot, self).step(obs)

        # first step
        if obs.first():
            start_y, start_x = (obs.observation.feature_minimap.player_relative
                                == features.PlayerRelative.SELF).nonzero()
            print(start_x)
            xmean = start_x.mean()
            ymean = start_y.mean()

            self.base_location = (xmean, ymean)
            if xmean <= 31 and ymean <= 31:
                self.Start_top = True
                self.attack_coordinates = (47, 47)
            else:
                self.Start_top = False
                self.attack_coordiantes = (12, 16)

        free_supply = (obs.observation.player.food_cap -
                       obs.observation.player.food_used)
        action = [actions.FUNCTIONS.no_op()]
        if self.reqSteps == 0:
            self.selector = "test"  # random.choice(selectors)

        if self.selector == "buildSelector":

            if self.reqSteps == 0:
                self.doBuild = random.choice(buildSelector)

            if self.doBuild == "expand":
                action = BuildOrders.expand(self, obs, self.start_top, 0)

            if self.doBuild == "build_scv":  # build scv
                action = BuildOrders.build_scv(self, obs, free_supply)

            elif self.doBuild == "build_supply_depot":  # build supply depot
                action = BuildOrders.build_supply_depot(self, obs, free_supply)

            elif self.doBuild == "build_barracks":
                action = BuildOrders.build_barracks(self, obs)

            elif self.doBuild == "build_refinery":
                action = BuildOrders.build_refinery(self, obs)

            elif self.doBuild == "return_scv":
                action = BuildOrders.return_scv(self, obs)

            elif self.selector == 'attackSelector':
                if self.reqSteps == 0:
                    self.doAttack = random.choice(attackSelector)

                if self.doAttack == "attack":
                    action = Attack.attack(self, obs, self.base_location)

        elif self.selector == "test":
            if BuildOrders.select_unit(self, obs, units.Terran.SCV):
                if BuildOrders.do_action(self, obs, actions.FUNCTIONS.Build_CommandCenter_screen.id):
                    minerals = BuildOrders.get_units(self, obs, units.Neutral.MineralField)
                    mineralx = [mineral.x for mineral in minerals]
                    mineraly = [mineral.y for mineral in minerals]

                    mineralsx = statistics.mean(mineralx)
                    mineralsy = statistics.mean(mineraly)
                    print(mineralsx)
                    print(mineralsy)

                    if mineralsx <= 42:
                        mineralsx += 7
                    else:
                        mineralsx -= 7

                    if mineralsy >= 42:
                        mineralsy += 2
                    else:
                        mineralsy -= 2
                    target = (mineralsx, mineralsy)

                    return actions.FUNCTIONS.Build_CommandCenter_screen("now", target)

            action = [actions.FUNCTIONS.move_camera((22, 18))]

            command_scv = BuildOrders.get_units(self, obs, units.Terran.SCV)
            if len(command_scv) > 0 and not BuildOrders.select_unit(self, obs, units.Terran.SCV):
                if (obs.observation.player.idle_worker_count > 0):
                    action = [actions.FUNCTIONS.select_idle_worker(
                        "select", obs, units.Terran.SCV)]
                else:
                    command = random.choice(command_scv)
                    action = [actions.FUNCTIONS.select_point(
                        "select", (BuildOrders.sigma(self, command.x),
                                   BuildOrders.sigma(self, command.y)))]

        return action[0]
