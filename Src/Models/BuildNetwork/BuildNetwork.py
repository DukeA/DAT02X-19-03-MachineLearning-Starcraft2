



from Models.BuildNetwork.Build_Actor import Build_Actor
from Models.BuildNetwork.Build_Critic_Actor import Build_Critic_Actor



class BuildNetwork:

    def __init__(self,build_state,action_state):
        self.build_state = build_state
        self.action_state = action_state
        self.epoch =5000
        self.lerarning_rate =0.02
        self.epsilon =1.0
        self.epsilon_decay =0.99
        self.tau =0.125

        self.build_actor = Build_Actor(,)




    def create_build_model(self, build_state):
        build_state = Build_Actor(self,build_state)


    def create_crtic_build_model(self,build_state):
        build_state = Build_Critic_Actor(self,build_state)


    def load_weights(self, item):

    def save_weights(self,item):