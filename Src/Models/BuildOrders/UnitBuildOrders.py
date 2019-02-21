import  random


from pysc2.agents import base_agent
from pysc2.lib import actions,units




class UnitOrders(base_agent.BaseAgent):
    def __init__(self):
        super(UnitOrders,self).__init__()


    def build_Marines(self,obs ,free_supply):
        new_action = [actions.FUNCTIONS.no_op()]
        barracks = UnitOrders.get_units(self, obs, units.Terran.Barracks)
        if self.reqSteps == 0:
            self.reqSteps = 2

        elif self.reqSteps == 2:
            self.reqSteps = 1
            if len(barracks) > 0:
                new_action = [actions.FUNCTIONS.select_point("select",
                                                             (UnitOrders.sigma(self, barracks[0].x),
                                                              UnitOrders.sigma(self, barracks[0].y)))]
        elif self.reqSteps ==1:
            self.reqSteps=0
            if len(barracks) > 0:
                if UnitOrders.select_unit(self,obs,units.Terran.Barracks):
                    if UnitOrders.do_action\
                        (self,obs,actions.FUNCTIONS.Train_Marine_quick.id
                        )  and free_supply>0:
                        new_action = [actions.FUNCTIONS.Train_Marine_quick("now")]
        return  new_action;

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
        units = UnitOrders.get_units(self, obs, unit_type)
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
