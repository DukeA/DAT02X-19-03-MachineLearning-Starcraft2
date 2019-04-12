import random
import numpy as np
from collections import deque

import tensorflow as tf
from keras import backend
from werkzeug.wrappers import json

from Models.BuildNetwork.Build_Actor import Build_Actor
from Models.BuildNetwork.Build_Critic_Actor import Build_Critic_Actor


class BuildNetwork:

    def __init__(self, build_state, action_state):
        self.Batch_Size = 32
        self.Buffer_size = 10000
        self.lerarning_rate = 0.0001
        self.epsilon = 1.0
        self.gamma = 0.9
        self.epsilon_decay = 0.99
        self.tau = 0.125

        self.build_state = build_state
        self.action_state = action_state
        self.action_space = len(self.action_state)

        self.action_Explored = 10000
        self.episode_count = 2000
        self.max_steps = 1000
        self.reward = 0
        self.done = False
        self.step = 0
        self.indicator = 0
        self.episode = 0
        self.NUM_STEPS_UNTIL_UPDATE = 10

        self.config = tf.ConfigProto()
        self.config.gpu_options.allow_growth = True
        self.sess = tf.Session(config=self.config)
        backend.set_session(self.sess)

        self.build_actor = Build_Actor()
        self.crtic_build_Actor = Build_Critic_Actor()

        self.total_reward = 0
        self.prev_state = None
        self.prev_actions = None
        self.memory_Buffer = deque(maxlen=4000)

        self.actions_softmax = tf.nn.softmax(self.build_actor.build_author_output[0])

        self.sess.run(tf.global_variables_initializer())

        print("Trying to find the loadweights")
        if isinstance(self.action_space, int):
            try:
                self.load_weights("")
            except:
                print("Could load the files")
        else:
            try:
                self.load_weights("")
            except:
                print("Cannot find the weight")

    def predict_neural_network(self, build_Current_state, action_state):
        if isinstance(self.build_state, int):
            state, old_score, map = build_Current_state
        else:
            state,old_score,map =  build_Current_state

        if random.random() < self.epsilon:
            action_probs =[1/self.action_space]*self.action_space
        else:
            action_probs = self.sess.run(self.actions_softmax, feed_dict={
                self.build_actor: state
            })
        action_index = np.random.choice(range(self.action_space),1,p = action_probs)[0]
        if  self.episode > 0:
            self.memory_Buffer.append([self.prev_state[0],self.prev_actions,build_Current_state
                                      state[0],False])
        self.prev_actions = action_index
        self.prev_state = state
        self.episode +=

        chosen_action = self.action_space[action_index]
        if len((self.memory_Buffer)> self.Batch_Size):
            traning_batch = random.sample(self.memory_Buffer,self.Batch_Size)
            self.train_neural_network(self,traning_batch)

        if np.mod (self.episode, 30) ==0  and self.episode > 0:
            if self.train_indicaor:
                if isinstance(self.build_state, int):
                    self.build_actor.model.save_weights("Models/MachineLearning/actormodel.h5", overwrite=True)
                    with open("Models/MachineLearning/actormodel.json", "w") as outfile:
                        json.dump(self.actor.model.to_json(), outfile)

                    self.critic.model.save_weights("criticmodel.h5", overwrite=True)
                    with open("criticmodel.json", "w") as outfile:
                        json.dump(self.critic.model.to_json(), outfile)
        return chosen_action

    def train_neural_network(self, traning_batch):
        states = np.asarray([row[0] for row in traning_batch])
        actions = np.asarray([row[1]for row in traning_batch])
        rewards = np.asarray([row[2]for row in traning_batch])
        next_states = np.asarray([row[3] for row in traning_batch])
        dones = np.asarray([row[4]for row in traning_batch])

        next_states_value = self.crtic_build_Actor
        state_values = next_states_value
        predicted_state_valies = self.crtic_build_Actor
        target_actor = np.zeros((len(predicted_state_valies),self))

        for idx, reward in enumerate(rewards):
            if dones[idx]:
                state_values[idx] = reward
                target_actor[idx][actions[idx]] = reward - predicted_state_valies[idx]
            else:
                state_values[idx] = reward + self.gamma *next_states_value[idx]
                target_actor[idx][actions[idx]] = reward +self.gamma *  next_state_values[idx] \
                                                  - predicted_state_values[idx]



    def probs_to_one_hot(self,probabilites):
        one_hot_tensor =[]
        for prob in probabilites:
            a = tf.

    def update_weights(self):
        self.build_actor.update_athor_values(self)
        self.crtic_build_Actor.update_crtic_weights(self)

    def load_weights(self, path):
        list = []
        list.append(self.build_actor.load_weights(self, path))
        list.append(self.crtic_build_Actor.load_weights(self, path))
        return list

    def save_weights(self, path):
        list =[]
        list.append(self.build_actor.save_weights(self, path))
        list.append(self.crtic_build_Actor.save_weights(self, path))
        return list