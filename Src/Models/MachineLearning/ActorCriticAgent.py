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

OU = OU()       #Ornstein-Uhlenbeck Process

class ActorCriticAgent:
    def __init__(self, state_dim, action_space):
        self.train_indicator = True
        self.BUFFER_SIZE = 100000
        self.BATCH_SIZE = 32
        self.GAMMA = 0.9
        self.TAU = 0.1     #Target Network HyperParameters
        self.LRA = 0.0001    #Learning rate for Actor
        self.LRC = 0.001     #Lerning rate for Critic

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
        self.epsilon = 1
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
        self.buff = ReplayBuffer(self.BUFFER_SIZE)    # Create replay buffer

        self.total_reward = 0
        self.prev_state = None
        self.prev_actions = None


        # Now load the weight
        print("Now we load the weight")
        try:
            self.actor.model.load_weights("actormodel.h5")
            self.critic.model.load_weights("criticmodel.h5")
            self.actor.target_model.load_weights("actormodel.h5")
            self.critic.target_model.load_weights("criticmodel.h5")
            print("Weight load successfully")
        except:
            print("Cannot find the weight")

        # Batch variables
        #self.loss = 0

    def predict(self, game_state, obs):

        state = np.hstack((game_state.minerals, game_state.vespene, obs.observation.player.food_workers, obs.observation.player.food_cap))

        loss = 0

        self.epsilon *= 0.99
        print("Epsilon: ", self.epsilon)

        if self.episode > 0:
            test = self.critic.model.trainable_weights
            test2 = self.sess.run(test)

            if len(self.buffer) == self.NUM_STEPS_UNTIL_UPDATE:
                if obs.last():
                    R = 0
                else:
                    R = self.critic.model.predict(state.reshape(1, state.shape[0]))[0][0]

                states = np.asarray([row[0] for row in self.buffer])
                actions_one_hot = np.asarray([row[1] for row in self.buffer])
                rewards = np.asarray([row[2] for row in self.buffer])
                new_states = np.asarray([row[3] for row in self.buffer])
                values = np.asarray([row[4] for row in self.buffer])

                discounted_rewards = np.zeros(len(self.buffer))
                discounted_values = np.zeros(len(self.buffer))

                for idx, reward in reversed(list(enumerate(rewards))):
                    R = reward + self.GAMMA * R
                    discounted_rewards[idx] = R
                    discounted_values[idx] = R - values[idx]

                self.actor.train(states, actions_one_hot, discounted_values)
                self.critic.train(states, discounted_rewards)

                self.buffer = []

        r = random.random()

        if r < self.epsilon:
            action_probabilities = "random"
            actions_one_hot = tf.one_hot([random.randint(0, self.action_dim-1)], self.action_dim).eval(session=self.sess)[0]
        else:
            action_probabilities = self.actor.model.predict(state.reshape(1, state.shape[0]))
            chosen_actions = np.argmax(action_probabilities, axis=1)
            actions_one_hot = tf.one_hot(chosen_actions, self.action_dim).eval(session=self.sess)[0]

        value = self.critic.model.predict(state.reshape(1, state.shape[0]))[0][0]

        self.prev_actions = actions_one_hot
        self.prev_state = state

        if self.episode == 0:
            self.prev_actions = actions_one_hot
            self.prev_state = state
            self.buffer = []
        else:
            self.buffer.append(
                [self.prev_state, self.prev_actions, game_state.reward, state, value, False])  # Add replay buffer

        self.episode += 1

        max_index = np.argmax(actions_one_hot)
        chosen_action = self.action_space[max_index]

        # FOR TESTING
        print('Probs:', action_probabilities)
        print('Chosen action:', chosen_action)
        print('Reward:', game_state.reward)

        if np.mod(self.episode, 30) == 0 and self.episode > 0:
            if self.train_indicator:
                print("Now we save the model")
                self.actor.model.save_weights("actormodel.h5", overwrite=True)
                with open("actormodel.json", "w") as outfile:
                    json.dump(self.actor.model.to_json(), outfile)

                self.critic.model.save_weights("criticmodel.h5", overwrite=True)
                with open("criticmodel.json", "w") as outfile:
                    json.dump(self.critic.model.to_json(), outfile)

        return chosen_action



    def probs_to_one_hot(self, probabilities):
        one_hot_tensor = []
        for prob in probabilities:
            a = tf.constant(prob)
            one_hot = tf.one_hot(tf.nn.top_k(a).indices, tf.shape(a)[0]).eval(session=self.sess)
            one_hot_tensor.append(one_hot[0])
        return np.array(one_hot_tensor)
