from pysc2.env import sc2_env
from pysc2.lib import features
from Models.BotFile.aiBot import AiBot
from Models.MachineLearning.ActorCriticAgent import ActorCriticAgent


def main(unused_argv):
    agent = AiBot()
    epsilon = 0.2
    epsilon_min = 0.01
    eps_reduction_factor = 0.999
    save_game = False
    episode = 0
    path = ""

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
                                         sc2_env.Difficulty.easy)],
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
                episode += 1
                if agent.actor_critic_agent.epsilon > epsilon_min:
                    agent.actor_critic_agent.epsilon *= eps_reduction_factor
                print(agent.actor_critic_agent.epsilon)
                agent.reward = 0
                while True:
                    step_actions = [agent.step(timesteps[0], epsilon)]

                    if timesteps[0].last():
                        state, oldscore, map = agent.game_state.get_state_now(timesteps[0])
                        if agent.reward == 1:
                            reward = 30000 + (timesteps[0].observation.score_cumulative.score - oldscore)
                        else:
                            reward = -30000 + (timesteps[0].observation.score_cumulative.score - oldscore)


                        agent.actor_critic_agent.buffer.append(
                            [agent.actor_critic_agent.prev_state[0], agent.actor_critic_agent.prev_actions, reward, state[0], True])
                        print(agent.steps)
                        if save_game:
                            agent.save_game(path, episode)
                        break
                    timesteps = env.step(step_actions)

    except KeyboardInterrupt:
        pass
