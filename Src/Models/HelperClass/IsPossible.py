from pysc2.agents import base_agent
from pysc2.lib import actions, units

from Models.HelperClass.HelperClass import HelperClass

class IsPossible(base_agent.BaseAgent):

    def build_marines_possible(self, obs):
        return obs.observation.player.minerals >= 50 and (obs.observation.player.food_cap -
                       obs.observation.player.food_used) >= 1

    def build_scv_possible(self, obs):
        return obs.observation.player.minerals >= 50 and (obs.observation.player.food_cap -
                       obs.observation.player.food_used) >= 1

    def build_supply_depot_possible(self, obs):
        return obs.observation.player.minerals >= 100

    def build_barracks_possible(self, obs):
        return obs.observation.player.minerals >= 150

    def build_refinery_possible(self, obs):
        return obs.observation.player.minerals >= 75

    def build_command_center_possible(self, obs):
        return obs.observation.player.minerals >= 400

    def build_factory_possible(self, obs):
        return obs.observation.player.minerals >= 150 and obs.observation.player.vespene >= 100

    def build_starport_possible(self, obs):
        return obs.observation.player.minerals >= 150 and obs.observation.player.vespene >= 100

    def upgrade_barracks_possible(self, obs):
        return obs.observation.player.minerals >= 50 and obs.observation.player.vespene >= 25

    def build_marauder_possible(self, obs):
        return obs.observation.player.minerals >= 100\
               and obs.observation.player.vespene >= 25\
               and (obs.observation.player.food_cap -
                    obs.observation.player.food_used) >= 2

    def build_reaper_possible(self, obs):
        return obs.observation.player.minerals >= 50\
               and obs.observation.player.vespene >= 50\
               and (obs.observation.player.food_cap -
                    obs.observation.player.food_used) >= 1

    def build_hellion_possible(self, obs):
        return obs.observation.player.minerals >= 100\
               and obs.observation.player.vespene >= 0\
               and (obs.observation.player.food_cap -
                    obs.observation.player.food_used) >= 2

    def build_viking_possible(self, obs):
        return obs.observation.player.minerals >= 150\
               and obs.observation.player.vespene >= 75\
               and (obs.observation.player.food_cap -
                    obs.observation.player.food_used) >= 2

    def build_medivac_possible(self, obs):
        return obs.observation.player.minerals >= 100\
               and obs.observation.player.vespene >= 100\
               and (obs.observation.player.food_cap -
                    obs.observation.player.food_used) >= 2

    def build_techlab_possible(self, obs):
        return False
