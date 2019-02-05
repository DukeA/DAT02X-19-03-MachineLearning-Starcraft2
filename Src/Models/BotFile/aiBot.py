import random
from pysc2.agents import base_agent
from pysc2.lib import actions, units


class aiBot(base_agent.BaseAgent):
    drone_selected = False
    pylon_built = False
    gateway_built = False
    base_Right_location = None;

    def step(self, obs):
        super(aiBot, self).step(obs)

        gateway = self.get_units_by_type(obs, units.Protoss.Gateway)
        if len(gateway) == 0:
            if self.select_unit_of_type(obs, units.Protoss.Probe):
                if self.can_do(obs, actions.FUNCTIONS.Build_Gateway_screen.id):
                    x = random.randint(0, 83)
                    y = random.randint(0, 83)

                    return actions.FUNCTIONS.Build_Gateway_screen("now", (10, 20))

        pylon = self.get_units_by_type(obs, units.Protoss.Pylon)
        if len(pylon) >= 0:
            if self.select_unit_of_type(obs, units.Protoss.Probe):
                if (actions.FUNCTIONS.Build_Pylon_screen.id in
                        obs.observation.available_actions):
                    x = random.randint(0, 83)
                    y = random.randint(0, 83)

                    return actions.FUNCTIONS.Build_Pylon_screen("now", (x, y))


        if actions.FUNCTIONS.Train_Probe_quick.id in obs.observation.available_actions:
            return actions.FUNCTIONS.Train_Probe_quick("now")



        nexuses = self.get_units_by_type(obs,units.Protoss.Nexus)
        if len(nexuses) > 0:
            nexus = random.choice(nexuses)
            return actions.FUNCTIONS.select_point("select_all_type", (nexus.x, nexus.y))
        return actions.FUNCTIONS.no_op()

    def get_units_by_type( self,obs, unit_type):
        return [unit for unit in obs.observation.feature_units
                if unit.unit_type == unit_type]

    def select_unit_of_type( self, obs,unit_type):
        if (len(obs.observation.single_select) > 0 and
                obs.observation.single_select[0].unit_type == unit_type):
            return True

        if (len(obs.observation.multi_select) > 0 and
                obs.observation.multi_select[0].unit_type == unit_type):
            return True

        return False

    def build_pylon(self, obs):
        if self.select_unit_of_type(obs, units.Protoss.Probe):
            if (actions.FUNCTIONS.Build_Pylon_screen.id in
                    obs.observation.available_actions):
                x = random.randint(0, 83)
                y = random.randint(0, 83)

                return actions.FUNCTIONS.Build_Pylon_screen("now", (x, y))


    def build_gateway(self, obs):
        if self.select_unit_of_type(obs, units.Protoss.Probe):
            if (actions.FUNCTIONS.Build_Gateway_screen.id in
                    obs.observation.available_actions):
                x = random.randint(0, 83)
                y = random.randint(0, 83)

                return actions.FUNCTIONS.Build_Gateway_screen("now", (x, y))
