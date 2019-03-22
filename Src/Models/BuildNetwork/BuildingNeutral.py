

from enum import Enum
from pysc2.lib import units

"""
The class is an enum class for all the neutral buildings in the enviorment
"""
class BuildingsNeutral(Enum):
    Minerals = units.Neutral.MineralField
    Minerals_750Field = units.Neutral.MineralField750
    Minerals_BattlestationField = units.Neutral.BattleStationMineralField
    Minerals_750BattlestationField = units.Neutral.BattleStationMineralField750
    Minerals_LabMineral = units.Neutral.LabMineralField
    Minerals_750LabMineral = units.Neutral.LabMineralField750
    Minerals_PurifiedField = units.Neutral.PurifierMineralField
    Minerals_750PurifiedField = units.Neutral.PurifierMineralField750
    Minerals_RichField = units.Neutral.RichMineralField
    Minerals_750RichField = units.Neutral.RichMineralField750
    Vaspane_Gas = units.Neutral.VespeneGeyser
    Rich_Vaspane_Gas = units.Neutral.RichVespeneGeyser
    Ramp_Left = units.Neutral.DebrisRampLeft
    Ramp_Right = units.Neutral.DebrisRampRight
