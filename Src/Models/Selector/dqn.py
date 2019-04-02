import random
import gym
import numpy as np
from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam


class DQN:
    def __init__(self, state_size, action_size):
        """Initializes the network
                :param action_size: The size of the action space.
                :param state_size: The number of different state variables
                """

        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95    # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = self._build_model()

    def _build_model(self):
        """Builds the network with the desired layout
                returns: the network
                """

        # Neural Net for Deep-Q learning Model
        model = Sequential()
        model.add(Dense(24, input_dim=self.state_size, activation='relu'))
        model.add(Dense(24, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse',
                      optimizer=Adam(lr=self.learning_rate))
        return model

    def remember(self, state, action, reward, next_state, done):
        """Adds a entry to the memory
                :param state: The state.
                :param action: The action taken.
                :param reward: Reward received from the action
                :param next_state: The following state
                :param done: A bool indicating if its the last step
                """
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        """Takes an action either based on the state or at random.
                :param state: The current state
                """
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])  # returns action

    def replay(self, batch_size):
        """trains the network based on its memory
                :param batch_size: How big the random batch is to be that is used in fitting the network.
                """

        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if state is None:
                break
            if not done:
                target = reward + self.gamma * \
                    np.amax(self.model.predict(next_state))
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def load(self, name):
        """Loads a network from file
                :param name: The path to the file
                """
        self.model.load_weights(name)

    def save(self, name):
        """saves a network to file
                :param name: The path to the file
                """
        self.model.save_weights(name)
