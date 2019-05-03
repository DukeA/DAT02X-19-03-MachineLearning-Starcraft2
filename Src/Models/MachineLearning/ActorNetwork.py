from keras.layers import Dense, Input
from keras.models import Model
import tensorflow as tf
import keras.backend as K


HIDDEN1_UNITS = 64
HIDDEN2_UNITS = 128


class ActorNetwork(object):
    def __init__(self, sess, state_size, action_size, BATCH_SIZE, TAU, LEARNING_RATE):
        self.sess = sess
        self.BATCH_SIZE = BATCH_SIZE
        self.TAU = TAU
        self.LEARNING_RATE = LEARNING_RATE
        self.ENTROPY_WEIGHT = 1e-5
        self.IMITATION_WEIGHT = 0.1
        self.AMPLIFIER = 1e2

        K.set_session(sess)

        # Now create the model
        self.model, self.state, self.output, self.weights = self.create_actor_network(
            state_size, action_size)

        self.model_policy = self.model.output
        self.softmax_policy = tf.nn.softmax(self.model_policy)

        self.action_one_hot = tf.placeholder(dtype=tf.float32)
        self.advantages = tf.placeholder(dtype=tf.float32)
        self.imitation_weight = tf.placeholder(dtype=tf.float32)
        self.imitation_actions = tf.placeholder(dtype=tf.float32)

        negative_likelihoods = tf.nn.softmax_cross_entropy_with_logits_v2(
            labels=self.action_one_hot, logits=self.model_policy)
        weighted_negative_likelihoods = tf.multiply(negative_likelihoods, self.advantages)

        self.policy_loss = tf.reduce_mean(weighted_negative_likelihoods)

        self.entropy_loss = - tf.reduce_sum(self.softmax_policy *
                                            tf.log(self.softmax_policy+10**-15))

        self.imitation_loss = tf.reduce_mean(tf.losses.softmax_cross_entropy(
            logits=self.model_policy, onehot_labels=self.imitation_actions))

        total_loss = (self.policy_loss * self.AMPLIFIER - self.entropy_loss * self.ENTROPY_WEIGHT) * (1 - self.imitation_weight) + \
                     self.imitation_loss * self.imitation_weight

        optimizer = tf.train.RMSPropOptimizer(learning_rate=self.LEARNING_RATE)
        self.gradients = optimizer.compute_gradients(total_loss)
        capped_gvs = [(self.ClipIfNotNone(grad), var) for grad, var in self.gradients]
        self.optimize = optimizer.apply_gradients(capped_gvs)

        self.sess.run(tf.global_variables_initializer())

    def train(self, states, action_one_hot, advantages, imitation_actions):

        imitation_weight = self.IMITATION_WEIGHT

        self.sess.run(self.optimize, feed_dict={
            self.state: states,
            self.action_one_hot: action_one_hot,
            self.advantages: advantages,
            self.imitation_actions: imitation_actions,
            self.imitation_weight: imitation_weight
        })

        policy_loss = self.sess.run(self.policy_loss, feed_dict={
            self.state: states,
            self.action_one_hot: action_one_hot,
            self.advantages: advantages
        })
        print("Weighted policy loss", policy_loss * self.AMPLIFIER * (1 - imitation_weight))
        entropy_loss = self.sess.run(self.entropy_loss, feed_dict={
            self.state: states,
        })
        print("Weighted entropy loss", entropy_loss * self.ENTROPY_WEIGHT * (1 - imitation_weight))
        imitation_loss = self.sess.run(self.imitation_loss, feed_dict={
            self.state: states,
            self.imitation_actions: imitation_actions
        })
        print("Weighted imitation loss", imitation_loss * imitation_weight)

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
        print("Building Actor model")
        S = Input(shape=[state_size])
        x = Dense(32, activation='relu', kernel_initializer='random_normal')(S)
        x = Dense(32, activation='relu', kernel_initializer='random_normal')(x)
        x = Dense(16, activation='relu', kernel_initializer='random_normal')(x)
        V = Dense(action_dim, activation='linear', kernel_initializer='random_normal')(x)
        model = Model(inputs=S, outputs=V)
        return model, S, V, model.trainable_weights
