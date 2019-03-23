

from enum import Enum
from pysc2.lib import units

"""
The class is an enum class for all the neutral buildings in the enviorment
"""
class BuildingsNeutral(Enum):
    Minerals = units.Neutral.MineralField.value
    Minerals_750Field = units.Neutral.MineralField750.value
    Minerals_BattlestationField = units.Neutral.BattleStationMineralField.value
    Minerals_750BattlestationField = units.Neutral.BattleStationMineralField750.value
    Minerals_LabMineral = units.Neutral.LabMineralField.value
    Minerals_750LabMineral = units.Neutral.LabMineralField750.value
    Minerals_PurifiedField = units.Neutral.PurifierMineralField.value
    Minerals_750PurifiedField = units.Neutral.PurifierMineralField750.value
    Minerals_RichField = units.Neutral.RichMineralField.value
    Minerals_750RichField = units.Neutral.RichMineralField750.value
    Vaspane_Gas = units.Neutral.VespeneGeyser.value
    Rich_Vaspane_Gas = units.Neutral.RichVespeneGeyser.value
    Ramp_Left = units.Neutral.DebrisRampLeft.value
    Ramp_Right = units.Neutral.DebrisRampRight.value
