import numpy as np
import tensorflow as tf

from keras import Input, Model
from keras.layers import Dense, Concatenate
from keras.optimizers import Adam


class Actor:

    def __init__(self, sess, state_dim, action_dim, learning_rate, TAU):

        self.sess = sess
        self.TAU = TAU

        self.state, self.output, self.model, self.weights = \
            self.create_new_network(state_dim, action_dim, 200, 200)
        self.target_state, self.target_output, self.target_model, self.target_weights = \
            self.create_new_network(state_dim, action_dim, 200, 200)

        #self.action_one_hot = tf.placeholder(dtype=tf.float32)
        #self.discounted_values = tf.placeholder(dtype=tf.float32)
        self.target_actor = tf.placeholder(dtype=tf.float32)

        #negative_likelihoods = tf.nn.softmax_cross_entropy_with_logits_v2(labels=self.action_one_hot, logits=self.model.output)
        #weighted_negative_likelihoods = tf.multiply(negative_likelihoods, self.discounted_values)
        #loss = tf.reduce_mean(weighted_negative_likelihoods)
        #gradient = tf.gradients(loss, self.weights)
        #grad = zip(gradient, self.weights)

        #self.optimize = tf.train.AdamOptimizer(learning_rate=learning_rate).apply_gradients(grad)

        loss2 = tf.reduce_sum(
            tf.nn.softmax_cross_entropy_with_logits_v2(logits=self.output,
                                                    labels=self.target_actor))
        self.optimize = tf.train.AdamOptimizer(learning_rate).minimize(loss2)

        self.sess.run(tf.global_variables_initializer())

    def train(self, states, target_actor): #, action_one_hot, discounted_values):
        self.sess.run(self.optimize, feed_dict={
            self.state: states,
            self.target_actor: target_actor
            #self.action_one_hot: action_one_hot,
            #self.discounted_values: discounted_values
        })

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
