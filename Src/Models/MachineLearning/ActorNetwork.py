import matplotlib.pyplot as plt
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


HIDDEN1_UNITS = 16
HIDDEN2_UNITS = 32
HIDDEN3_UNITS = 200


class ActorNetwork(object):
    def __init__(self, sess, state_size, action_size, BATCH_SIZE, TAU, LEARNING_RATE, UPDATE_STEPS):
        self.sess = sess
        self.BATCH_SIZE = BATCH_SIZE
        self.TAU = TAU
        self.LEARNING_RATE = LEARNING_RATE
        self.UPDATE_STEPS = UPDATE_STEPS
        self.ENTROPY_WEIGHT = 0.005
        self.IMITATION_WEIGHT = 100

        K.set_session(sess)

        # Now create the model
        self.model, self.state, self.output, self.weights = self.create_actor_network(
            state_size, action_size)

        self.model_policy = self.model.output
        self.softmax_policy = tf.nn.softmax(self.model_policy)

        self.action_one_hot = tf.placeholder(dtype=tf.float32)
        self.advantages = tf.placeholder(dtype=tf.float32)
        self.imitation_actions = tf.placeholder(dtype=tf.float32)

        negative_likelihoods = tf.nn.softmax_cross_entropy_with_logits_v2(
            labels=self.action_one_hot, logits=self.model_policy)
        weighted_negative_likelihoods = tf.multiply(negative_likelihoods, self.advantages)

        self.policy_loss = tf.reduce_mean(weighted_negative_likelihoods)

        self.entropy_loss = - tf.reduce_sum(self.softmax_policy * tf.log(self.softmax_policy))

        self.imitation_loss = tf.reduce_mean(tf.losses.mean_squared_error(self.softmax_policy, self.imitation_actions))

        total_loss = self.policy_loss - self.entropy_loss * self.ENTROPY_WEIGHT + self.imitation_loss * self.IMITATION_WEIGHT

        optimizer = tf.train.RMSPropOptimizer(learning_rate=self.LEARNING_RATE)
        self.gradients = optimizer.compute_gradients(total_loss)
        capped_gvs = [(self.ClipIfNotNone(grad), var) for grad, var in self.gradients]
        self.optimize = optimizer.apply_gradients(capped_gvs)

        self.num_avg = 50
        self.avg_policy_loss = 0
        self.avg_entropy_loss = 0

        self.predict_iter = 0
        self.plot_iter = 0
        #
        f, (ax1, ax2, ax3) = plt.subplots(3, 1, num=2)

        self.fig = f

        self.ax1 = ax1
        self.ax1.plot()
        self.ax1.set_title("Policy loss averaged over 50 values")

        self.ax2 = ax2
        self.ax2.plot()
        self.ax2.set_title("Weighted entropy loss averaged over 50 values")

        self.ax3 = ax3
        self.ax3.plot()
        self.ax3.set_title("Total loss averaged over 50 values")
        plt.subplots_adjust(hspace=0.5)

        self.sess.run(tf.global_variables_initializer())

    def train(self, states, action_one_hot, advantages, imitation_actions):
        # grads = self.sess.run(self.gradients, feed_dict={
        #    self.state: states,
        #    self.action_one_hot: action_one_hot,
        #    self.advantages: advantages
        # })
        self.sess.run(self.optimize, feed_dict={
            self.state: states,
            self.action_one_hot: action_one_hot,
            self.advantages: advantages,
            self.imitation_actions: imitation_actions
        })
        # test1 = self.sess.run(self.model_policy, feed_dict={
        #    self.state: states,
        # })
        # print(test1)
        # test = self.sess.run(self.softmax_policy, feed_dict={
        #    self.state: states,
        # })
        # print(test)
        policy_loss = self.sess.run(self.policy_loss, feed_dict={
            self.state: states,
            self.action_one_hot: action_one_hot,
            self.advantages: advantages
        })
        print("Policy loss", policy_loss)
        entropy_loss = self.sess.run(self.entropy_loss, feed_dict={
            self.state: states,
        })
        print("Total entropy loss", entropy_loss * self.ENTROPY_WEIGHT)
        imitation_loss = self.sess.run(self.imitation_loss, feed_dict={
            self.state: states,
            self.imitation_actions: imitation_actions
        })
        print("Total imitation loss", imitation_loss * self.IMITATION_WEIGHT)

        # self.avg_policy_loss += policy_loss
        # self.avg_entropy_loss += entropy_loss
        # if self.predict_iter >= self.num_avg:
        #     self.ax1.scatter(self.plot_iter, self.avg_policy_loss/self.num_avg, s=3, c='blue')
        #     self.ax2.scatter(self.plot_iter, self.avg_entropy_loss /
        #                      self.num_avg*self.ENTROPY_WEIGHT, s=3, c='blue')
        #     self.ax3.scatter(self.plot_iter, (self.avg_policy_loss +
        #                                       self.avg_entropy_loss*self.ENTROPY_WEIGHT)/self.num_avg, s=3, c='blue')
        #     self.fig.savefig("loss.png")
        #     self.avg_policy_loss = 0
        #     self.avg_entropy_loss = 0
        #     self.plot_iter += 1
        #     self.predict_iter = 0
        # self.predict_iter += 1
        #print("Plot iter: ", self.plot_iter)
        #print("Predict iter: ", self.predict_iter)

    def target_train(self):
        actor_weights = self.model.get_weights()
        actor_target_weights = self.target_model.get_weights()
        for i in range(len(actor_weights)):
            actor_target_weights[i] = self.TAU * actor_weights[i] + \
                (1 - self.TAU) * actor_target_weights[i]
        self.target_model.set_weights(actor_target_weights)

    def ClipIfNotNone(self, grad):
        if grad is None:
            return grad
        return tf.clip_by_value(grad, -1, 1)

    def create_actor_network(self, state_size, action_dim):
        print("Now we build the model")
        S = Input(shape=[state_size])
        h0 = Dense(HIDDEN1_UNITS, activation='relu', kernel_initializer='random_normal')(S)
        h1 = Dense(HIDDEN2_UNITS, activation='relu', kernel_initializer='random_normal')(h0)
        V = Dense(action_dim, activation='linear', kernel_initializer='random_normal')(h1)
        model = Model(inputs=S, outputs=V)
        return model, S, V, model.trainable_weights
