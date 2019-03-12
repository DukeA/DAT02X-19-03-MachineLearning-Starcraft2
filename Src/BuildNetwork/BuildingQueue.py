
from enum import  Enum
from pysc2.lib import units


class BuildingQueue(Enum):
    commandcenter = units.Terran.CommandCenter,
    barracks = units.Terran.Barracks,
    barracks_techlab = units.Terran.BarracksTechLab,
    factory = units.Terran.Factory,
    refinary = units.Terran.Refinery,
    starPort = units.Terran.Starport,
    supply_depot = units.Terran.SupplyDepot




