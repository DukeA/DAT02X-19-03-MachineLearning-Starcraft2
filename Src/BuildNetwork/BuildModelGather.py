import random
import numpy as np
import statistics

from pysc2.lib import actions, units, features
from collections import defaultdict



from Models.HelperClass.HelperClass import HelperClass
from Models.BotFile.State import State
from BuildNetwork.BuildingQueue import BuildingQueue

"""
    The class is a wrapper class for the 
    State of the building location which checks all the 
    
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
            def wrapped(*args, **kwargs):
                result = orig_attr(*args, **kwargs)
                if result == self.State:
                    return self
                return  result
            return wrapped
        else:
            return orig_attr


    def set_observable_location(self,obs):
        for buildings_type in self.buildings:

            buildings_type = HelperClass.get_units(self, obs, buildings_type)

            if len(buildings_type) != 0:
                for building in buildings_type:
                    building_coordinate = building[0]
                    coordinates_on_screen = obs.observation.feature_minmap.player_relative[
                        int(round(building_coordinate[1]))][int(round(building_coordinate[0]))]
                    if coordinates_on_screen == 1:
                        self.buildlocation.append(building)
        return self.buildlocation

    def set_locations(self,obs):
        n = obs.observation.feature_minmap
        viewlist = [[0]*n for i in range(n)]
        for i in range(n):
            for j in range(n):
                if i > 0 and j < 0 :
                    viewlist.append(0)
                elif i > 50 and j < 50:
                    viewlist.append(1)
        for row in viewlist:
          matrix = [str(elem) for elem in row]
        return matrix



    def set_buildmap(self):
        viewlist = [[0]*81 for i in range(81)]
        return viewlist




    def
