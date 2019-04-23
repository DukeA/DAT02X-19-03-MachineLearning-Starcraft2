import numpy as np
import random
import math
import argparse
from keras.models import model_from_json, Model
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.optimizers import Adam
import tensorflow as tf
# from keras.engine.training import _collect_trainable_weights
import json

from Models.MachineLearning.ReplayBuffer import ReplayBuffer
from Models.MachineLearning.ActorNetwork import ActorNetwork
from Models.MachineLearning.CriticNetwork import CriticNetwork
import timeit

from collections import deque

class ActorCriticAgent:
    def __init__(self, state_dim, action_space, epsilon):

        ############### Hyperparameters #################

        self.train_indicator = True
        self.BATCH_SIZE = 64
        self.GAMMA = 0.9995
        self.TAU = 0.1  # Target Network HyperParameters
        self.LRA = 0.000001  # Learning rate for Actor
        self.LRC = 0.000001  # Lerning rate for Critic

        self.buffer = deque(maxlen=5000)
        self.good_buffer = deque(maxlen=8000)
        self.GOOD_GAME = False
        self.buffer_epsilon = 0.
        self.buffer_epsilon_decay = 0.99
        self.buffer_epsilon_min = 0.0

        ################ Other stuff #####################

        self.action_space = action_space
        self.action_dim = len(self.action_space)
        self.state_dim = state_dim  # TODO Pass variable from State to set this automatically

        np.random.seed(1337)

        self.epsilon = epsilon
        self.indicator = 0
        self.episode = 0
        self.NUM_STEPS_UNTIL_UPDATE = 10

        # Tensorflow GPU optimization
        self.config = tf.ConfigProto()
        self.config.gpu_options.allow_growth = True
        self.sess = tf.Session(config=self.config)
        from keras import backend as k
        k.set_session(self.sess)

        self.actor = ActorNetwork(self.sess, self.state_dim, self.action_dim,
                                  self.BATCH_SIZE, self.TAU, self.LRA, self.NUM_STEPS_UNTIL_UPDATE)
        self.critic = CriticNetwork(self.sess, self.state_dim, self.BATCH_SIZE,
                                    self.TAU, self.LRC, self.NUM_STEPS_UNTIL_UPDATE)

        self.actions = tf.placeholder(tf.int32)
        self.action_one_hot = tf.one_hot(self.actions, self.action_dim)

        self.total_reward = 0
        self.prev_state = None
        self.prev_actions = None
        self.bonusreward = 0

        self.actions_softmax = tf.nn.softmax(self.actor.model.output[0])

        self.sess.run(tf.global_variables_initializer())

        self.build_order = ["scv", "scv", "supply", "scv", "scv", "barracks", "scv", "barracks", "scv",
                            "barracks", "scv", "supply", "scv", "barracks", "barracks", "scv", "barracks", "scv", "supply"]
        self.build_index = 0
        # Now load the weight
        try:
            self.actor.model.load_weights("actormodel.h5")
            self.critic.model.load_weights("criticmodel.h5")
            print("Weight load successfully")
        except:
            print("Cannot find the weight")

        # Batch variables
        # self.loss = 0

    def predict(self, game_state, obs):
        state, oldscore, map = game_state.get_state_now(obs)
        if self.GOOD_GAME:

            if self.build_index >= len(self.build_order):
                if state[0][7] < 6/10:
                    if state[0][0] >= 150/3000:
                        action_index = 4
                    elif state[0][4] >= 1/200:
                        action_index = 5
                    else:
                        action_index = 0
                elif state[0][8] >= 10/200 and random.random() < 0.1:
                    action_index = 6
                elif state[0][4] >= 1/200:
                    action_index = 5
                elif state[0][3]-state[0][2] <= 3/200 and state[0][0] > 100/3000:
                    action_index = 2
                elif state[0][3]-state[0][2] >= 1/200 and state[0][0] > 50/3000:
                    action_index = 3
                elif state[0][4] >= 1/200:
                    action_index = 5
                else:
                    action_index = 0
            else:
                build = self.build_order[self.build_index]
                if build == "scv":
                    if state[0][0] >= 50/3000 and state[0][3]-state[0][2] >= 1/200:
                        action_index = 1
                        self.build_index += 1
                    elif state[0][4] >= 1/200:
                        action_index = 5
                    else:
                        action_index = 0

                if build == "supply":
                    if state[0][0] >= 100/3000:
                        action_index = 2
                        self.build_index += 1
                    elif state[0][4] >= 1/200:
                        action_index = 5
                    else:
                        action_index = 0

                if build == "barracks":
                    if state[0][0] >= 150/3000:
                        action_index = 4
                        self.build_index += 1
                    elif state[0][4] >= 1/200:
                        action_index = 5
                    else:
                        action_index = 0
        else:
            if random.random() < self.epsilon:
                action_probs = [1/self.action_dim]*self.action_dim
                # "print("Random action")
            else:
                action_probs = self.sess.run(self.actions_softmax, feed_dict={
                    self.actor.state: state
                })
                #print("No_op: " + '%.3e' % action_probs[0] +

                 #     ".  SCV: " + '%.3e' % action_probs[1] +

                  #    ".  Supply: " + '%.3e' % action_probs[2] +

                   #   ".  Marine: " + '%.3e' % action_probs[3] +

                    #  ".  Rax: " + '%.3e' % action_probs[4] +

                     # ".  Mine: " + '%.3e' % action_probs[5] +

                      #".  Attack: " + '%.3e' % action_probs[6])
                # if math.isnan(action_probs[0]):
                #weights = self.actor.model.get_weights()
                #print("Found nan")
            action_index = np.random.choice(range(self.action_dim), 1, p=action_probs)[0]

        # print(game_state.reward+bonusreward)
        if self.GOOD_GAME and self.episode > 0:
            self.good_buffer.append([self.prev_state[0], self.prev_actions,
                                     0, state[0], False])

        elif self.episode > 0:
            self.buffer.append(
                [self.prev_state[0], self.prev_actions, 0, state[0], False])  # Add replay

        # print("Reward: ", game_state.reward+bonusreward)

        # discourage bad supplydepots
        # if ((state[0][3]-state[0][2] > 15/200) or state[0][3] == 1) and action_index == 2:
        #     self.bonusreward = -100
            #print(self.bonusreward + game_state.reward)
        # encourage good supplydepots
        # if (state[0][3]-state[0][2] < 3/200) and action_index == 2:
        #     bonusreward = 80
        # discourage too many scvs
        # if state[0][9] >= 24/200 and action_index == 1:
        #     self.bonusreward = -80
        # encourage return scv
        # if state[0][4] >= 2/200 and action_index == 5 and not state[0][4] >= 20:
        #     self.bonusreward = 20
        # discourage doing nothing
        # if state[0][0] > 500/3000 and action_index == 0:
        #     bonusreward = -40

        # checking if returnscv possible
        # if state[0][4] == 0 and action_index == 5:
        #     # print("bad return")
        #     bonusreward = -1
        # # check if build marine is possible
        # if (state[0][7] == 0 or state[0][0] < 50/3000 or state[0][3]-state[0][2] == 0) and action_index == 3:
        #     # print("bad marine")
        #     bonusreward = -1
        # # check is build scv is possible
        # if (state[0][5] == 0 or state[0][0] < 50/3000 or state[0][3]-state[0][2] == 0) and action_index == 1:
        #     # print("bad scv")
        #     bonusreward = -1
        # # check build supply depot possible
        # if state[0][0] < 100/3000 and action_index == 2:
        #     # print("bad supplydepot")
        #     bonusreward = -1
        # # check build barracks possible
        # if (state[0][6] == 0 or state[0][0] < 150/3000) and action_index == 4:
        #     # print("bad barrack")
        #     bonusreward = -1
        # # check if attack is possible
        # if state[0][8] <= 5/200 and action_index == 6:
        #     # print("bad attack")
        #     bonusreward = -1

        self.total_reward += game_state.reward+self.bonusreward
        self.bonusreward = 0
        self.prev_actions = action_index
        self.prev_state = state
        self.episode += 1

        chosen_action = self.action_space[action_index]
        # print(chosen_action)
        # print(action_probs)

        if chosen_action == "attack":
            game_state.units_attacked = obs.observation.player.army_count/200
            game_state.last_attacked = state[0][-1]
        if(len(self.buffer) > self.BATCH_SIZE):
            if self.buffer_epsilon > random.random():
                training_batch = random.sample(self.good_buffer, self.BATCH_SIZE)
            else:
                training_batch = random.sample(self.buffer, self.BATCH_SIZE)
            self.train(training_batch)

        # FOR TESTING
        if np.mod(self.episode, 30) == 0 and self.episode > 0:
            if self.train_indicator:
                self.actor.model.save_weights("actormodel.h5", overwrite=True)
                with open("actormodel.json", "w") as outfile:
                    json.dump(self.actor.model.to_json(), outfile)

                self.critic.model.save_weights("criticmodel.h5", overwrite=True)
                with open("criticmodel.json", "w") as outfile:
                    json.dump(self.critic.model.to_json(), outfile)

        return chosen_action

    def train(self, training_batch):
        states = np.asarray([row[0] for row in training_batch])
        actions = np.asarray([row[1] for row in training_batch])
        rewards = np.asarray([row[2] for row in training_batch])
        next_states = np.asarray([row[3] for row in training_batch])
        dones = np.asarray([row[4] for row in training_batch])

        next_state_values = self.critic.model.predict(next_states)
        state_values = next_state_values

        predicted_state_values = self.critic.model.predict(states)

        for idx, reward in enumerate(rewards):
            if dones[idx]:
                state_values[idx] = reward
            else:
                state_values[idx] = reward + self.GAMMA * next_state_values[idx]

        advantages = [state_val[0] - predicted_state_values[idx][0]
                      for idx, state_val in enumerate(state_values)]

        action_one_hots = self.sess.run(self.action_one_hot, feed_dict={
            self.actions: actions
        })

        self.actor.train(states, action_one_hots, advantages)
        self.critic.train(states, state_values)

    def probs_to_one_hot(self, probabilities):
        one_hot_tensor = []
        for prob in probabilities:
            a = tf.constant(prob)
            one_hot = tf.one_hot(tf.nn.top_k(a).indices, tf.shape(a)[0]).eval(session=self.sess)
            one_hot_tensor.append(one_hot[0])
        return np.array(one_hot_tensor)
