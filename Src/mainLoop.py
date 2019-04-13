from pysc2.env import sc2_env
from pysc2.lib import features
from Models.BotFile.aiBot import AiBot
from Models.MachineLearning.ActorCriticAgent import ActorCriticAgent
import matplotlib.pyplot as plt
import pickle
import csv

def main(unused_argv):
    agent = AiBot()
    epsilon = 1
    epsilon_min = 0.1
    eps_reduction_factor = 0.99
    save_game = False
    episode = 0
    path = ""

    # The code automatically runs on LSTM networks if len(state_size) > 1 and saves to LSTM .h5 and .json files.

    # with lstm: (need to change this in State too)
    # state_size = (3, 30)
    # without lstm:
    state_size = 30

    agent.actor_critic_agent = ActorCriticAgent(state_size,
            ["no_op",
            "build_scv",
            "build_supply_depot",
            "build_marine",
            "build_barracks",
            "return_scv",
            "attack"],
             epsilon)
    all_rewards = []

    try:
        with sc2_env.SC2Env(
                map_name="AbyssalReef",
                players=[sc2_env.Agent(sc2_env.Race.terran),
                         sc2_env.Bot(sc2_env.Race.terran,
                                         sc2_env.Difficulty.very_easy)],
                agent_interface_format=features.AgentInterfaceFormat(
                    feature_dimensions=features.Dimensions(screen=84, minimap=64),
                    use_feature_units=True,
                    use_raw_units=True,
                    use_camera_position=True),
                step_mul=8,  # about 200 APM
                game_steps_per_episode=30000,  # Ends after 13 minutes (real-time)16 * 60 * 0 * 1.4
                # save_replay_episodes=1, #How often do you save replays
                # replay_dir="C:/Users/Claes/Desktop/StarCraft2Replays", # Need to change to your own path
                visualize=True,
                disable_fog=True) as env:
            while True:
                agent.setup(env.observation_spec(), env.action_spec())
                timesteps = env.reset()
                agent.reset()
                if episode > 0:
                    all_rewards = all_rewards+[agent.actor_critic_agent.total_reward]
                    with open("Models/MachineLearning/all_rewards.data", 'wb') as filehandle:
                        pickle.dump(all_rewards, filehandle)
                    with open('Models/MachineLearning/all_rewards.txt', mode='w') as filehandle:
                        for i in all_rewards:
                            filehandle.write("%s\n" % i)

                    average_count = 5
                    if episode > 5:
                        average_rewards = []
                        for i in range(len(all_rewards)-average_count):
                            average_i = 0
                            for j in range(average_count):
                                average_i += all_rewards[i+j]
                            average_rewards = average_rewards+[average_i/average_count]

                        with open("Models/MachineLearning/average_rewards.data", 'wb') as filehandle:
                            pickle.dump(average_rewards, filehandle)
                        with open('Models/MachineLearning/average_rewards.txt', mode='w') as filehandle:
                            for i in average_rewards:
                                filehandle.write("%s\n" % i)

                episode += 1
                if agent.actor_critic_agent.epsilon > epsilon_min:
                    agent.actor_critic_agent.epsilon *= eps_reduction_factor
                elif agent.actor_critic_agent.epsilon < epsilon_min:
                    agent.actor_critic_agent.epsilon = epsilon_min
                print(agent.actor_critic_agent.epsilon)
                agent.reward = 0
                agent.actor_critic_agent.total_reward = 0
                while True:
                    step_actions = [agent.step(timesteps[0], epsilon)]

                    if timesteps[0].last():
                        if isinstance(state_size, int):
                            state, oldscore, map = agent.game_state.get_state_now(timesteps[0])
                        else:
                            state, oldscore, map = agent.game_state.get_lstm_state_now(timesteps[0])
                        if agent.reward == 1:
                            # Reward was 30000 before
                            reward = 5000 + (timesteps[0].observation.score_cumulative.score - oldscore)
                            agent.actor_critic_agent.total_reward += reward
                        else:
                            reward = -5000 + (timesteps[0].observation.score_cumulative.score - oldscore)
                            agent.actor_critic_agent.total_reward += reward

                        agent.actor_critic_agent.buffer.append(
                            [agent.actor_critic_agent.prev_state[0], agent.actor_critic_agent.prev_actions, reward, state[0], True])
                        if save_game:
                            agent.save_game(path, episode)
                        print("Total reward: "+str(agent.actor_critic_agent.total_reward))
                        break
                    timesteps = env.step(step_actions)

    except KeyboardInterrupt:
        pass
