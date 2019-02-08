import random
import numpy
from pysc2.agents import base_agent
from pysc2.env import sc2_env
from pysc2.lib import actions, features, units
from absl import app

FUNCTIONS = actions.FUNCTIONS

class Agent(base_agent.BaseAgent):

    def step(self, obs):
        super(Agent, self).step(obs)
        if (FUNCTIONS.Train_Probe_quick.id in obs.observation.available_actions):
            return FUNCTIONS.Train_Probe_quick("now")
        else:
            nexuses = [unit for unit in obs.observation.feature_units
                if unit.unit_type == units.Protoss.Nexus]

            if len(nexuses) > 0:
                nexus = random.choice(nexuses)
        
                return FUNCTIONS.select_point("select_all_type", (nexus.x, nexus.y))
            else:
                return FUNCTIONS.no_op()

def main(unused_argv):
  agent = Agent()
  try:
    while True:
      with sc2_env.SC2Env(
          map_name="Simple64",
          players=[sc2_env.Agent(sc2_env.Race.protoss),
                   sc2_env.Bot(sc2_env.Race.random,
                               sc2_env.Difficulty.very_easy)],
          agent_interface_format=features.AgentInterfaceFormat(
              feature_dimensions=features.Dimensions(screen=84, minimap=64),
              use_feature_units=True),
          step_mul=16,
          game_steps_per_episode=0,
          visualize=True) as env:
          
        agent.setup(env.observation_spec(), env.action_spec())
        
        timesteps = env.reset()
        agent.reset()
        
        while True:
          step_actions = [agent.step(timesteps[0])]
          if timesteps[0].last():
            break
          timesteps = env.step(step_actions)
      
  except KeyboardInterrupt:
    pass
  
if __name__ == "__main__":
    app.run(main)