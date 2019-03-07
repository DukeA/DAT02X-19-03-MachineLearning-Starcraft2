from pysc2.agents import base_agent
from pysc2.lib import actions, units

from Models.HelperClass.HelperClass import HelperClass

class IsPossible(base_agent.BaseAgent):

    def build_marines_possible(self, obs):
        return obs.observation.player.minerals >= 50 and (obs.observation.player.food_cap -
                       obs.observation.player.food_used) > 0

    def build_scv_possible(self, obs):
        return obs.observation.player.minerals >= 50 and (obs.observation.player.food_cap -
                       obs.observation.player.food_used) > 0

    def build_supply_depot_possible(self, obs):
        return obs.observation.player.minerals >= 100

    def build_barracks_possible(self, obs):
        return obs.observation.player.minerals >= 150

    def build_refinery_possible(self, obs):
        refineries = HelperClass.get_units(self, obs, units.Terran.Refinery)
        return obs.observation.player.minerals >= 75 and len(refineries) < 2

    def build_command_center_possible(self, obs):
        return obs.observation.player.minerals >= 500

    def build_factory_possible(self, obs):
        return False

    def build_starport_possible(self, obs):
        return False

    def upgrade_barracks_possible(self, obs):
        return False

    def build_marauder_possible(self, obs):
        return False

    def build_medivac_possible(self, obs):
        return False

    def build_techlab_possible(self, obs):
        return False
