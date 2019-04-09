import numpy as np
import tensorflow as tf

from keras import Input, Model
from keras.layers import Dense, Concatenate
from keras.optimizers import Adam


class Critic:

    def __init__(self, state_dim, action_dim, learning_rate, TAU):

        self.TAU = TAU

        self.state, self.output, self.model, self.weights = \
            self.create_new_network(state_dim, action_dim, 24, 24)
        self.target_state, self.target_output, self.target_model, self.target_weights = \
            self.create_new_network(state_dim, action_dim, 24, 24)

        self.model.compile(optimizer=Adam(lr=learning_rate), loss='mse')

    def train(self, states, correct_q_values):
        self.model.fit(states, correct_q_values, verbose=0)

    def target_train(self):
        weights = self.model.get_weights()
        target_weights = self.target_model.get_weights()
        for i in range(len(weights)):
            target_weights[i] = self.TAU * weights[i] + (1 - self.TAU) * target_weights[i]
        self.target_model.set_weights(target_weights)

    def create_new_network(self, state_dim, action_dim, hidden_size_1, hidden_size_2):

        i = Input(shape=[state_dim])
        h1 = Dense(hidden_size_1, activation='relu', kernel_initializer='truncated_normal')(i)
        #h2 = Dense(hidden_size_2, activation='relu', kernel_initializer='truncated_normal')(h1)
        o = Dense(action_dim, activation='linear', kernel_initializer='truncated_normal')(h1)

        model = Model(inputs=i, outputs=o)

        return i, o, model, model.trainable_weights
