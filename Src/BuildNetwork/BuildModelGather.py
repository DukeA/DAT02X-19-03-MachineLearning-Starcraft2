import random
import numpy as np
import statistics

from pysc2.lib import actions, units, features
from collections import defaultdict



from Models.HelperClass.HelperClass import HelperClass
from Models.BotFile.State import State
from BuildNetwork.BuildingTerranQueue import BuildingTerranQueue
from BuildNetwork.BuildingNeutral import BuildingsNeutral

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
        self.buildings =[
            BuildingTerranQueue.commandcenter,
            BuildingTerranQueue.supply_depot,
            BuildingTerranQueue.barracks,
            BuildingTerranQueue.barracks_techlab,
            BuildingTerranQueue.factory,
            BuildingTerranQueue.refinary,
            BuildingTerranQueue.starPort
        ]
        self.neutralLocation = [
                BuildingsNeutral.Vaspane_Gas,
            BuildingsNeutral.Rich_Vaspane_Gas,
            BuildingsNeutral.Minerals,
            BuildingsNeutral.Minerals_750Field,
            BuildingsNeutral.Minerals_BattlestationField,
            BuildingsNeutral.Minerals_750BattlestationField,
            BuildingsNeutral.Minerals_LabMineral,
            BuildingsNeutral.Minerals_750LabMineral,
            BuildingsNeutral.Minerals_PurifiedField,
            BuildingsNeutral.Minerals_750PurifiedField,
            BuildingsNeutral.Minerals_RichField,
            BuildingsNeutral.Minerals_750RichField,
            BuildingsNeutral.Ramp_Left,
            BuildingsNeutral.Ramp_Right
        ]


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

    def set_locations(self, obs):
        viewlist = self.set_buildmap()
        build_units = []
        for i in range(self.buildlocation):
            build_units.append(self.get_unit_location(obs, i))
        for j in range(self.neutralLocation):
            build_units.append(self.get_unit_location(obs, j))

        for unit in build_units:
            viewlist

        return viewlist




    def get_unit_location(self, obs,buildType):
        unit_location = [unit for unit in obs.observation.feature_units
             if unit.unit_type == buildType]
        return unit_location

    def set_buildmap(self):
        viewlist = np.full((81, 81), 0)
        return viewlist



