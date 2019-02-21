

from pysc2.agents import base_agent


from Models.BuildOrders.UnitBuildOrders import UnitBuildOrders


class UnitBuildOrdersController(base_agent.BaseAgent):
    def __init__(self):
        super.UnitBuildOrdersController().__init__()

    def train_marines(self, obs,free_supply):
        UnitBuildOrders.build_marines(self, obs, free_supply)
