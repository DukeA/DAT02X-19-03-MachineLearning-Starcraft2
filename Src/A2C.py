# Inspiration from https://github.com/OctThe16th/A2C-Keras without the noise

from keras import models, layers, optimizers
import keras
import keras.backend as K
import tensorflow as tf
from pysc2.env import sc2_env
from pysc2.lib import features, units
from Models.BotFile.aiBot import AiBot
from DLNetwork.ActorNetwork import ActorNetwork
from DLNetwork.CriticNetwork import CriticNetwork
from DLNetwork.StateActionBuffer import StateActionBuffer
from DLNetwork.BuildAgent import BuildAgent
from absl import app
import numpy as np
import h5py
import threading
import time
from collections import defaultdict

MIN_BATCH = 32
LOSS_V = .5
GAMMA = 0.99
N_STEP_RETURN = 10
GAMMA_N = GAMMA ** N_STEP_RETURN
LSTM_LEN = 20
STATE_SIZE = (LSTM_LEN, 11)
action_space = {
    0: "no_op",
    1: "expand",
    2: "build_supply_depot",
    3: "build_refinery",
    4: "build_barracks",
    5: "build_factory",
    6: "build_starport",
    7: "build_tech_lab_barracks",
    8: "build_scv",
    9: "build_marine",
    10: "build_marauder",
    11: "build_reaper",
    12: "build_hellion",
    13: "build_medivac",
    14: "build_viking",
    15: "distribute_scv",
    16: "return_scv"
}


class ActorCriticNetwork(object):
    train_queue = [[], [], [], [], []]  # s, a, r, s', s' terminal mask
    lock_queue = threading.Lock()

    def __init__(self, state_size, network_path=None):
        self.time_steps = state_size[0]
        self.state_size = state_size
        self.action_len = len(action_space)
        self.model = self.create_network()
        if network_path is not None:
            self.model.load_weights(network_path)
        self.NONE_STATE = np.zeros(state_size)

    @staticmethod
    def value_loss():
        def val_loss(y_true, y_pred):
            advantage = y_true - y_pred
            return K.mean(LOSS_V * K.square(advantage))
        return val_loss

    @staticmethod
    def policy_loss(actual_value, predicted_value):
        advantage = actual_value - predicted_value

        def pol_loss(y_true, y_pred):
            log_prob = K.log(K.sum(y_pred * y_true, axis=1, keepdims=True) + 1e-10)
            return log_prob * K.stop_gradient(advantage)
        return pol_loss

    def create_network(self):
        # state_size should be (time_steps, #of_state_parameters)
        state_input = layers.Input(shape=self.state_size)
        actual_value = layers.Input(shape=(1,))

        s1 = layers.LSTM(100, return_sequences=False)(state_input)
        s2 = layers.Dense(50, activation='relu')(s1)

        out_action = layers.Dense(self.action_len, activation='softmax')(s2)
        out_value = layers.Dense(1, name='out_value')(s2)

        model = models.Model(inputs=[state_input, actual_value], outputs=[out_action, out_value])
        model.compile(optimizer=optimizers.RMSprop(),
                      loss=[self.policy_loss(actual_value=actual_value, predicted_value=out_value),
                      self.value_loss(), ])
        model.predict([np.zeros(shape=[1]+list(STATE_SIZE)), np.zeros(shape=(1, 1))])
        return model

    def optimize(self):
        # Some obsolete asynchronous stuff
        if len(self.train_queue[0]) < MIN_BATCH:
            time.sleep(0)
            return

        with self.lock_queue:
            if len(self.train_queue[0]) < MIN_BATCH:
                return

            s, a, r, s_, s_mask = self.train_queue
            self.train_queue = [[], [], [], [], []]

        print("optimize")

        print(s)
        print(a)
        print(r)
        print(s_)
        print(s_mask)
        s = np.vstack(s)
        a = np.vstack(a)
        r = np.vstack(r)
        s_ = np.vstack(s_)
        s_mask = np.vstack(s_mask)

        if len(s) > 5 * MIN_BATCH:
            print("Something about batch")

        v = self.predict_v(s_)
        r = r + GAMMA_N * v * s_mask

        self.model.train_on_batch([s, r], [a, v, r])

        # sample_noise() is not a thing in Dense layer.
        self.model.get_layer('out_action')
        self.model.get_layer('out_value')

    def print_average_weight(self):
        print(np.mean(self.model.get_layer('out_action').get_weights()[1]))

    def train_push(self, s, a, r, s_):
        with self.lock_queue:
            self.train_queue[0].append(s)
            self.train_queue[1].append(a)
            self.train_queue[2].append(r)

            if s_ is None:
                self.train_queue[3].append(self.NONE_STATE)
                self.train_queue[4].append(0.)
            else:
                self.train_queue[3].append(s_)
                self.train_queue[4].append(1.)
        if len(self.train_queue[0]) > MIN_BATCH:
            self.optimize()

    def predict(self, s):
        p, v = self.model.predict([s, np.zeros(shape=(s.shape[0], 1))])
        return p, v

    def predict_p(self, s):
        p, v = self.model.predict([s, np.zeros(shape=(s.shape[0], 1))])
        print(p)
        print(v)
        return p

    def predict_v(self, s):
        p, v = self.model.predict([s, np.zeros(shape=(s.shape[0], 1))])
        return v


