from pysc2.env import sc2_env
from pysc2.lib import features, units
from Models.BotFile.aiBot import AiBot
from DLNetwork.ActorNetwork import ActorNetwork
from DLNetwork.CriticNetwork import CriticNetwork
from DLNetwork.StateActionBuffer import StateActionBuffer
from DLNetwork.BuildAgent import BuildAgent
from absl import app
import numpy as np
import tensorflow as tf
from keras import backend as K
import h5py


def main(unused_argv):
    is_training = True
    BUFFER_SIZE = 100000
    BATCH_SIZE = 32
    GAMMA = 0.99
    TAU = 0.001
    LRA = 0.0001
    LRC = 0.001

    step_mul = 5
    maximum_bot_steps_per_episode = 16 * 60 * 4 * 1.4 / step_mul    # A "bug" makes this ineffective


    LSTM_len = 20
    state_size = (LSTM_len, 13)
    action_len = 17

    EXPLORE = 100000.
    epsilon = 1

    # Might need GPU version of tensorflow
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    sess = tf.Session(config=config)
    K.set_session(sess)

    buffer = StateActionBuffer(BUFFER_SIZE)
    actor = ActorNetwork(sess, state_size, action_len, BATCH_SIZE, TAU, LRA)
    critic = CriticNetwork(sess, state_size, action_len, BATCH_SIZE, TAU, LRC)
    build_agent = BuildAgent(actor, critic, buffer, LSTM_len)

    # Now load the weight
    print("Now we load the weight")
    try:
        actor.model.load_weights("actormodel.h5")
        critic.model.load_weights("criticmodel.h5")
        actor.target_model.load_weights("actormodel.h5")
        critic.target_model.load_weights("criticmodel.h5")
        print("Weight load successfully")
    except:
        print("Cannot find the weight")

    agent = AiBot(build_agent)
    episode = 0

    try:
        with sc2_env.SC2Env(
                map_name="AbyssalReef",
                players=[sc2_env.Agent(sc2_env.Race.terran),
                         sc2_env.Bot(sc2_env.Race.terran,
                                     sc2_env.Difficulty.very_easy)],
                agent_interface_format=features.AgentInterfaceFormat(
                    feature_dimensions=features.Dimensions(screen=84, minimap=64),
                    use_feature_units=True,
                    use_raw_units=True),
                step_mul=step_mul,  #about 200 APM
                game_steps_per_episode=maximum_bot_steps_per_episode*step_mul*1.1,
                #save_replay_episodes=1, #How often do you save replays
                #replay_dir="C:/Users/Claes/Desktop/StarCraft2Replays", # Need to change to your own path
                visualize=True,
                disable_fog=True) as env:
            while True:
                agent.setup(env.observation_spec(), env.action_spec())

                timesteps = env.reset()
                agent.reset()
                episode += 1
                total_reward = 0
                done = False
                game_result = 0
                while True:
                    loss = 0
                    epsilon -= 1.0 / EXPLORE
                    step_actions = [agent.step(timesteps[0])]
                    if timesteps[0].last():
                        done = True
                    if is_training:
                        if (agent.next_action is not None
                                and agent.next_action is not "updateState"
                                and agent.predicted_this_step):
                            if len(agent.game_state.get_state()) > 0:
                                latest_state = agent.game_state.get_state()[len(agent.game_state.get_state()) - 1]
                                if agent.game_state.units_amount[units.Terran.SCV.value] >= 14:
                                    print(">=14 SCVs at agent step " + str(agent.steps))
                                    done = True
                                    game_result = 1
                                elif latest_state[4] >= maximum_bot_steps_per_episode:  # A "bug" makes this ineffective
                                    print("here")
                                    done = True
                                    game_result = -1
                            print("AI just predicted something")
                            if done:
                                buffer.set_latest_done()
                                buffer.set_latest_reward(game_result)
                            batch = buffer.get_batch(BATCH_SIZE)
                            states = np.asarray([e[0] for e in batch])
                            actions = np.asarray([e[1] for e in batch])
                            new_states = np.asarray([e[2] for e in batch])
                            rewards = np.asarray([e[3] for e in batch])
                            y_t = np.asarray([e[1] for e in batch])
                            dones = np.asarray([e[4] for e in batch])

                            target_q_values = critic.target_model.predict([new_states,
                                                                           actor.target_model.predict(new_states)])

                            for k in range(len(batch)):
                                if dones[k]:
                                    y_t[k] = rewards[k]
                                else:
                                    y_t[k] = rewards[k] + GAMMA * target_q_values[k]

                            loss += critic.model.train_on_batch([states, actions], y_t)
                            a_for_grad = actor.model.predict(states)
                            grads = critic.gradients(states, a_for_grad)
                            # Not sure if grads[0] breaks anything.
                            actor.train(states, grads[0])
                            actor.target_train()
                            critic.target_train()

                            total_reward += buffer.get_newest_data()[3]
                    if done:
                        break
                    timesteps = env.step(step_actions)
                if np.mod(episode, 3) == 0:
                    if is_training:
                        print("Saving model")
                        actor.model.save_weights("actormodel.h5", overwrite=True)
                        critic.model.save_weights("criticmodel.h5", overwrite=True)
                print("TOTAL REWARD @ " + str(episode) + "-th Episode  : Reward " + str(total_reward))

    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    app.run(main)
