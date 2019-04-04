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

MIN_BATCH = 32
LOSS_V = .5
GAMMA = 0.99
N_STEP_RETURN = 10
GAMMA_N = GAMMA ** N_STEP_RETURN


class ActorCriticNetwork(object):
    train_queue = [[], [], [], [], []]  # s, a, r, s', s' terminal mask
    lock_queue = threading.Lock()

    def __init_(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.model = self.create_network()
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

        out_action = layers.Dense(self.action_size, activation='softmax')(s2)
        out_value = layers.Dense(1, name='out_value')(s2)

        model = models.Model(input=[state_input, actual_value], output=[out_action, out_value])
        model.compile(optimizer=optimizers.RMSprop(),
                      loss=[self.policy_loss(actual_value=actual_value, predicted_value=out_value),
                      self.value_loss(),
                      'mae'])
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

        self.model.get_layer('out_action').sample_noise()
        self.model.get_layer('out_value').sample_noise()

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
        p, v, r = self.model.predict([s, np.zeros(shape=(s.shape[0], 1))])
        return p, v

    def predict_p(self, s):
        p, v, r = self.model.predict([s, np.zeros(shape=(s.shape[0], 1))])
        return p

    def predict_v(self, s):
        p, v, r = self.model.predict([s, np.zeros(shape=(s.shape[0], 1))])
        return v

# TODO: Agent.