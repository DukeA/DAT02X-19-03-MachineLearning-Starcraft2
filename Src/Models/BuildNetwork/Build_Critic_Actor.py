

from keras.layers import Dense,Input
from keras.models import Model,Sequential
from keras.layers.merge import Add
from keras.optimizers import Adam

class Build_Critic_Actor:

    def __init__(self,build_model,action_model,Learning_rate):
        self.build_model = build_model
        self.action_model = action_model
        self.Learning_rate = Learning_rate
        self.crtic_model = Build_Critic_Actor.create_crtic_model(self,build_model,action_model)



    def create_crtic_model(self,build_model,action_model):

        build_author_model = Sequential
        build_author_model.add(Dense(300,input_dim=build_model,activation='relu'))
        build_author_model.add(Dense(600,activation='relu'))
        action_crtic_model =Sequential
        action_crtic_model.add(Dense(600, input_dim=action_model,activation='relu'))
        critic_state_model = Sequential
        critic_state_model.add(Add()[build_author_model,action_crtic_model])
        critic_state_output = Sequential
        critic_state_output.add(Dense(1, input_dim=critic_state_model,activation='relu'))
        critic_model= Sequential
        critic_model.add(Model(input=critic_state_model,output =critic_state_output))
        critic_model.compile(loss='mse',optimizer=Adam(Build_Critic_Actor.Learning_rate))
        return critic_model


    def train_crtic(self, sample_screen):
        for items in sample:


    def load_weights(self,path):
        self.crtic_model.load_weights(path)

    def save_weights(self,path):
        self.crtic_model.save_weights(path + 'crtic_build_actor.h5')