class Worker(object):
    def __init__(self, network):
        self.network = network
        self.time_steps = network.state_size[0]
        self.buffer = StateActionBuffer(N_STEP_RETURN)
        self.agent = AiBot(self)
        self.last_action = 0
        self.R = 0
        self.last_lstm_state = [[(50 / 25) / 40, 0, 1 / 10, 0, 0, 0, 0, 0, 12 / 100, 0, 0]] * self.time_steps
        self.old_states = [[(50 / 25) / 40, 0, 1 / 10, 0, 0, 0, 0, 0, 12 / 100, 0, 0]] * (self.time_steps - 1)

    def reset(self):
        self.last_action = 0
        self.R = 0
        self.last_lstm_state = [[[(50 / 25) / 40, 0, 1 / 10, 0, 0, 0, 0, 0, 12 / 100, 0, 0]] * self.time_steps]
        self.old_states = [[(50 / 25) / 40, 0, 1 / 10, 0, 0, 0, 0, 0, 12 / 100, 0, 0]] * (self.time_steps - 1)
        self.agent.reset()

        # Should it reset the buffer?
        self.buffer.reset()

    def predict_action(self, state):
        corrected_state = self.format_lstm_state(state)
        print(corrected_state)

        last_action_vector = np.zeros(len(action_space))
        last_action_vector[self.last_action] = 1

        self.buffer.add(self.last_lstm_state, last_action_vector, corrected_state, 0)

        self.last_lstm_state = corrected_state
        p = self.network.predict_p(corrected_state)[0]

        # TODO: An action randomizer

        self.last_action = np.random.choice(len(action_space), p=p)

        return action_space.get(self.last_action, "no_op")

    def format_lstm_state(self, state):
        """
        Takes a state input and formats it to LSTM state. Doesn't update self.old_states.
        :param state:
        :return:
        """
        newest_state = len(state) - 1
        units_amount = defaultdict(int, state[newest_state][5])
        minerals = int(state[newest_state][0]/25)
        if minerals > 40:
            minerals = 40
        minerals = minerals/40
        gas = int(state[newest_state][1]/25)
        if gas > 40:
            gas = 40
        gas = gas/40
        command_centers = units_amount[units.Terran.CommandCenter.value]/10
        if command_centers > 1:
            command_centers = 1
        supply_depots = units_amount[units.Terran.SupplyDepot.value]/25
        if supply_depots > 1:
            supply_depots = 1
        refineries = units_amount[units.Terran.Refinery.value]/24
        if refineries > 1:
            refineries = 1
        barracks = units_amount[units.Terran.Barracks.value]/15
        if barracks > 1:
            barracks = 1
        factories = units_amount[units.Terran.Factory.value]/15
        if factories > 1:
            factories = 1
        starports = units_amount[units.Terran.Starport.value]/15
        if starports > 1:
            starports = 1
        scvs = units_amount[units.Terran.SCV.value]/100
        if scvs > 1:
            scvs = 1
        marines = units_amount[units.Terran.Marine.value]/100
        if marines > 1:
            marines = 1
        step = int(state[newest_state][4]*5/(16*1.4*5))    # Binning steps to 5 second intervals.
        step = step/134    # Equivalent to about 11 minutes
        if step > 1:
            step = 1

        new_state = [minerals, gas, command_centers, supply_depots, refineries, barracks,
                     factories, starports, scvs, marines, step]

        time_state = self.old_states+[new_state]
        formatted_state = np.asarray([time_state])
        formatted_state.reshape(1, self.time_steps, len(new_state))
        self.old_states = self.old_states[1:len(self.old_states)]+[new_state]
        return formatted_state

    def train(self):
        _, _, s_, reward, _ = self.buffer.get_newest_data()
        self.R = (self.R + reward * GAMMA_N) / GAMMA
        memory = self.buffer.get_buffer()

        def get_sample(m, k):
            st, ac, _, _, _ = m[0]
            _, _, _, st_, _ = m[k-1]

            return st, ac, self.R, st_

        if s_ is None:
            while len(memory) > 0:
                n = len(memory)
                s, a, r, s_ = get_sample(memory, n)
                self.network.train_push(s, a, r, s_)

                self.R = (self.R - memory[0][2]) / GAMMA
                memory.pop(0)

            self.R = 0

        if len(memory) >= N_STEP_RETURN:
            s, a, r, s_ = get_sample(memory, N_STEP_RETURN)
            self.network.train_push(s, a, r, s_)

            self.R = self.R - memory[0][2]


