from pysc2.agents import base_agent
from pysc2.lib import actions, units

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
        return obs.observation.player.minerals >= 75

    def build_command_center_possible(self, obs):
        return obs.observation.player.minerals >= 500

