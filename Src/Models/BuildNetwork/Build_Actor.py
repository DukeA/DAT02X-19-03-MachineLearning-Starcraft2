from keras.layers import Dense, Input
from keras.models import Model
import keras.backend as backend
import tensorflow as tf
from keras.optimizers import Adam


class Build_Actor:
    def __init__(self, sess,build_reward, build_model, action_szie, learning_rate, batch_size, tau):
        self.sess = sess
        self.build_reward = build_reward
        self.build_model = build_model
        self.action_size = action_szie
        self.learning_rate = learning_rate
        self.batch_size = batch_size
        self.Tau = tau
        backend.set_session(sess)
        value = self.build_model[0]
        self.build_actor_model, self.build_actor_state, \
        self.build_actor_output, self.build_actor_weights = Build_Actor.create_actor_model(self, self.build_reward,
                                                                                             self.action_size)
        self.target_build_actor = tf.placeholder(tf.float32)
        self.build_actor_optimizer = Adam(lr=self.learning_rate)
        self.build_actor_model.compile(optimizer=self.build_actor_optimizer, loss='mse')

    def create_actor_model(self, build_model, action_state):
        value = (len(build_model),)
        build_model_state = Input(shape=value)
        hidden_layer1 = Dense(32, activation='relu', kernel_initializer='random_normal')(build_model_state)
        hidden_layer2 = Dense(16, activation='relu', kernel_initializer='random_normal')(hidden_layer1)
        build_action_state = Dense(action_state, activation='linear', kernel_initializer='random_normal')(hidden_layer2)
        build_actor_model = Model(input=build_model_state, output=build_action_state)
        return build_actor_model, build_model_state, \
               build_action_state, build_actor_model.trainable_weights

    def train_author(self, build_state, action_state):
        self.sess.run(self.build_actor_optimizer, feed_dict={
            self.build_actor_model: build_state,
            self.build_actor_state: action_state
        })

    def update_author_values(self):
        build_author_weights = self.build_actor_model.get_weights()
        build_target_weights = self.target_build_actor.getWeights()
        for i in range(len(build_author_weights)):
            build_target_weights[i] = self.Tau * build_target_weights[i] + (1 - self.Tau) * build_target_weights[i]
        self.target_build_actor.set_weights(build_target_weights)

    def load_weights(self, path):
        self.build_actor_model.load_weights(path)

    def save_weights(self, path):
        self.build_actor_model.save_weights(path + 'build_actor.h5')
