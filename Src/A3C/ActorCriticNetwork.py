from keras import models, layers, optimizers
import keras
import keras.backend as K
import tensorflow as tf

class ActorCriticNetwork(keras.Model):
    def __init__(self, state_size, action_size):
        super(ActorCriticNetwork, self).__init__()
        self.state_size = state_size
        self.action_size = action_size

    def predict_sc2(self, state):
        return 0

# TODO: Actual A3C