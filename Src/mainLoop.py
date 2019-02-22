from pysc2.env import sc2_env
from pysc2.lib import features
from Models.BotFile.aiBot import aiBot


def main(unused_argv):
    agent = aiBot()
    try:
        while True:
            with sc2_env.SC2Env(
                    map_name="AbyssalReef",
                    players=[sc2_env.Agent(sc2_env.Race.terran),
                             sc2_env.Bot(sc2_env.Race.terran,
                                         sc2_env.Difficulty.very_easy)],
                    agent_interface_format=features.AgentInterfaceFormat(
                        feature_dimensions=features.Dimensions(screen=84, minimap=64),
                        use_feature_units=True),
                    step_mul=5,  #about 200 APM
                    game_steps_per_episode=80000, # about 1 h before game ends
                    #save_replay_episodes=1, #How often do you save replays
                    #replay_dir="C:/Users/Claes/Desktop/StarCraft2Replays", # Need to change to your own path, notice forward slashes instead of backslashes!
                    #You can visualize replay with command "python -m pysc2.bin.play --replay "C:/Users/Claes/Desktop/StarCraft2Replays/AbyssalReef_2019-02-22-09-42-52.SC2Replay"" (but with your own path)
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
