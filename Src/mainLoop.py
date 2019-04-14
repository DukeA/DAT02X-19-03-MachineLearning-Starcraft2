from pysc2.env import sc2_env
from pysc2.lib import features
from Models.BotFile.aiBot import AiBot
from Models.MachineLearning.ActorCriticAgent import ActorCriticAgent
import pickle
import os


def main(unused_argv):
    agent = AiBot()
    epsilon = 0.4
    epsilon_min = 0.01
    eps_reduction_factor = 0.99
    save_game = False
    episode = 0
    path = ""
    save_buffer = False

    agent.actor_critic_agent = ActorCriticAgent(30,
                                                ["no_op",
                                                 "build_scv",
                                                 "build_supply_depot",
                                                 "build_marine",
                                                 "build_barracks",
                                                 "return_scv",
                                                 "attack"],
                                                epsilon)
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
                agent.actor_critic_agent.build_index = 0
                if os.path.isfile('/path/to/file'):
                    filehandler1 = open("good_buffer.data", 'rb')
                    agent.actor_critic_agent.good_buffer = pickle.load(filehandler1)
                agent.reset()
                episode += 1
                if agent.actor_critic_agent.epsilon > epsilon_min:
                    agent.actor_critic_agent.epsilon *= eps_reduction_factor
                if agent.actor_critic_agent.buffer_epsilon > agent.actor_critic_agent.buffer_epsilon_min:
                    agent.actor_critic_agent.buffer_epsilon *= agent.actor_critic_agent.buffer_epsilon_decay
                print(agent.actor_critic_agent.epsilon)
                agent.reward = 0
                while True:
                    step_actions = [agent.step(timesteps[0], epsilon)]

                    if timesteps[0].last():
                        state, oldscore, map = agent.game_state.get_state_now(timesteps[0])
                        if agent.reward == 1:
                            reward = 1000
                        elif agent.reward == -1:
                            reward = -1000
                        if agent.actor_critic_agent.GOOD_GAME:
                            agent.actor_critic_agent.good_buffer.append(
                                [agent.actor_critic_agent.prev_state[0], agent.actor_critic_agent.prev_actions, reward, state[0], True])
                        else:
                            agent.actor_critic_agent.buffer.append(
                                [agent.actor_critic_agent.prev_state[0], agent.actor_critic_agent.prev_actions, reward, state[0], True])

                        if save_buffer:
                            filehandler = open("good_buffer.data", 'wb')
                            pickle.dump(agent.actor_critic_agent.good_buffer, filehandler)
                            print(len(agent.actor_critic_agent.good_buffer))
                        if save_game:
                            agent.save_game(path, episode)
                        break
                    timesteps = env.step(step_actions)

    except KeyboardInterrupt:
        pass
