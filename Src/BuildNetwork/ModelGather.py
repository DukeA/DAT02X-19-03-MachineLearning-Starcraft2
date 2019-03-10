
import numpy as np

from pysc2.lib import actions, units,features
from _collections import defaultdict




from Models.HelperClass.HelperClass import HelperClass
from Models.BotFile.State import State
from BuildNetwork.BuildingQueue import BuildingQueue

"""
    The class is a wrapper class for the State of the buildinglocation
    
"""
class BuildModelGather:

    def __init__(self, State):
        self.State = State()
        self.reward = State.reward
        self.units_in_progress =State.units_in_progress
        self.buildlocation = []
        self.buildings =[BuildingQueue.commandcenter,
                         BuildingQueue.supply_depot,
                         BuildingQueue.barracks,
                         BuildingQueue.barracks_techlab,
                         BuildingQueue.factory,
                         BuildingQueue.refinary,
                         BuildingQueue.starPort]


    def __getattr__(self, item):
        orig_attr= self.State.__getattribute__(item)
        if callable(orig_attr):
            def wrapped(*args ,**kwargs):
                result = orig_attr(*args ,**kwargs)
                if result == self.State:
                    return self
                return  result
            return wrapped
        else:
            return orig_attr





    def set_observable_location(self,obs):

        



        obs.observation.feature_minmap.player_relative[
            int(round())
        ]



    def check_obeervable_buildinglocation(self, obs):
        building_state = self.

        build_location =[]

