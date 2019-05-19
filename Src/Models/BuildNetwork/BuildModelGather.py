import numpy as np

from Models.BuildNetwork.BuildingTerranQueue import BuildingTerranQueue
from Models.BuildNetwork.BuildingNeutral import BuildingsNeutral

"""
    The class is a wrapper class for the 
    State of the building location which checks the environment and 
    places them in a grid structure.
    
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

    """
        :param The parameter of the observable universe
        The method takes the  environment and sets  the value of the environment in that place.
        With the  new value which was supposed to be the value of the  building.
        
    """

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
                     values = unit[0]
                     for i in range(values[0], values[2]):
                         if (i < 82 and i > 0):
                            for j in range(values[1], values[3]):
                                if (j < 82 and j > 0):
                                    value_x = i
                                    value_y = j
                                    if isinstance(values[4], tuple):
                                        value_type = values[4][0]
                                    else:
                                        value_type = values[4]
                                    viewlist[value_x, value_y] = value_type
        return viewlist

    """
        :param obs - The seen environment form the model the 
        :param building_type - The  set type of the terran buildings 
        in the game from the Enum class
        The class gets the radius for each of the coordinates for each of the building
    """

    def get_units_infrastructre_location(self, obs, building_type):
        value = building_type
        units = [unit for unit in obs.observation.feature_units
                 if unit.unit_type == building_type]
        if not units:
            return
        coordinates = []
        for unit in units:
            unit_shape = unit.radius * 2
            coordinates.append(
                BuildModelGather.set_setsourdingvalues(self, unit.x, unit.y, unit_shape, building_type)
            )
        return coordinates

    """
         :param obs - The seen environment for the 
         :param neutral_type - The set of the neutral buildings which are part of the enum class
         The class returns the location of the coordinates for the neutral objects
     """

    def get_neutral_object_location(self, obs, neutral_type):
        neutral_units = [unit for unit in obs.observation.feature_units
                         if unit.unit_type == neutral_type]
        if not neutral_units:
            return
        neutral_coordinates = []
        for unit in neutral_units:
            unit_shape = unit.radius * 2
            neutral_coordinates.append(
                BuildModelGather.set_setsourdingvalues(self, unit.x, unit.y, unit_shape, neutral_type))
        return neutral_coordinates

    """
        :param unit_x - The x location for the type
        :param unit_y - The y location for the type
        :param unit_shape - The shape of the unit
        :param type - The value of the unit type
        The method sets the surrounding variables to be the same as the type of building and sets it to that place
    """

    def set_setsourdingvalues(self, unit_x, unit_y, unit_shape, type):
        radius = unit_shape
        x = unit_x - radius
        y = unit_y - radius
        diameter = radius
        coordinates_radius = []
        coordinates_radius.append((x, y,unit_x, unit_y, type))
        return coordinates_radius

    """
        An method which builds up an array which has the size of 82  arrays with the size 82
    """

    def set_buildmap(self):
        viewlist = np.full((82, 82), 0)
        return viewlist
