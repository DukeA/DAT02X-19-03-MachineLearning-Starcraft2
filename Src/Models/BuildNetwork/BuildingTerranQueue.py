
from enum import  Enum
from pysc2.lib import units

"""
The class is an  collection of all the  
enum values  from the pysc2 library
"""

class BuildingTerranQueue(Enum):
    commandcenter = units.Terran.CommandCenter.value,
    barracks = units.Terran.Barracks.value,
    barracks_techlab = units.Terran.BarracksTechLab.value,
    factory = units.Terran.Factory.value,
    refinary = units.Terran.Refinery.value,
    starPort = units.Terran.Starport.value,
    supply_depot = units.Terran.SupplyDepot.value




