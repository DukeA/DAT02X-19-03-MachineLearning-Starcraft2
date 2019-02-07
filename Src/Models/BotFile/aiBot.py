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


        supply_depot = self.get_units_by_type(obs, units.Terran.SupplyDepot)
        if len(supply_depot) >= 0 :
            if self.select_unit_of_type(obs, units.Terran.SCV):
                if self.can_do(obs,actions.FUNCTIONS.Build_SupplyDepot_screen.id):
                    x = random.randint(0, 83)
                    y = random.randint(0, 83)

                    return actions.FUNCTIONS.Build_SupplyDepot_screen("now", (x, y))

        barracks = self.get_units_by_type(obs,units.Terran.Barracks)
        if len(barracks) ==0:
            if self.select_unit_of_type(obs,units.Terran.SCV):
                if self.can_do(obs,actions.FUNCTIONS.Build_Barracks_screen.id):
                    x = random.randint(0,83)
                    y = random.randint(0,83)


                    return  actions.FUNCTIONS.Build_Barracks_screen("now",(x,y))

        refinery = self.get_units_by_type(obs, units.Terran.Refinery)
        if len(refinery) == 0:
            if self.select_unit_of_type(obs, units.Terran.SCV):
                if self.can_do(obs, actions.FUNCTIONS.Build_Refinery_screen.id):
                    x = random.randint(0, 83)
                    y = random.randint(0, 83)

                    return actions.FUNCTIONS.Build_Refinery_screen("now", (x, y))


        if actions.FUNCTIONS.Train_SCV_quick.id in obs.observation.available_actions:
            return actions.FUNCTIONS.Train_SCV_quick("now")



        command_scv = self.get_units_by_type(obs,units.Terran.SCV)
        if len(command_scv) > 0:
            command = random.choice(command_scv)
            return actions.FUNCTIONS.select_point("select_all_type", (command.x, command.y))
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

    def can_do(self, obs, action):
        return action in obs.observation.available_actions

    def build_supplydepot(self):
        return


