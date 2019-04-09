
from keras.layers import Dense, Input
from keras.models import Sequential,Model
from keras.optimizers import Adam

class Build_Actor:
    def __init__(self,build_model, action_szie, learning_rate, epsilion):
        self.build_model = build_model
        self.epsilon = epsilion
        self.action_size = action_szie
        self.learning_rate = learning_rate
        self.build_author_model = Build_Actor.create_actor_model(self,Build_Actor.build_model)


    def create_actor_model (self,build_model):
        build_state_model = Sequential
        build_state_model.add(Dense(300,input_dim=build_model,activation='relu'))
        build_state_model.add(Dense(600,activation='relu'))
        build_state_model.add(Dense(300,activation='relu'))
        build_state_model.add(Dense(self.action_size[0],activation='relu'))
        build_state_model.compile(loss="mse", optimizer=Adam(Build_Actor.learning_rate))
        return build_state_model

    def train_actor_model(self, sample_screen):
        for items in sample_screen:



    def load_weights(self, item):
        self.build_author_model.load_weights(item)


    def save_weights(self, item):
        self.build_author_model.save_weights(item)