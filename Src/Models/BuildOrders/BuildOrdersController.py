

from pysc2.agents import base_agent


from Models.BuildOrders.BuildOrders import BuildOrders
from Models.HelperClass.HelperClass import HelperClass
"""
 @Author Adam Grandén
 @Class Description:
 The code  is a controller for the method  Build Methods which sends a
 call to the  BuildOrder method and execute
 the following methods to make it run
"""


class BuildOrdersController(base_agent.BaseAgent):
    def __init__(self):
        super(BuildOrdersController).__init__()
        self.BuildOrders()

    def build_supply_depot(self, obs):
        BuildOrders.build_supply_depot(self, obs)

    def build_refinery(self, obs):
        BuildOrders.build_refinery(self, obs)

    def build_barracks(self, obs):
        BuildOrders.build_barracks(self, obs)

    def return_scv(self, obs):
        BuildOrders.return_scv(self, obs)

    def build_expand(self, obs, top_start):
        BuildOrders.expand(self, obs, top_start)

    def build_starport(self, obs):
        BuildOrders.build_starport(self, obs)

    def build_factory(self, obs):
        BuildOrders.build_factory(self, obs)

    def upgrade_barracks(self, obs):
        BuildOrders.upgrade_barracks(self, obs)
