import numpy as np
from keras.initilizers import normal, identity
from keras.models import model_from_json,load_model
from keras.models import Sequential


class BuildNetwork:
    def __init__(self, state_size, action_size,build_model,batch_size,tau,learning_rate):
        self.state_size = state_size
        self.action_size = action_size
        self.build_model = build_model
        self.gamma = 0.99
        self.learning_rate = learning_rate
        self.states = []
        self.gradients = []
        self.batch_size = batch_size
        self.tau = tau


