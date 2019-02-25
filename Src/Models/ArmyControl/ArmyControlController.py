

from pysc2.agents import base_agent
from Models.ArmyControl.ArmyControl import ArmyControl

"""
 @Author Adam Grandén
 @Class Description: 
 The code  is a controller for the method  Build Methods which sends a
 call to the  BuildOrder method and execute 
 the following methods to make it run
 
 Adapted for ArmyControl
"""


class ArmyControlController(base_agent.BaseAgent):
    def __init__(self):
        super(ArmyControlController).__init__()
        self.ArmyControl()

    def attack(self, obs, location=None):
        ArmyControl.attack(self, obs, location)

    def retreat(self, obs, location=None):
        ArmyControl.retreat(self, obs, location)