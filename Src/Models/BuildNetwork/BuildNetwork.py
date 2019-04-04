import numpy as np
import tensorflow as tf
import keras.backend as backend
from keras import Input, Model
from keras.layers import Dense, add
from tflearn import Adam


class BuildNetwork:
    def __init__(self, sess, build_size, action_size, batch_size, tau, learning_rate):
        self.sess = sess
        self.build_size = build_size
        self.action_size = action_size
        self.batch_size = batch_size
        self.tau = tau
        self.learning_rate = learning_rate

        backend.set_session(sess)

        self.model, self.action, self.state = self.create_buildnetwork(self, build_size, action_size)
        self.target_model, self.target_action, self.target_state = self.create_buildnetwork(build_size, action_size)
        self.gradients = tf.gradients(self.model.output, self.action)
        self.sess.run(tf.initialize_all_variables())

    def gradients(self, states, actions):
        return self.sess.run(self.action_grads, feed_dict={
            self.state: states,
            self.action: actions
        })

    def train_network(self):
        critic_weights = self.model.getWeights()
        critic_target_weights = self.target_model.getweights()
        for i in range(len(critic_weights)):
            critic_target_weights[i] = self.tau* critic_weights[i]+(1-self.tau)*critic_target_weights[i]
        self.target_model.setWeights(critic_target_weights)

    def create_crtic_network(self, build_size,action_size):
        Build_Model = Input(shape =[build_size])
        Action_model = Input(shape=[action_size])
        conv1 = Dense(300,activation='relu')(Build_Model)
        conv2 = Dense(600,activation='linear')(conv1)
        hidden_1 = Dense(600,activation='linear')(conv2)
        hidden_2 = add([hidden_1,conv1])
        hidden_3 = Dense(600,activation='relu')(hidden_2)
        Model_output = Dense(action_size,activation='linear')(hidden_3)
        model = Model(input=[Build_Model,Action_model],output=Model_output)
        adam = Adam(lr =self.learning_rate)
        model.compile(loss='mse', optimizer=adam)
        return  model,Action_model,Build_Model


