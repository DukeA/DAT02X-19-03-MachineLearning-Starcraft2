from pysc2.agents import base_agent
from pysc2.lib import actions, units

class marineAttack(base_agent.BaseAgent):

    def step(self, obs):
        super(marineAttack, self).step(obs)

        print('Own marines: '+str(len(self.get_own_units(obs, units.Terran.Marine))))
        print('Enemy marines: '+str(len(self.get_enemy_units(obs, units.Terran.Marine))))

        # TODO: Attacking...

        return actions.FUNCTIONS.no_op()


    def get_own_units(self, obs, unit_type):
        return [unit for unit in obs.observation.feature_units
                if (unit.unit_type == unit_type) & (unit[1] == 1)]


    def get_enemy_units(self, obs, unit_type):
        return [unit for unit in obs.observation.feature_units
                if (unit.unit_type == unit_type) & (unit[1] == 4)]
