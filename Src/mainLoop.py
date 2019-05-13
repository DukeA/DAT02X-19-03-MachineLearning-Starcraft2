from pysc2.env import sc2_env
from pysc2.lib import features
from Models.BotFile.aiBot import AiBot
from Models.MachineLearning.ActorCriticAgent import ActorCriticAgent
import pickle
import os
from collections import deque
import matplotlib.pyplot as plt


def main(unused_argv):
    agent = AiBot()
    epsilon = 0
    epsilon_min = 0
    eps_reduction_factor = 0.99
    save_game = False
    episode = 0
    path = ""
    save_buffer = False

    last_100 = deque(maxlen=100)
    iter = 1

    agent.actor_critic_agent = ActorCriticAgent(30,
                                                ["no_op",
                                                 "build_scv",
                                                 "build_supply_depot",
                                                 "build_marine",
                                                 "build_barracks",
                                                 "return_scv",
                                                 "attack"],
                                                epsilon)

    game_results = []
    latest_result = 0
    all_rewards = []

    # Plot setup
    fig, ax = plt.subplots(num=1)
    ax.plot()
    ax.set_title("Score for each game over time")

    fig2, ax2 = plt.subplots(num=3)
    ax2.plot()
    ax2.set_title("win%")

    fig3, ax3 = plt.subplots(num=4)
    ax3.plot()
    ax3.set_title("totalreward")

    try:
        with sc2_env.SC2Env(
                map_name="AbyssalReef",
                players=[sc2_env.Agent(sc2_env.Race.terran),
                         sc2_env.Bot(sc2_env.Race.terran,
                                     sc2_env.Difficulty.medium)],
                agent_interface_format=features.AgentInterfaceFormat(
                    feature_dimensions=features.Dimensions(screen=84, minimap=64),

                    use_feature_units=True,
                    use_raw_units=True,
                    use_camera_position=True),
                step_mul=8,
                game_steps_per_episode=30000,
                visualize=False,
                disable_fog=True) as env:
            while True:
                agent.setup(env.observation_spec(), env.action_spec())

                timesteps = env.reset()
                agent.actor_critic_agent.build_index = 0
                if os.path.isfile('good_buffer.data'):
                    filehandler1 = open("good_buffer.data", 'rb')
                    agent.actor_critic_agent.good_buffer = pickle.load(filehandler1)
                agent.reset()
                if episode > 0:
                    all_rewards = all_rewards + [agent.actor_critic_agent.total_reward]
                    with open('all_rewards.txt', mode='w') as filehandle:
                        for i in all_rewards:
                            filehandle.write("%s\n" % i)
                    game_results = game_results + [latest_result]
                    with open('game_results.txt', mode='w') as filehandle:
                        for i in game_results:
                            filehandle.write("%s\n" % i)
                episode += 1
                if agent.actor_critic_agent.epsilon > epsilon_min:
                    agent.actor_critic_agent.epsilon *= eps_reduction_factor
                if agent.actor_critic_agent.buffer_epsilon > agent.actor_critic_agent.buffer_epsilon_min:
                    agent.actor_critic_agent.buffer_epsilon *= agent.actor_critic_agent.buffer_epsilon_decay
                if agent.actor_critic_agent.actor.IMITATION_WEIGHT > 0.0001:
                    agent.actor_critic_agent.actor.IMITATION_WEIGHT *= 0.97
                else:
                    agent.actor_critic_agent.actor.IMITATION_WEIGHT = 0.0001
                print("Imitation weight: ", agent.actor_critic_agent.actor.IMITATION_WEIGHT)

                # For determining win/loss/tie
                agent.reward = 0
                # For plotting total reward
                agent.actor_critic_agent.total_reward = 0

                while True:
                    step_actions = [agent.step(timesteps[0], epsilon, episode)]

                    if timesteps[0].last():
                        state, oldscore, map = agent.game_state.get_state_now(timesteps[0])

                        # If it won
                        if agent.reward == 1:
                            last_100.append(1)
                            latest_result = 1
                            end_reward = 1
                        # If it lost
                        elif agent.reward == -1:
                            last_100.append(0)
                            latest_result = 0
                            end_reward = -1
                        # If time's up
                        else:
                            last_100.append(0)
                            latest_result = 0
                            end_reward = -0.5

                        agent.actor_critic_agent.total_reward += end_reward

                        if agent.actor_critic_agent.GOOD_GAME:
                            agent.actor_critic_agent.good_buffer.append(
                                [agent.actor_critic_agent.prev_state[0],
                                 agent.actor_critic_agent.prev_actions, end_reward, state[0], True])
                        else:
                            agent.actor_critic_agent.buffer.append(
                                [agent.actor_critic_agent.prev_state[0],
                                 agent.actor_critic_agent.prev_actions, end_reward, state[0], True])

                        if save_buffer and agent.reward == 1:
                            filehandler = open("good_buffer.data", 'wb')
                            pickle.dump(agent.actor_critic_agent.good_buffer, filehandler)
                            print(len(agent.actor_critic_agent.good_buffer))
                        if save_game:
                            agent.save_game(path, episode)
                        print("Score: ", timesteps[0].observation.score_cumulative.score)
                        ax.scatter(
                            episode, timesteps[0].observation.score_cumulative.score, s=3, c='blue')
                        fig.savefig("score.png")

                        if len(last_100) == last_100.maxlen:
                            percent = sum(last_100) / 100
                            ax2.scatter(iter, percent, s=3, c='blue')
                            iter += 1
                            fig2.savefig("winpercent.png")
                        ax3.scatter(episode, agent.actor_critic_agent.total_reward, s=3, c='blue')
                        fig3.savefig("total_reward.png")
                        break
                    timesteps = env.step(step_actions)

    except KeyboardInterrupt:
        pass
