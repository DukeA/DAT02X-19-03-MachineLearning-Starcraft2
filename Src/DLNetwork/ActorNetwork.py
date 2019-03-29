from keras import models, layers, optimizers
import keras.backend as K
import tensorflow as tf


class ActorNetwork(object):
    def __init__(self, sess, state_size, action_len, BATCH_SIZE, TAU, LEARNING_RATE):
        self.sess = sess
        self.BATCH_SIZE = BATCH_SIZE
        self.TAU = TAU
        self.LEARNING_RATE = LEARNING_RATE

        K.set_session(sess)

        self.model, self.weights, self.state = self.create_actor_network(state_size, action_len)
        self.target_model, self.target_weights, self.target_state = self.create_actor_network(state_size, action_len)
        self.action_gradient = tf.placeholder(tf.float32, [None, action_len])
        self.params_grad = tf.gradients(self.model.output, self.weights, -self.action_gradient)
        grads = zip(self.params_grad, self.weights)
        self.optimize = tf.train.AdamOptimizer(LEARNING_RATE).apply_gradients(grads)
        self.sess.run(tf.initialize_all_variables())

    def train(self, states, action_grads):
        self.sess.run(self.optimize, feed_dict={
            self.state: states,
            self.action_gradient: action_grads
        })

    def target_train(self):
        actor_weights = self.model.get_weights()
        actor_target_weights = self.target_model.get_weights()
        for i in range(len(actor_weights)):
            actor_target_weights[i] = self.TAU * actor_weights[i] + (1 - self.TAU) * actor_target_weights[i]
        self.target_model.set_weights(actor_target_weights)

    def create_actor_network(self, state_size, action_len):
        state_input = layers.Input(shape=state_size)
        # state_size should be (time_steps, #of_state_parameters)
        s1 = layers.LSTM(100, return_sequences=False)(state_input)
        s2 = layers.Dense(50, activation='relu')(s1)
        out = layers.Dense(action_len, activation='softmax')(s2)
        model = models.Model(input=[state_input], output=out)

        model.compile(loss='categorical_crossentropy',
                      optimizer='adam',
                      metrics=['accuracy'])
        return model, model.trainable_weights, state_input
