

from enum import Enum
from pysc2.lib import units


class BuildingTerran(Enum):
    Minerals = units.Neutral.MineralField
    Minerals_750Field = units.Neutral.MineralField750
    Minerals_BattlestationField = units.Neutral.BattleStationMineralField
    Minerals_