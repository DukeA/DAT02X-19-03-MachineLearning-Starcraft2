
import numpy as np
import random
import argparse
from keras.models import model_fromjson,Model
from keras.models import Sequential
from keras.layers.core import Dense,Dropout,Activation,Flatten
from keras.optimizers import Adam
import tensorflow as tf
import json

from Models.BuildNetwork.BuildNetwork import BuildNetwork
from Models.BuildNetwork.CriticBuildNetwork import CriticBuildNetwork
from Models.BuildNetwork.BuildFacade import BuildFacade
class BuildCrticAgent()
    def __init__(self,action_dim,state_dim,action_space):
        self.tra