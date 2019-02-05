import random
from pysc2.agents import base_agent
from pysc2.lib import actions, units,features
FUNCTIONS = actions.FUNCTIONS


_BUILD_GATEWAY = FUNCTIONS.Build_Gateway_screen.id
_BUILD_PYLON = FUNCTIONS.Build_Pylon_screen.id;
_BUILD_ASSIMILATOR = FUNCTIONS.Build_Assimilator_screen.id

_TRAIN_PROBE = FUNCTIONS.Train_Probe_quick.id;

_U_TYPE = features.ScreenFeatures.unit_type;
_PLAYER_R = features.ScreenFeatures.player_relative;

_BOT_SELF = 1
_BUILD_NOT_QUEUED = [0]
_BUILD_QUEUED = [1]

class aiBot(base_agent.BaseAgent):
    drone_selected = False
    pylon_built = False
    gateway_built = False
    base_Right_location = None;

    def step(self, obs):
        super(aiBot, self).step(obs)


        if aiBot.base_Right_location is None:
            aiBot.check_Start_Location(self,obs)

        if _TRAIN_PROBE in obs.observation.available_actions:
            return FUNCTIONS.Train_Probe_quick("now")
        elif _BUILD_PYLON in obs.observation.available_actions:
            aiBot.build_pylon( self, obs)
        elif _BUILD_GATEWAY in obs.observation.available_actions:
            aiBot.build_gateway( self, obs)
        else:
            nexuses = [unit for unit in obs.observation.feature_units
                       if unit.unit_type == units.Protoss.Nexus]

            if len(nexuses) > 0:
                nexus = random.choice(nexuses)

                return FUNCTIONS.select_point("select_all_type", (nexus.x, nexus.y))
            else:
                return FUNCTIONS.no_op()

    def build_pylon( self,obs):
        unit_type = obs.observation["screen"][_U_TYPE]
        unit_y, unit_x = (unit_type == units.Protoss.Nexus).nonzero

        target = self.BuildLocation(int(unit_x.mean()), 0,int(unit_y.mean()),15)

        self.pylon_built = True

        return actions.FunctionCall(_BUILD_PYLON,[_BUILD_NOT_QUEUED, target])

    def build_gateway(self, obs):
        unit_type = obs.observation["screen"][_U_TYPE]
        unit_y, unit_x = (unit_type == units.Protoss.Nexus).nonzero

        target = self.BuildLocation(int(unit_x.mean()), 0,int(unit_y.mean()),20)
        self.gateway_built = True;

        return actions.FunctionCall(_BUILD_GATEWAY,[_BUILD_NOT_QUEUED, target])

    def check_Start_Location(self,obs):
        player_y, player_x = (obs.observation["minimap"][_PLAYER_R] == _BOT_SELF).nonzero()
        self.base_Right_location= player_y.mean() >=31

    def BuildLocation(self,x,x_distance,y,y_distance):
        if not self.base_Right_location:
            return [x+x_distance,y+y_distance]
        return [x+x_distance,y-y_distance]