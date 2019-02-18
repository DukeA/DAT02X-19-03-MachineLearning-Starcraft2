from pysc2.env import sc2_env
from pysc2.lib import features
from Models.MarineAttack.marineAttack import marineAttack
from Models.MarineAttack.marineAttack import marineAttackGenerator
from absl import app
import numpy as np


def main(unused_argv):
    marine_difference = []
    prediction = []
    result = []
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
                step_mul=1,
                game_steps_per_episode=0,
                visualize=True) as env:
            while episode < max_episodes:
                episode += 1
                print("Episode "+str(episode)+"/"+str(max_episodes))
                agent = marineAttackGenerator()
                agent.setup(env.observation_spec(), env.action_spec())

                timesteps = env.reset()
                agent.reset()

                while True:
                    step_actions = [agent.step(timesteps[0])]
                    if timesteps[0].last():
                        prediction.append(agent.predicted_outcome)
                        print(len(agent.own_marines) - len(agent.enemy_marines))
                        print(timesteps[0][1])
                        marine_difference.append(len(agent.own_marines) - len(agent.enemy_marines))
                        result.append(timesteps[0][1])
                        break
                    timesteps = env.step(step_actions)
            print(marine_difference)
            print(prediction)
            print(result)
            game_data = np.array((marine_difference, prediction, result))
            print(game_data)
            np.save('RandomData', game_data)

    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    app.run(main)
