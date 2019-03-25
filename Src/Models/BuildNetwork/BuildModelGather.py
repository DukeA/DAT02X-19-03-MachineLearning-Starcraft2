import numpy as np

from Models.HelperClass.HelperClass import HelperClass
from Models.BuildNetwork.BuildingTerranQueue import BuildingTerranQueue
from Models.BuildNetwork.BuildingNeutral import BuildingsNeutral
from Models.HelperClass.HelperClass import HelperClass

"""
    The class is a wrapper class for the 
    State of the building location which checks all the 
    
"""


class BuildModelGather:
    buildings = [
        BuildingTerranQueue.commandcenter.value,
        BuildingTerranQueue.supply_depot.value,
        BuildingTerranQueue.barracks.value,
        BuildingTerranQueue.barracks_techlab.value,
        BuildingTerranQueue.factory.value,
        BuildingTerranQueue.refinary.value,
        BuildingTerranQueue.starPort.value
    ]

    neutral_location = [
        BuildingsNeutral.Vaspane_Gas.value,
        BuildingsNeutral.Rich_Vaspane_Gas.value,
        BuildingsNeutral.Minerals.value,
        BuildingsNeutral.Minerals_750Field.value,
        BuildingsNeutral.Minerals_BattlestationField.value,
        BuildingsNeutral.Minerals_750BattlestationField.value,
        BuildingsNeutral.Minerals_LabMineral.value,
        BuildingsNeutral.Minerals_750LabMineral.value,
        BuildingsNeutral.Minerals_PurifiedField.value,
        BuildingsNeutral.Minerals_750PurifiedField.value,
        BuildingsNeutral.Minerals_RichField.value,
        BuildingsNeutral.Minerals_750RichField.value,
        BuildingsNeutral.Ramp_Left.value,
        BuildingsNeutral.Ramp_Right.value
    ]

    def __init__(self, state):
        self.state = state()
        self.reward = state.reward
        self.units_in_progress = state.units_in_progress


    def __getattr__(self, item):
        orig_attr = self.State.__getattribute__(item)
        if callable(orig_attr):
            def wrapped(*args, **kwargs):
                result = orig_attr(*args, **kwargs)
                if result == self.State:
                    return self
                return result

            return wrapped
        else:
            return orig_attr

    def set_observable_location(self, obs):
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
        viewlist = BuildModelGather.set_buildmap(self)
        build_units_list = []
        for i in BuildModelGather.buildings:
            build_units_list.append(BuildModelGather.get_units_infrastructre_location(self, obs, i))
        for j in BuildModelGather.neutral_location:
            build_units_list.append(BuildModelGather.get_neutral_object_location(self, obs, j))
        for build_units in build_units_list:
            if (build_units != None):
                for unit in build_units:
                    for value in unit:
                        value_x = value[0]
                        value_y = value[1]
                        if isinstance(value[2], tuple):
                            value_type = value[2][0]
                        else:
                            value_type = value[2]
                        viewlist[value_x, value_y] = value_type
        return viewlist

    def get_units_infrastructre_location(self, obs, building_type):
        units = [unit for unit in obs.observation.feature_units
                 if unit.unit_type == building_type]
        if not units:
            return
        coordinates = []
        for unit in units:
            unit_shape = unit.radius * 2
            coordinates.append(
                BuildModelGather.set_setsourdingvalues(self, unit.x , unit.y, unit_shape, building_type)
            )
        return coordinates

    def get_neutral_object_location(self, obs, neutral_type):
        neutral_units = [unit for unit in obs.observation.feature_units
                 if unit.unit_type == neutral_type]
        if not neutral_units:
            return
        neutral_coordinates = []
        for unit in neutral_units:
            unit_shape = unit.radius*2
            for i in range(unit.radius):
                neutral_coordinates.append(
                    BuildModelGather.set_setsourdingvalues(self, unit.x , unit.y, unit_shape, neutral_type)
                )
        return neutral_coordinates

    def set_setsourdingvalues(self, unit_x, unit_y, unit_shape, type):
        radius = unit_shape
        x = unit_x-radius
        y = unit_y-radius
        diameter = radius
        coordinates_radius = []
        for i in range(diameter):
            for j in range(diameter):
                coordinates_radius.append((x+i, y+j, type))
        return coordinates_radius

    def set_buildmap(self):
        viewlist = np.full((82, 82), 0)
        return viewlist
