
from enum import  Enum
from pysc2.lib import units

"""
The class is an  collection of all the  units which the  ai is able to build
"""


class BuildingTerranQueue(Enum):
    commandcenter = units.Terran.CommandCenter,
    barracks = units.Terran.Barracks,
    barracks_techlab = units.Terran.BarracksTechLab,
    factory = units.Terran.Factory,
    refinary = units.Terran.Refinery,
    starPort = units.Terran.Starport,
    supply_depot = units.Terran.SupplyDepot




