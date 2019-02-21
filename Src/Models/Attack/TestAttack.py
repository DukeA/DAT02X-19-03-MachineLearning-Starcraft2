from pysc2.env import sc2_env
from pysc2.agents import base_agent
from pysc2.lib import features, actions
from Models.Attack.Attack import Attack
from absl import app

class TestAttack(base_agent.BaseAgent):
    def __init__(self):
        super(TestAttack, self).__init__()
        self.base_location = None
        self.reqSteps = 0
        self.minimap_size = 64
        self.has_attacked = False
        self.attacking = False

    def step(self, obs):
        super(TestAttack, self).step(obs)
        if obs.first():
            start_y, start_x = (obs.observation.feature_minimap.player_relative
                                == features.PlayerRelative.SELF).nonzero()
            xmean = start_x.mean()
            ymean = start_y.mean()

            self.base_location = (xmean, ymean)

        if self.reqSteps == 0 and self.has_attacked:
            self.attacking = False

        if self.reqSteps == 0 and not self.has_attacked:
            self.attacking = True

        if self.attacking:
            return Attack.attack(self, obs)

        return actions.FUNCTIONS.no_op()


def main(unused_argv):
    max_episodes = 10
    episode = 0
    try:
        with sc2_env.SC2Env(
                map_name="UnitSpawnerMarine",
                players=[sc2_env.Agent(sc2_env.Race.terran),
                         sc2_env.Bot(sc2_env.Race.random,
                                     sc2_env.Difficulty.very_easy)],
                agent_interface_format=features.AgentInterfaceFormat(
                    feature_dimensions=features.Dimensions(screen=84, minimap=64),
                    use_feature_units=True, ),
                step_mul=5,
                game_steps_per_episode=0,
                visualize=True) as env:
            while episode < max_episodes:
                episode += 1
                print("Episode "+str(episode)+"/"+str(max_episodes))
                agent = TestAttack()
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
