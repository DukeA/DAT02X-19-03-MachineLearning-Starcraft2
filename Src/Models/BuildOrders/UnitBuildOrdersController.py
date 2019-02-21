

from pysc2.agents import base_agent


from Models.BuildOrders.UnitBuildOrders import  UnitBuildOrders



class UnitBuildOrdersController(base_agent.BaseAgent):
    def __init__(self):
        super.UnitBuildOrdersController().__init__
        self.UnitBuildOrders(self)

    def train_marines(self, obs):
        UnitBuildOrders.build_Marines(self, obs)
