import numpy as np
import random
import argparse
from keras.models import model_from_json, Model
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.optimizers import Adam
import tensorflow as tf
#from keras.engine.training import _collect_trainable_weights
import json

from Models.MachineLearning.ReplayBuffer import ReplayBuffer
from Models.MachineLearning.ActorNetwork import ActorNetwork
from Models.MachineLearning.CriticNetwork import CriticNetwork
from Models.MachineLearning.OU import OU
import timeit

from collections import deque

OU = OU()       #Ornstein-Uhlenbeck Process

class ActorCriticAgent:
    def __init__(self, state_dim, action_space, epsilon):
        self.train_indicator = True
        self.BUFFER_SIZE = 100000
        self.BATCH_SIZE = 32
        self.GAMMA = 0.999999
        self.TAU = 0.1     #Target Network HyperParameters
        self.LRA = 0.0001    #Learning rate for Actor
        self.LRC = 0.0001     #Lerning rate for Critic

        self.action_space = action_space
        self.action_dim = len(self.action_space)
        self.state_dim = state_dim  # TODO Pass variable from State to set this automatically

        np.random.seed(1337)

        self.vision = False

        self.EXPLORE = 100000.
        self.episode_count = 2000
        self.max_steps = 1000
        self.reward = 0
        self.done = False
        self.step = 0
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

        self.actor = ActorNetwork(self.sess, self.state_dim, self.action_dim, self.BATCH_SIZE, self.TAU, self.LRA, self.NUM_STEPS_UNTIL_UPDATE)
        self.critic = CriticNetwork(self.sess, self.state_dim, self.BATCH_SIZE, self.TAU, self.LRC, self.NUM_STEPS_UNTIL_UPDATE)

        self.total_reward = 0
        self.prev_state = None
        self.prev_actions = None
        self.buffer = deque(maxlen=10000)
        self.good_buffer = None
        self.buffer_epsilon = 0.3
        self.buffer_epsilon_decay = 0.9999


        self.actions_softmax = tf.nn.softmax(self.actor.model.output[0])

        self.sess.run(tf.global_variables_initializer())

        # Now load the weight
        try:
            self.actor.model.load_weights("actormodel.h5")
            self.critic.model.load_weights("criticmodel.h5")
            print("Weight load successfully")
        except:
            print("Cannot find the weight")

        # Batch variables
        #self.loss = 0

    def predict(self, game_state, obs):
        state, oldscore, map = game_state.get_state_now(obs)



        if random.random() < self.epsilon:
             action_probs = [1/self.action_dim]*self.action_dim
        else:
            action_probs = self.sess.run(self.actions_softmax, feed_dict={
                self.actor.state: state
            })
        action_index = np.random.choice(range(self.action_dim), 1, p=action_probs)[0]

        bonusreward = 0
        if ((state[0][3]-state[0][2] > 15/200) or state[0][3] == 1) and action_index == 2:
            bonusreward = -40
        if (state[0][3]-state[0][2] < 3/200) and action_index == 2:
            bonusreward = 20
        if state[0][9] >= 24/200 and action_index == 1:
            bonusreward = -10
        if state[0][4] >= 2/100 and action_index == 5:
            bonusreward = 10
        if state[0][4] == 0 and action_index == 5:
            bonusreward = -30
        if self.episode > 0:
            self.buffer.append(
                [self.prev_state[0], self.prev_actions, game_state.reward+bonusreward, state[0], False])  # Add replay
        print(self.action_space[action_index])
        print(game_state.reward+bonusreward)
        self.prev_actions = action_index
        self.prev_state = state
        self.episode += 1

        chosen_action = self.action_space[action_index]
        if chosen_action == "attack":
            game_state.units_attacked = obs.observation.player.army_count
            game_state.last_attacked = state[0][-1]
        if(len(self.buffer) > self.BATCH_SIZE):
            #if self.buffer_epsilon > random.random()):
            #    training_batch = random.sample(self.good_buffer, self.BATCH_SIZE)
            #    self.buffer_epsilon *= self.buffer_epsilon_decay
            #else:
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
        target_actor = np.zeros((len(predicted_state_values), self.action_dim))

        for idx, reward in enumerate(rewards):
            if dones[idx]:
                state_values[idx] = reward
                target_actor[idx][actions[idx]] = reward - predicted_state_values[idx]
            else:
                state_values[idx] = reward + self.GAMMA * next_state_values[idx]
                target_actor[idx][actions[idx]] = reward + self.GAMMA * next_state_values[idx] - predicted_state_values[idx]

        self.actor.train(states, target_actor)

        self.critic.train(states, state_values)



    def probs_to_one_hot(self, probabilities):
        one_hot_tensor = []
        for prob in probabilities:
            a = tf.constant(prob)
            one_hot = tf.one_hot(tf.nn.top_k(a).indices, tf.shape(a)[0]).eval(session=self.sess)
            one_hot_tensor.append(one_hot[0])
        return np.array(one_hot_tensor)
