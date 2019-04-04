import numpy as np
import math
from keras.initializers import normal, identity
from keras.models import model_from_json
from keras.models import Sequential, Model
#from keras.engine.training import collect_trainable_weights
from keras.layers import Dense, Flatten, Input, merge, Lambda
from keras.optimizers import Adam
import tensorflow as tf
import keras.backend as K

HIDDEN1_UNITS = 150
HIDDEN2_UNITS = 300

class ActorNetwork(object):
    def __init__(self, sess, state_size, action_size, BATCH_SIZE, TAU, LEARNING_RATE, UPDATE_STEPS):
        self.sess = sess
        self.BATCH_SIZE = BATCH_SIZE
        self.TAU = TAU
        self.LEARNING_RATE = LEARNING_RATE
        self.UPDATE_STEPS = UPDATE_STEPS

        K.set_session(sess)

        # Now create the model
        self.model, self.weights, self.state = self.create_actor_network(state_size, action_size)
        self.target_model, self.target_weights, self.target_state = self.create_actor_network(state_size, action_size)
        self.action_one_hot = tf.placeholder(tf.float32, [None, action_size])
        self.discounted_values = tf.placeholder(tf.float32, [UPDATE_STEPS, ])

        negative_likelihoods = tf.nn.softmax_cross_entropy_with_logits_v2(labels=self.action_one_hot, logits=self.model.output)
        weighted_negative_likelihoods = tf.multiply(negative_likelihoods, self.discounted_values)
        loss = tf.reduce_mean(weighted_negative_likelihoods)

        self.params_grad = tf.gradients(loss, self.weights)
        grads = zip(self.params_grad, self.weights)
        self.optimize = tf.train.AdamOptimizer(LEARNING_RATE).apply_gradients(grads)

        self.sess.run(tf.global_variables_initializer())

    def train(self, states, action_one_hots, discounted_values):
        self.sess.run(self.optimize, feed_dict={
            self.state: states,
            self.action_one_hot: action_one_hots,
            self.discounted_values: discounted_values
        })

    def target_train(self):
        actor_weights = self.model.get_weights()
        actor_target_weights = self.target_model.get_weights()
        for i in range(len(actor_weights)):
            actor_target_weights[i] = self.TAU * actor_weights[i] + (1 - self.TAU)* actor_target_weights[i]
        self.target_model.set_weights(actor_target_weights)

    def create_actor_network(self, state_size, action_dim):
        print("Now we build the model")
        S = Input(shape=[state_size])   
        h0 = Dense(HIDDEN1_UNITS, activation='relu', kernel_initializer='random_normal')(S)
        h1 = Dense(HIDDEN2_UNITS, activation='relu', kernel_initializer='random_normal')(h0)
        V = Dense(action_dim, activation='relu', kernel_initializer='random_normal')(h1)
        model = Model(inputs=S, outputs=V)
        return model, model.trainable_weights, S

