
from pysc2.agents import base_agent
from pysc2.lib import actions,units

from Models.BuildOrders.ActionSingelton import ActionSingelton
from Models.HelperClass.HelperClass import HelperClass

"""
@Author :Adam Grandén
The UnitBuildOrders  is the class which builds units 
from the specfic infrastrucutre in this case to build marines from barracks 
"""

class UnitBuildOrders(base_agent.BaseAgent):
    def __init__(self):
        super(UnitBuildOrders,self).__init__()
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
                        [actions.FUNCTIONS.select_point("select",(HelperClass.sigma(self, this_barrack.x),
                                                              HelperClass.sigma(self, this_barrack.y)))]
            elif self.reqSteps == 1:
                self.reqSteps=0
                if len(barracks_location) > 0:
                    if HelperClass.select_unit(self,obs,units.Terran.Barracks):
                        if HelperClass.do_action(self,obs,actions.FUNCTIONS.Train_Marine_quick.id)\
                                and free_supply > 0:
                            new_action = [actions.FUNCTIONS.Train_Marine_quick("now")]
        ActionSingelton().set_action(new_action)

    def findall_barracks(self, obs):
        barracks_location = []
        barracks = HelperClass.get_units(self, obs,units.Terran.Barracks)
        for barrack_unit in barracks:
            barracks_location.append(barrack_unit)
        return barracks_location





