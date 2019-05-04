import numpy as np
import random
import tensorflow as tf
import json

from Models.MachineLearning.ActorNetwork import ActorNetwork
from Models.MachineLearning.CriticNetwork import CriticNetwork

from collections import deque


class ActorCriticAgent:
    def __init__(self, state_dim, action_space, epsilon):

        ############### Hyperparameters #################

        self.train_indicator = True
        self.BATCH_SIZE = 64
        self.GAMMA = 0.9995
        self.TAU = 0.1  # Target Network HyperParameters
        self.LRA = 0.00001  # Learning rate for Actor
        self.LRC = 0.00001  # Learning rate for Critic

        self.buffer = deque(maxlen=10000)
        self.good_buffer = deque(maxlen=8000)
        self.GOOD_GAME = False
        self.buffer_epsilon = 0
        self.buffer_epsilon_decay = 1
        self.buffer_epsilon_min = 0.0

        ################ Other stuff #####################

        self.action_space = action_space
        self.action_dim = len(self.action_space)
        self.state_dim = state_dim

        np.random.seed(1337)

        self.epsilon = epsilon
        self.episode = 0

        # Tensorflow GPU optimization
        self.config = tf.ConfigProto()
        self.config.gpu_options.allow_growth = True
        self.sess = tf.Session(config=self.config)
        from keras import backend as k
        k.set_session(self.sess)

        self.actor = ActorNetwork(self.sess, self.state_dim, self.action_dim,
                                  self.BATCH_SIZE, self.TAU, self.LRA)
        self.critic = CriticNetwork(self.sess, self.state_dim, self.BATCH_SIZE,
                                    self.TAU, self.LRC)

        self.actions = tf.placeholder(tf.int32)
        self.action_one_hot = tf.one_hot(self.actions, self.action_dim)

        self.total_reward = 0
        self.prev_state = None
        self.prev_actions = None

        self.actions_softmax = tf.nn.softmax(self.actor.model.output[0])

        self.sess.run(tf.global_variables_initializer())

        self.build_order = ["scv", "scv", "supply", "scv", "scv", "barracks", "scv", "barracks", "scv",
                            "barracks", "scv", "supply", "scv", "barracks", "barracks", "scv", "barracks", "scv", "supply"]
        self.build_index = 0
        # Now load the weight
        try:
            self.actor.model.load_weights("actormodel.h5")
            self.critic.model.load_weights("criticmodel.h5")
            print("Weights loaded successfully")
        except IOError:
            print("Could not find weights")

    def predict(self, game_state, obs):
        state, oldscore, map = game_state.get_state_now(obs)
        if self.GOOD_GAME:
            action_probs = self.help_policy(state)[0]
        else:
            action_probs = self.sess.run(self.actions_softmax, feed_dict={
                self.actor.state: state
            })

        action_index = np.random.choice(range(self.action_dim), 1, p=action_probs)[0]

        if self.GOOD_GAME and self.episode > 0:
            self.good_buffer.append([self.prev_state[0], self.prev_actions,
                                     0, state[0], False])

        elif self.episode > 0:
            self.buffer.append(
                [self.prev_state[0], self.prev_actions, 0, state[0], False])  # Add replay

        self.total_reward += game_state.reward
        self.prev_actions = action_index
        self.prev_state = state
        self.episode += 1

        chosen_action = self.action_space[action_index]

        print("No_op: " + '%.3e' % action_probs[0] +
              ".  SCV: " + '%.3e' % action_probs[1] +
              ".  Supply: " + '%.3e' % action_probs[2] +
              ".  Marine: " + '%.3e' % action_probs[3] +
              ".  Rax: " + '%.3e' % action_probs[4] +
              ".  Mine: " + '%.3e' % action_probs[5] +
              ".  Attack: " + '%.3e' % action_probs[6])
        print("Chosen action: ", chosen_action)
        print("Help policy action: ", self.action_space[np.argmax(self.help_policy(state))])

        if chosen_action == "attack":
            game_state.units_attacked = obs.observation.player.army_count/200
            game_state.last_attacked = state[0][-1]
        if(len(self.buffer) > self.BATCH_SIZE):
            if self.buffer_epsilon > random.random():
                training_batch = random.sample(self.good_buffer, self.BATCH_SIZE)
                self.train(training_batch, imitate=True)
            else:
                training_batch = random.sample(self.buffer, self.BATCH_SIZE)
            self.train(training_batch, imitate=False)

        # FOR TESTING
        if np.mod(self.episode, 30) == 0 and self.episode > 0:
            if self.train_indicator:
                self.actor.model.save_weights("actormodel.h5", overwrite=True)
                with open("actormodel.json", "w") as outfile:
                    json.dump(self.actor.model.to_json(), outfile)

                self.critic.model.save_weights("criticmodel.h5", overwrite=True)
                with open("criticmodel.json", "w") as outfile:
                    json.dump(self.critic.model.to_json(), outfile)

        return chosen_action

    def train(self, training_batch, imitate):
        states = np.asarray([row[0] for row in training_batch])
        actions = np.asarray([row[1] for row in training_batch])
        rewards = np.asarray([row[2] for row in training_batch])
        next_states = np.asarray([row[3] for row in training_batch])
        dones = np.asarray([row[4] for row in training_batch])

        next_state_values = self.critic.model.predict(next_states)
        state_values = next_state_values

        predicted_state_values = self.critic.model.predict(states)

        for idx, reward in enumerate(rewards):
            if dones[idx]:
                state_values[idx] = reward
            else:
                state_values[idx] = reward + self.GAMMA * next_state_values[idx]

        advantages = [state_val[0] - predicted_state_values[idx][0]
                      for idx, state_val in enumerate(state_values)]

        action_one_hots = self.sess.run(self.action_one_hot, feed_dict={
            self.actions: actions
        })

        imitation_actions = self.help_policy_2(states)

        self.actor.train(states, action_one_hots, advantages, imitation_actions)
        self.critic.train(states, state_values)

    def probs_to_one_hot(self, probabilities):
        one_hot_tensor = []
        for prob in probabilities:
            a = tf.constant(prob)
            one_hot = tf.one_hot(tf.nn.top_k(a).indices, tf.shape(a)[0]).eval(session=self.sess)
            one_hot_tensor.append(one_hot[0])
        return np.array(one_hot_tensor)

    def help_policy(self, states):
        actions = []
        for state in states:
            state = [state]
            if self.build_index >= len(self.build_order):
                if state[0][8] >= 10 / 200 and random.random() < 0.1:
                    action_index = 6
                elif state[0][7] < 6 / 10 and random.random() < 0.9:
                    if state[0][0] >= 150 / 3000:
                        action_index = 4
                    elif state[0][4] >= 1 / 200:
                        action_index = 5
                    else:
                        action_index = 0
                elif state[0][4] >= 1 / 200:
                    action_index = 5
                elif state[0][3] - state[0][2] <= 3 / 200 and state[0][0] > 100 / 3000:
                    action_index = 2
                elif state[0][3] - state[0][2] >= 1 / 200 and state[0][0] > 50 / 3000:
                    action_index = 3
                elif state[0][4] >= 1 / 200:
                    action_index = 5
                else:
                    action_index = 0
            else:
                build = self.build_order[self.build_index]
                if build == "scv":
                    if state[0][0] >= 50 / 3000 and state[0][3] - state[0][2] >= 1 / 200:
                        action_index = 1
                        self.build_index += 1
                    elif state[0][4] >= 1 / 200:
                        action_index = 5
                    else:
                        action_index = 0

                if build == "supply":
                    if state[0][0] >= 100 / 3000:
                        action_index = 2
                        self.build_index += 1
                    elif state[0][4] >= 1 / 200:
                        action_index = 5
                    else:
                        action_index = 0

                if build == "barracks":
                    if state[0][0] >= 150 / 3000:
                        action_index = 4
                        self.build_index += 1
                    elif state[0][4] >= 1 / 200:
                        action_index = 5
                    else:
                        action_index = 0
            action_one_hot = [0] * self.action_dim
            action_one_hot[action_index] = 1
            actions.append(action_one_hot)
        return actions

    def help_policy_2(self, states):
        actions = []
        for state in states:
            state = [state]
            if state[0][8] >= 20 / 200 and random.random() < 0.9:
                action_index = 6
            elif state[0][8] >= 10 / 200 and random.random() < 0.2:
                action_index = 6
            elif state[0][6] == 0:
                action_index = 2
            elif state[0][7] < 6 / 10 and random.random() < 0.9 and state[0][0] >= 150 / 3000:
                action_index = 4
            elif state[0][4] >= 1 / 200:
                action_index = 5
            elif state[0][3] - state[0][2] <= 5 / 200 and state[0][0] > 100 / 3000:
                action_index = 2
            elif state[0][3] - state[0][2] >= 1 / 200 and state[0][0] > 50 / 3000 and state[0][9] < 16/200:
                action_index = 1
            elif state[0][3] - state[0][2] >= 1 / 200 and state[0][0] > 50 / 3000:
                action_index = 3
            else:
                action_index = 0

            action_one_hot = [0] * self.action_dim
            action_one_hot[action_index] = 1
            actions.append(action_one_hot)

        return actions
