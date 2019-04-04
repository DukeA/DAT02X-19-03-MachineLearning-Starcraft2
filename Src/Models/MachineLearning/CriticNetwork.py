import numpy as np
import math
from keras.initializers import normal, identity
from keras.models import model_from_json, load_model
#from keras.engine.training import collect_trainable_weights
from keras.models import Sequential
from keras.layers import Dense, Flatten, Input, merge, Lambda, Activation, add
from keras.models import Sequential, Model
from keras.optimizers import Adam
import keras.backend as K
import tensorflow as tf

HIDDEN1_UNITS = 150
HIDDEN2_UNITS = 300

class CriticNetwork(object):
    def __init__(self, sess, state_size, BATCH_SIZE, TAU, LEARNING_RATE, UPDATE_STEPS):
        self.sess = sess
        self.BATCH_SIZE = BATCH_SIZE
        self.TAU = TAU
        self.LEARNING_RATE = LEARNING_RATE
        self.UPDATE_STEPS = UPDATE_STEPS

        K.set_session(sess)

        # Now create the model
        self.model, self.weights, self.state = self.create_critic_network(state_size)
        self.target_model, self.target_weights, self.target_state = self.create_critic_network(state_size)

        self.discounted_rewards = tf.placeholder(tf.float32, [UPDATE_STEPS, ])
        squared_difference = tf.reduce_sum(tf.math.squared_difference(tf.cast(self.discounted_rewards, tf.float32), self.model.output))

        self.params_grad = tf.gradients(squared_difference, self.weights)
        grads = zip(self.params_grad, self.weights)
        self.optimize = tf.train.AdamOptimizer(LEARNING_RATE).apply_gradients(grads)

        self.sess.run(tf.global_variables_initializer())

    def train(self, states, discounted_rewards):
        self.sess.run(self.optimize, feed_dict={
            self.state: states,
            self.discounted_rewards: discounted_rewards
        })

    def target_train(self):
        critic_weights = self.model.get_weights()
        critic_target_weights = self.target_model.get_weights()
        for i in range(len(critic_weights)):
            critic_target_weights[i] = self.TAU * critic_weights[i] + (1 - self.TAU) * critic_target_weights[i]
        self.target_model.set_weights(critic_target_weights)

    def create_critic_network(self, state_size):
        print("Now we build the model")
        S = Input(shape=[state_size])
        w1 = Dense(HIDDEN1_UNITS, activation='relu')(S)
        h1 = Dense(HIDDEN2_UNITS, activation='relu')(w1)
        V = Dense(1, activation='linear')(h1)
        model = Model(inputs=S, outputs=V)
        adam = Adam(lr=self.LEARNING_RATE)
        model.compile(loss='mse', optimizer=adam)
        return model, model.trainable_weights, S
