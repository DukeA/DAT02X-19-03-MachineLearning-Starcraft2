from pysc2.agents import base_agent

from Models.BuildOrders.BuildOrders import BuildOrders

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

    def build_supply_depot(self, obs, build_location):
        BuildOrders.build_supply_depot(self, obs, build_location)

    def build_refinery(self, obs):
        BuildOrders.build_refinery(self, obs)

    def build_barracks(self, obs, build_location):
        BuildOrders.build_barracks(self, obs, build_location)

    def return_scv(self, obs):
        BuildOrders.return_scv(self, obs)

    def build_expand(self, obs):
        BuildOrders.expand(self, obs)

    def build_starport(self, obs):
        BuildOrders.build_starport(self, obs)

    def build_factory(self, obs):
        BuildOrders.build_factory(self, obs)

    def build_tech_lab_barracks(self, obs):
        BuildOrders.build_tech_lab_barracks(self, obs)
