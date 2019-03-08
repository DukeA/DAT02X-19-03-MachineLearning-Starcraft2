from pysc2.env import sc2_env
from pysc2.lib import features, units
from Models.BotFile.aiBot import AiBot
from absl import app
import pickle


def main(unused_argv):
    agent = AiBot()
    episode = 0
    try:
        with sc2_env.SC2Env(
                map_name="AbyssalReef",
                players=[sc2_env.Agent(sc2_env.Race.terran),
                         sc2_env.Bot(sc2_env.Race.terran,
                                         sc2_env.Difficulty.very_easy)],
                agent_interface_format=features.AgentInterfaceFormat(
                    feature_dimensions=features.Dimensions(screen=84, minimap=64),
                    use_feature_units=True),
                step_mul=5,  #about 200 APM
                game_steps_per_episode=16 * 60 * 0 * 1.4,  # Ends after 13 minutes (real-time)
                #save_replay_episodes=1, #How often do you save replays
                #replay_dir="C:/Users/Claes/Desktop/StarCraft2Replays", # Need to change to your own path
                visualize=True,
                disable_fog=True) as env:
            while True:
                agent.setup(env.observation_spec(), env.action_spec())

                timesteps = env.reset()
                agent.reset()
                episode += 1

                while True:
                    step_actions = [agent.step(timesteps[0])]
                    print(agent.game_state.units_amount[units.Terran.SCV.value])
                    if agent.game_state.units_amount[units.Terran.SCV.value] == 17:
                        print("17 SCVs at agent step "+str(agent.steps))
                        with open("test"+str(episode)+".data", 'wb') as filehandle:
                            pickle.dump(agent.game_state.get_state(), filehandle)
                        with open("test"+str(episode)+".data", 'rb') as filehandle:
                            testing = pickle.load(filehandle)
                            print(testing)
                        break
                    if timesteps[0].last():
                        break
                    timesteps = env.step(step_actions)

    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    app.run(main)
