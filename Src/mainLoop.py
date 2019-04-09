from pysc2.env import sc2_env
from pysc2.lib import features
from Models.BotFile.aiBot import AiBot


def main(unused_argv):
    agent = AiBot()
    save_game = True
    episode = 0
    path1 = "C:/Users/Claes/Desktop/DAT02X-19-03-MachineLearning-Starcraft2/Src/Data/no_op/"
    path2 = "C:/Users/Claes/Desktop/DAT02X-19-03-MachineLearning-Starcraft2/Src/Data/build_scv/"
    path3 = "C:/Users/Claes/Desktop/DAT02X-19-03-MachineLearning-Starcraft2/Src/Data/build_supply_depot/"
    path4 = "C:/Users/Claes/Desktop/DAT02X-19-03-MachineLearning-Starcraft2/Src/Data/build_marine/"
    path5 = "C:/Users/Claes/Desktop/DAT02X-19-03-MachineLearning-Starcraft2/Src/Data/build_marauder/"
    path6 = "C:/Users/Claes/Desktop/DAT02X-19-03-MachineLearning-Starcraft2/Src/Data/build_reaper/"
    path7 = "C:/Users/Claes/Desktop/DAT02X-19-03-MachineLearning-Starcraft2/Src/Data/build_hellion/"
    path8 = "C:/Users/Claes/Desktop/DAT02X-19-03-MachineLearning-Starcraft2/Src/Data/build_medivac/"
    path9 = "C:/Users/Claes/Desktop/DAT02X-19-03-MachineLearning-Starcraft2/Src/Data/build_viking/"
    path10 = "C:/Users/Claes/Desktop/DAT02X-19-03-MachineLearning-Starcraft2/Src/Data/build_barracks/"
    path11 = "C:/Users/Claes/Desktop/DAT02X-19-03-MachineLearning-Starcraft2/Src/Data/build_refinery/"
    path12 = "C:/Users/Claes/Desktop/DAT02X-19-03-MachineLearning-Starcraft2/Src/Data/retreat/"
    path13 = "C:/Users/Claes/Desktop/DAT02X-19-03-MachineLearning-Starcraft2/Src/Data/return_scv/"
    path14 = "C:/Users/Claes/Desktop/DAT02X-19-03-MachineLearning-Starcraft2/Src/Data/expand/"
    path15 = "C:/Users/Claes/Desktop/DAT02X-19-03-MachineLearning-Starcraft2/Src/Data/build_factory/"
    path16 = "C:/Users/Claes/Desktop/DAT02X-19-03-MachineLearning-Starcraft2/Src/Data/build_starport/"
    path17 = "C:/Users/Claes/Desktop/DAT02X-19-03-MachineLearning-Starcraft2/Src/Data/build_tech_lab_barracks/"
    path18 = "C:/Users/Claes/Desktop/DAT02X-19-03-MachineLearning-Starcraft2/Src/Data/attack/"

    try:
        with sc2_env.SC2Env(
                map_name="AbyssalReef",
                players=[sc2_env.Agent(sc2_env.Race.terran),
                         sc2_env.Bot(sc2_env.Race.terran,
                                         sc2_env.Difficulty.easy)],
                agent_interface_format=features.AgentInterfaceFormat(
                    feature_dimensions=features.Dimensions(screen=84, minimap=64),
                    use_feature_units=True,
                    use_raw_units=True,
                    use_camera_position=True),
                step_mul=5,  # about 200 APM
                game_steps_per_episode=1346*30,  # Ends after 13 minutes (real-time)16 * 60 * 0 * 1.4
                # save_replay_episodes=1, #How often do you save replays
                # replay_dir="C:/Users/Claes/Desktop/StarCraft2Replays", # Need to change to your own path
                visualize=True,
                disable_fog=True) as env:
            while True:
                agent.setup(env.observation_spec(), env.action_spec())

                timesteps = env.reset()
                agent.reset()
                episode += 1

                while True:
                    step_actions = [agent.step(timesteps[0])]
                    if timesteps[0].last():
                        if save_game and agent.reward == 1:
                            agent.save_game(path1, path2, path3, path4,
                            path5, path6, path7, path8, path9, path10, 
                            path11, path12, path13, path14, path15, 
                            path16, path17, path18, episode)
                        break
                    timesteps = env.step(step_actions)

    except KeyboardInterrupt:
        pass
