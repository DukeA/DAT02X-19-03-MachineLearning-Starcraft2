

from pysc2.agents import base_agent


from Models.BuildOrders.BuildOrders import BuildOrders
"""
 @Author Adam Grandén
 @Class Description: 
 The code  is a controller for the method  Build Methods which sends a
 call to the  BuildOrder method and execute 
 the following methods to make it run
"""


class BuildOrderController(base_agent.BaseAgent):
    def __init__(self):
        super(BuildOrderController).__init__()
        self.BuildOrders()

    def build_supplaydepot(self, obs, free_supply):
        BuildOrders.build_supply_depot(self, obs, free_supply)

    def build_refinary(self, obs):
        BuildOrders.build_refinery(self, obs)

    def build_barracks(self, obs):
        BuildOrders.build_barracks(self, obs)

    def build_scv(self, obs, free_supply):
        BuildOrders.build_scv(self, obs, free_supply)

    def return_scv(self, obs):
        BuildOrders.return_scv(self,obs)

    def build_expand(self, obs,top_start):
        BuildOrders.expand(self,obs,top_start)