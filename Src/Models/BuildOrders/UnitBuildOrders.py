
from pysc2.agents import base_agent
from pysc2.lib import actions, units

from Models.BuildOrders.ActionSingelton import ActionSingelton

"""
@Author :Adam Grandén
The UnitBuildOrders  is the class which builds units
from the specfic infrastrucutre in this case to build marines from barracks
"""


class UnitBuildOrders(base_agent.BaseAgent):
    def __init__(self):
        super(UnitBuildOrders, self).__init__()
        self.new_action = None

    def build_marines(self, obs, free_supply):
        new_action = [actions.FUNCTIONS.no_op()]
        barracks_location = UnitBuildOrders.findall_barracks(self, obs)
        for this_barrack in barracks_location:
            if self.reqSteps == 0:
                self.reqSteps = 2
            elif self.reqSteps == 2:
                self.reqSteps = 1
                if len(barracks_location) > 0:
                    new_action = \
                        [actions.FUNCTIONS.select_point("select", (UnitBuildOrders.sigma(self, this_barrack.x),
                                                                   UnitBuildOrders.sigma(self, this_barrack.y)))]
            elif self.reqSteps == 1:
                self.reqSteps = 0
                if len(barracks_location) > 0:
                    if UnitBuildOrders.select_unit(self, obs, units.Terran.Barracks):
                        if UnitBuildOrders.do_action(self, obs, actions.FUNCTIONS.Train_Marine_quick.id)\
                                and free_supply > 0:
                            new_action = [actions.FUNCTIONS.Train_Marine_quick("now")]
        ActionSingelton().set_action(new_action)

    def build_marauder(self, obs, free_supply):
        new_action = [actions.FUNCTIONS.no_op()]

        if self.reqSteps == 0:
            self.reqSteps = 3

        if self.reqSteps == 3:
            self.reqSteps = 2
            # or maybe another location if we have one for barracks
            new_action = [actions.FUNCTIONS.move_camera(self.base_location)]

        elif self.reqSteps == 2:
            self.reqSteps = 1
            barracks = UnitBuildOrders.get_units(self, obs, units.Terran.Barracks)
            if len(barracks) > 0:
                new_action = \
                    [actions.FUNCTIONS.select_point("select_all_type", (UnitBuildOrders.sigma(self, barracks[0].x),
                                                                        UnitBuildOrders.sigma(self, barracks[0].y)))]
        elif self.reqSteps == 1:
            self.reqSteps = 0
            if UnitBuildOrders.select_unit(self, obs, units.Terran.Barracks):
                if UnitBuildOrders.do_action(self, obs, actions.FUNCTIONS.Train_Marauder_quick.id):
                    new_action = [actions.FUNCTIONS.Train_Marauder_quick("now")]
        ActionSingelton().set_action(new_action)

    def build_medivac(self, obs, free_supply):
        new_action = [actions.FUNCTIONS.no_op()]
        if self.reqSteps == 0:
            self.reqSteps = 3

        if self.reqSteps == 3:
            self.reqSteps = 2
            # or maybe another location if we have one for starport
            new_action = [actions.FUNCTIONS.move_camera(self.base_location)]

        elif self.reqSteps == 2:
            self.reqSteps = 1
            starports = UnitBuildOrders.get_units(self, obs, units.Terran.Starport)
            if len(starports) > 0:
                new_action = \
                    [actions.FUNCTIONS.select_point("select_all_type", (UnitBuildOrders.sigma(self, starports[0].x),
                                                                        UnitBuildOrders.sigma(self, starports[0].y)))]
        elif self.reqSteps == 1:
            self.reqSteps = 0
            if UnitBuildOrders.select_unit(self, obs, units.Terran.Starport):
                if UnitBuildOrders.do_action(self, obs, actions.FUNCTIONS.Train_Medivac_quick.id):
                    new_action = [actions.FUNCTIONS.Train_Medivac_quick("now")]
        ActionSingelton().set_action(new_action)

    def findall_barracks(self, obs):
        barracks_location = []
        barracks = UnitBuildOrders.get_units(self, obs, units.Terran.Barracks)
        for barrack_unit in barracks:
            barracks_location.append(barrack_unit)
        return barracks_location

    def set_action(self, action):
        self.new_action = action

    def get_action(self):
        return self.new_action

    def get_units(self, obs, unit_type):
        return [unit for unit in obs.observation.feature_units
                if unit.unit_type == unit_type]

    def do_action(self, obs, action):
        return action in obs.observation.available_actions

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

    def not_in_progress(self, obs, unit_type):
        units = UnitBuildOrders.get_units(self, obs, unit_type)
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
