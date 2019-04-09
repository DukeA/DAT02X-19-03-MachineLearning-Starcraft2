import numpy as np
import tensorflow as tf
import random

from keras import Input, Model
from keras.layers import Dense, Concatenate
from keras.optimizers import Adam
from actor import Actor
from critic import Critic


class A3CAgent:

    def __init__(self, state_dim, action_dim, action_space, discount_factor):

        self.config = tf.ConfigProto()
        self.config.gpu_options.allow_growth = True
        self.sess = tf.Session(config=self.config)
        from keras import backend as k
        k.set_session(self.sess)

        self.actor_learning_rate = 0.001 # 0.0001 fungerade bäst hittills, med Q-värden som gradient-vikt
        self.critic_learning_rate = 0.001
        self.TAU = 0.01

        self.action_space = action_space
        self.action_dim = action_dim
        self.discount_factor = discount_factor

        self.actor = Actor(self.sess, state_dim, action_dim, self.actor_learning_rate, self.TAU)
        self.critic = Critic(state_dim, 1, self.critic_learning_rate, self.TAU)

        #self.correct_q_values = tf.placeholder(tf.float32)

        #loss = tf.reduce_sum(tf.squared_difference(self.correct_q_values, self.model.output))

        # gradients = tf.gradients(loss, self.weights)
        # grads = zip(gradients, self.weights)
        #self.optimize = tf.train.AdamOptimizer(learning_rate=self.learning_rate).minimize(loss, var_list=self.weights)

        self.actions_softmax = tf.nn.softmax(self.actor.model.output[0])

        self.sess.run(tf.global_variables_initializer())

    def predict_action(self, state):
        state = np.array([state])
        action_probs = self.sess.run(self.actions_softmax, feed_dict={
            self.actor.state: state
        })
        return np.random.choice([0, 1], 1, p=action_probs)[0]

    def train(self, training_batch):
        states = np.asarray([row[0] for row in training_batch])
        actions = np.asarray([row[1] for row in training_batch])
        rewards = np.asarray([row[2] for row in training_batch])
        next_states = np.asarray([row[3] for row in training_batch])
        dones = np.asarray([row[4] for row in training_batch])

                #state_values = self.critic.model.predict(states)

        next_state_values = self.critic.model.predict(next_states)
        state_values = next_state_values

        predicted_state_values = self.critic.model.predict(states)
        target_actor = np.zeros((len(predicted_state_values), 2))

        for idx, reward in enumerate(rewards):
            if dones[idx]:
                state_values[idx] = reward
                target_actor[idx][actions[idx]] = reward - predicted_state_values[idx]
            else:
                state_values[idx] = reward + self.discount_factor * next_state_values[idx]
                target_actor[idx][actions[idx]] = reward + self.discount_factor * next_state_values[idx] - predicted_state_values[idx]



        #advantages = [state_val[0] - predicted_state_values[idx][0] for idx, state_val in enumerate(state_values)]

                #action_probs = tf.nn.softmax(self.actor.model.predict(states)).eval(session=self.sess)
                #action_probs = self.actor.model.predict(states)

                #chosen_actions = np.asarray([np.argmax(action_prob_row) for action_prob_row in action_probs])
        #action_one_hots = tf.one_hot(actions, self.action_dim).eval(session=self.sess)
                # q_values = np.asarray([q_values[actions[idx]] for idx, q_values in enumerate(state_values)])
                #advantages = np.asarray([q_values[actions[idx]] - np.dot(q_values, action_probs[idx]) for idx, q_values in enumerate(state_q_values)])

        self.actor.train(states, target_actor)

        self.critic.train(states, state_values)

        #self.sess.run(self.optimize, feed_dict={
        #    self.correct_q_values: state_q_values,
        #    self.state: states
        #})

        #self.actor.target_train()
        #self.critic.target_train()


