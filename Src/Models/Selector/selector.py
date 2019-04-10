import random
from Models.HelperClass.IsPossible import IsPossible


from Models.MachineLearning.ActorCriticAgent import ActorCriticAgent
class Selector():

    def __init__(self):
        super(Selector, self).__init__()

    def selector(self, obs):

        if self.reqSteps == 0 and not self.game_state_updated:
            return "updateState"
        else:
            #if obs.first():
            #    self.actor_critic_agent =
            #else:
            self.game_state_updated = False
            return self.actor_critic_agent.predict(self.game_state, obs)

        return BuildSelector.buildSelector(self, obs)
