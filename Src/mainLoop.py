from pysc2.env import sc2_env
from pysc2.lib import features, units
from Models.BotFile.aiBot import AiBot


def main(unused_argv):
    agent = AiBot()
    best = None
    try:
        with sc2_env.SC2Env(
                map_name="AbyssalReef",
                players=[sc2_env.Agent(sc2_env.Race.terran),
                         sc2_env.Bot(sc2_env.Race.terran,
                                     sc2_env.Difficulty.very_easy)],
                agent_interface_format=features.AgentInterfaceFormat(
                    feature_dimensions=features.Dimensions(screen=84, minimap=64),
                    use_feature_units=True),
                step_mul=5,  # about 200 APM
                game_steps_per_episode=13000,  # Ends after 13 minutes (real-time)
                # save_replay_episodes=1, #How often do you save replays
                # replay_dir="C:/Users/Claes/Desktop/StarCraft2Replays", # Need to change to your own path
                visualize=False,
                disable_fog=True) as env:
            while True:
                agent.setup(env.observation_spec(), env.action_spec())

                timesteps = env.reset()
                agent.reset()
                check = 0

                while True:
                    step_actions = [agent.step(timesteps[0])]

                    if timesteps[0].last():
                        agent.agent.remember(agent.previous_state,
                                             agent.previous_action, -10, agent.previous_state, True)
                        agent.agent.save('shortgames.h5')
                        if len(agent.agent.memory) > 32:
                            agent.agent.replay(32)
                        agent.previous_action = None
                        agent.previous_state = None
                        break
                    if agent.game_state.units_amount[units.Terran.Marine.value] >= 10 and\
                            agent.game_state.units_amount[units.Terran.SCV.value] >= 16:
                        agent.agent.remember(agent.previous_state,
                                             agent.previous_action, 10, agent.previous_state, True)
                        agent.agent.save('shortgames.h5')
                        if len(agent.agent.memory) > 32:
                            agent.agent.replay(32)
                        agent.previous_action = None
                        agent.previous_state = None
                        if best is None or best > agent.steps*5:
                            best = agent.steps*5
                            print("best is:" + str(best))

                        break

                    timesteps = env.step(step_actions)

    except KeyboardInterrupt:
        pass