is_training = True
step_mul = 5
maximum_bot_steps_per_episode = 16 * 60 * 4 * 1.4 / step_mul


def run(self):
    episode = 0
    # path = path to network
    # network = ActorCriticNetwork(STATE_SIZE, path)
    network = ActorCriticNetwork(STATE_SIZE)
    worker = Worker(network)

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
                step_mul=step_mul,  # about 200 APM
                game_steps_per_episode=maximum_bot_steps_per_episode * step_mul * 1.1,
                # save_replay_episodes=1, #How often do you save replays
                # replay_dir="C:/Users/Claes/Desktop/StarCraft2Replays", # Need to change to your own path
                visualize=True,
                disable_fog=True) as env:
            while True:
                worker.agent.setup(env.observation_spec(), env.action_spec())

                timesteps = env.reset()
                worker.reset()
                episode += 1
                predicted_this_step = False
                R = 0
                done = False
                reward = 0
                while True:
                    step_actions = [worker.agent.step(timesteps[0])]
                    if (worker.agent.next_action is not None
                            and worker.agent.next_action is not "updateState"
                            and worker.agent.predicted_this_step):
                        predicted_this_step = True
                        print("AI just predicted something")
                        if len(worker.agent.game_state.get_state()) > 0:
                            latest_state = worker.agent.game_state.get_state()[
                                len(worker.agent.game_state.get_state()) - 1]
                            if worker.agent.game_state.units_amount[units.Terran.SCV.value] >= 14:
                                print(">=14 SCVs at agent step " + str(worker.agent.steps))
                                done = True
                                reward = 1
                                s, a, s_, r, d = worker.buffer.get_newest_data()
                                worker.buffer.set_newest_data((s, a, None, reward, done))
                            # A "bug" makes this ineffective (might be fixed)
                            elif latest_state[4] >= maximum_bot_steps_per_episode:
                                print("here")
                                done = True
                                reward = -1
                                s, a, s_, r, d = worker.buffer.get_newest_data()
                                worker.buffer.set_newest_data((s, a, None, reward, done))

                    if timesteps[0].last() and not predicted_this_step:
                        done = True
                        reward = -1
                        s = worker.last_lstm_state
                        a = np.zeros(len(action_space))
                        a[worker.last_action] = 1
                        worker.buffer.add((s, a, None, reward, done))

                    if done or predicted_this_step:
                        worker.train()

                    predicted_this_step = False
                    R += reward
                    if done:
                        break
                    timesteps = env.step(step_actions)
                if np.mod(episode, 3) == 0:
                    if is_training:
                        print("Saving model")
                        network.model.save_weights("model.h5", overwrite=True)

                print("TOTAL REWARD @ " + str(episode) + "-th Episode  : Reward " + str(R))

    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    app.run(run)
