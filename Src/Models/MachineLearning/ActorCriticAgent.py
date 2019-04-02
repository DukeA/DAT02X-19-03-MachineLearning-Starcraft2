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
    def __init__(self, action_dim, state_dim, action_space):
        self.train_indicator = True
        self.BUFFER_SIZE = 100000
        self.BATCH_SIZE = 32
        self.GAMMA = 0.9
        self.TAU = 0.1     #Target Network HyperParameters
        self.LRA = 0.0001    #Learning rate for Actor
        self.LRC = 0.001     #Lerning rate for Critic

        self.action_dim = action_dim
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
        self.action_space = action_space

        # Tensorflow GPU optimization
        self.config = tf.ConfigProto()
        self.config.gpu_options.allow_growth = True
        self.sess = tf.Session(config=self.config)
        from keras import backend as k
        k.set_session(self.sess)

        self.actor = ActorNetwork(self.sess, self.state_dim, self.action_dim, self.BATCH_SIZE, self.TAU, self.LRA)
        self.critic = CriticNetwork(self.sess, self.state_dim, self.action_dim, self.BATCH_SIZE, self.TAU, self.LRC)
        self.buff = ReplayBuffer(self.BUFFER_SIZE)    #Create replay buffer

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

        print("TORCS Experiment Start.")

    def predict(self, game_state, obs):

        state = np.hstack((game_state.minerals, game_state.vespene, obs.observation.player.food_workers, obs.observation.player.food_cap))

        loss = 0

        self.epsilon *= 0.99
        print("Epsilon: ", self.epsilon)

        r = random.random()

        if r < self.epsilon:
            action_probabilities = tf.one_hot([random.randint(0, self.action_dim-1)], self.action_dim).eval(session=self.sess)
        else:
            action_probabilities = self.actor.model.predict(state.reshape(1, state.shape[0]))

        print(action_probabilities)

        if self.episode == 0:
            self.prev_actions = action_probabilities
            self.prev_state = state

        else:
            self.buff.add(self.prev_state, self.prev_actions[0], game_state.reward, state, False)  # Add replay buffer

            self.prev_actions = action_probabilities
            self.prev_state = state

            # Do the batch update
            batch = self.buff.getBatch(self.BATCH_SIZE)
            states = np.asarray([e[0] for e in batch])
            actions = np.asarray([e[1] for e in batch])
            rewards = np.asarray([e[2] for e in batch])
            new_states = np.asarray([e[3] for e in batch])
            dones = np.asarray([e[4] for e in batch])
            y_t = np.asarray([e[1] for e in batch])

            target_q_values = self.critic.target_model.predict([new_states, self.actor.target_model.predict(new_states)])

            for k in range(len(batch)):
                if dones[k]:
                    y_t[k] = rewards[k]
                else:
                    y_t[k] = rewards[k] + self.GAMMA*target_q_values[k]

            if self.train_indicator:
                loss += self.critic.model.train_on_batch([states, actions], y_t)
                a_for_grad = self.actor.model.predict(states)
                grads = self.critic.gradients(states, a_for_grad)
                self.actor.train(states, grads)
                self.actor.target_train()
                self.critic.target_train()

            self.total_reward += game_state.reward

        self.episode += 1

        max_index = np.argmax(action_probabilities)

        chosen_action = self.action_space[max_index]

        # FOR TESTING
        print('Probs:', action_probabilities)
        print('Chosen action:', chosen_action)
        print('Reward:', game_state.reward)

        return chosen_action

        #if np.mod(self.episode, 3) == 0:
        #    if (self.train_indicator):
        #        print("Now we save the model")
         #       self.actor.model.save_weights("actormodel.h5", overwrite=True)
        ##            json.dump(self.actor.model.to_json(), outfile)
#
        #        self.critic.model.save_weights("criticmodel.h5", overwrite=True)
         #       with open("criticmodel.json", "w") as outfile:
         #           json.dump(self.critic.model.to_json(), outfile)

    def probs_to_one_hot(self, probabilities):
        one_hot_tensor = []
        for prob in probabilities:
            a = tf.constant(prob)
            one_hot = tf.one_hot(tf.nn.top_k(a).indices, tf.shape(a)[0]).eval(session=self.sess)
            one_hot_tensor.append(one_hot[0])
        return np.array(one_hot_tensor)
