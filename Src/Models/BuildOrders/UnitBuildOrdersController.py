

from pysc2.agents import base_agent


from Models.BuildOrders.UnitBuildOrders import UnitBuildOrders

"""
A Controller class which changes the state
of the action to build certain  troops
"""


class UnitBuildOrdersController(base_agent.BaseAgent):
    def __init__(self):
        super.UnitBuildOrdersController().__init__()

    def train_marines(self, obs, free_supply):
        UnitBuildOrders.build_marines(self, obs, free_supply)

    def train_marauder(self, obs, free_supply):
        UnitBuildOrders.build_marauder(self, obs, free_supply)

    def train_reaper(self, obs, free_supply):
        UnitBuildOrders.build_reaper(self, obs, free_supply)

    def train_hellion(self, obs, free_supply):
        UnitBuildOrders.build_hellion(self, obs, free_supply)

    def train_medivac(self, obs, free_supply):
        UnitBuildOrders.build_medivac(self, obs, free_supply)

    def train_viking(self, obs, free_supply):
        UnitBuildOrders.build_viking(self, obs, free_supply)

    def transform_viking_to_ground(self, obs):
        UnitBuildOrders.transform_viking_to_ground(self, obs)

    def transform_viking_to_air(self, obs):
        UnitBuildOrders.transform_viking_to_air(self, obs)
