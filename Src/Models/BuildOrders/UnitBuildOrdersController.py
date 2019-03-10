

from pysc2.agents import base_agent


from Models.BuildOrders.UnitBuildOrders import UnitBuildOrders

"""
A Controller class which changes the state
of the action to build certain  troops
"""


class UnitBuildOrdersController(base_agent.BaseAgent):
    def __init__(self):
        super.UnitBuildOrdersController().__init__()

    def train_marines(self, obs):
        UnitBuildOrders.build_marines(self, obs)

    def train_marauder(self, obs):
        UnitBuildOrders.build_marauder(self, obs)

    def train_reaper(self, obs,):
        UnitBuildOrders.build_reaper(self, obs)

    def train_hellion(self, obs):
        UnitBuildOrders.build_hellion(self, obs)

    def train_medivac(self, obs):
        UnitBuildOrders.build_medivac(self, obs)

    def build_scv(self, obs):
        UnitBuildOrders.build_scv(self, obs)

    def train_viking(self, obs):
        UnitBuildOrders.build_viking(self, obs)
