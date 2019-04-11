import numpy as np
import math
from keras.initializers import normal, identity
from keras.models import model_from_json
from keras.models import Sequential, Model
#from keras.engine.training import collect_trainable_weights
from keras.layers import Dense, Flatten, Input, merge, Lambda, LSTM
from keras.optimizers import Adam
import tensorflow as tf
import keras.backend as K

HIDDEN1_UNITS = 150
HIDDEN2_UNITS = 300
LSTM_UNITS = 128

class ActorNetwork(object):
    def __init__(self, sess, state_size, action_size, BATCH_SIZE, TAU, LEARNING_RATE, UPDATE_STEPS):
        self.sess = sess
        self.BATCH_SIZE = BATCH_SIZE
        self.TAU = TAU
        self.LEARNING_RATE = LEARNING_RATE
        self.UPDATE_STEPS = UPDATE_STEPS

        K.set_session(sess)

        # Now create the model
        self.model, self.state, self.output, self.weights = self.create_actor_network(state_size, action_size)
        self.target_actor = tf.placeholder(tf.float32)

        loss2 = tf.reduce_sum(
            tf.nn.softmax_cross_entropy_with_logits_v2(logits=self.output,
                                                    labels=self.target_actor))
        self.optimize = tf.train.AdamOptimizer(self.LEARNING_RATE).minimize(loss2)

    def train(self, states, target_actor):
        self.sess.run(self.optimize, feed_dict={
            self.state: states,
            self.target_actor: target_actor
        })

    def target_train(self):
        actor_weights = self.model.get_weights()
        actor_target_weights = self.target_model.get_weights()
        for i in range(len(actor_weights)):
            actor_target_weights[i] = self.TAU * actor_weights[i] + (1 - self.TAU)* actor_target_weights[i]
        self.target_model.set_weights(actor_target_weights)

    def create_actor_network(self, state_size, action_dim):
        if isinstance(state_size, int):
            print("Now we build the model")
            S = Input(shape=[state_size])
            h0 = Dense(HIDDEN1_UNITS, activation='relu', kernel_initializer='random_normal')(S)
            h1 = Dense(HIDDEN2_UNITS, activation='relu', kernel_initializer='random_normal')(h0)
            V = Dense(action_dim, activation='linear', kernel_initializer='random_normal')(h1)
            model = Model(inputs=S, outputs=V)
            return model, S, V, model.trainable_weights
        else:
            # Presumably we're here because it's LSTM.
            S = Input(shape=state_size)
            x = LSTM(LSTM_UNITS, return_sequences=True, kernel_initializer='random_normal')(S)
            x = LSTM(LSTM_UNITS, return_sequences=False, kernel_initializer='random_normal')(x)
            V = Dense(action_dim, activation='linear', kernel_initializer='random_normal')(x)
            model = Model(inputs=S, outputs=V)
            return model, S, V, model.trainable_weights
