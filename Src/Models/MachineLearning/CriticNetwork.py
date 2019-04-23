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

HIDDEN1_UNITS = 16
HIDDEN2_UNITS = 32
HIDDEN3_UNITS = 200


class CriticNetwork(object):
    def __init__(self, sess, state_size, BATCH_SIZE, TAU, LEARNING_RATE, UPDATE_STEPS):
        self.sess = sess
        self.BATCH_SIZE = BATCH_SIZE
        self.TAU = TAU
        self.LEARNING_RATE = LEARNING_RATE
        self.UPDATE_STEPS = UPDATE_STEPS

        K.set_session(sess)

        # Now create the model
        self.model, self.state, self.output, self.weight = self.create_critic_network(state_size)

        self.model.compile(optimizer=Adam(lr=self.LEARNING_RATE), loss='mse')

    def train(self, states, target_critic):
        self.model.fit(states, target_critic, verbose=0)

    def target_train(self):
        critic_weights = self.model.get_weights()
        critic_target_weights = self.target_model.get_weights()
        for i in range(len(critic_weights)):
            critic_target_weights[i] = self.TAU * critic_weights[i] + \
                (1 - self.TAU) * critic_target_weights[i]
        self.target_model.set_weights(critic_target_weights)

    def create_critic_network(self, state_size):
        print("Now we build the model")
        S = Input(shape=[state_size])
        w1 = Dense(HIDDEN1_UNITS, activation='relu')(S)
        h1 = Dense(HIDDEN2_UNITS, activation='relu')(w1)
        V = Dense(1, activation='linear')(h1)
        model = Model(inputs=S, outputs=V)
        return model, S, V, model.trainable_weights
