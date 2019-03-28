import numpy  as np
from kreas.models import Sequential
from keras.layers import Dense, Reshape,Flatten
from keras.optimizers import  Adam
import tensorflow as tf
import json



class CriticBuildNetwork:
    def __init__(self,state_size,action_size,build_model,batch_size,tau,learning_rate):
        self.state_size = state_size
        self.action_size = action_size
        self.build_model = build_model
        self.batch_size = batch_size
        self.tau = tau
        self.learning_rate = learning_rate

    def build_model(self):
        model = Sequential()
        model.add