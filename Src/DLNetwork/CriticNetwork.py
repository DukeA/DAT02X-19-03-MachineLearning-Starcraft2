from keras import models, layers, optimizers
import keras.backend as K
import tensorflow as tf


class CriticNetwork(object):
    def __init__(self, sess, state_size, action_len, BATCH_SIZE, TAU, LEARNING_RATE):
        self.sess = sess
        self.BATCH_SIZE = BATCH_SIZE
        self.TAU = TAU
        self.LEARNING_RATE = LEARNING_RATE
        self.action_len = action_len

        K.set_session(sess)

        self.model, self.action, self.state = self.create_critic_network(state_size, action_len)
        self.target_model, self.target_action, self.target_state = self.create_critic_network(state_size, action_len)
        self.action_grad = tf.gradients(self.model.output, self.action)
        self.sess.run(tf.initialize_all_variables())

    def gradients(self, states, actions):
        return self.sess.run(self.action_grad, feed_dict={
            self.state: states,
            self.action: actions
        })

    def target_train(self):
        critic_weights = self.model.get_weights()
        critic_target_weights = self.target_model.get_weights()
        for i in range(len(critic_weights)):
            critic_target_weights[i] = self.TAU * critic_weights[i] + (1 - self.TAU) * critic_target_weights[i]
        self.target_model.set_weights(critic_target_weights)

    def create_critic_network(self, state_size, action_len):
        state_input = layers.Input(shape=state_size)
        action_input = layers.Input(shape=[action_len])
        # state_size should be (time_steps, #of_state_parameters)
        s1 = layers.LSTM(100, return_sequences=False)(state_input)
        s2 = layers.Dense(50, activation='relu')(s1)
        s3 = layers.Dense(50, activation='linear')(s2)
        a1 = layers.Dense(50, activation='linear')(action_input)

        m1 = layers.Add()([s3, a1])
        m2 = layers.Dense(50, activation='relu')(m1)
        out = layers.Dense(action_len, activation='softmax')(m2)
        model = models.Model(input=[state_input, action_input], output=out)
        adam = optimizers.Adam(lr=self.LEARNING_RATE)
        model.compile(loss='categorical_crossentropy', optimizer=adam)

        # network = models.Sequential()
        # network.add(layers.concatenate([s2, a1]))
        # network.add(layers.Dense(32, activation='relu'))
        # network.add(layers.Dense(action_len, activation='softmax'))
        # network.compile(loss='categorical_crossentropy',
        #                optimizer='adam',
        #                metrics=['accuracy'])
        return model, action_input, state_input
