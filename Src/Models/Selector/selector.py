import random

from Models.Selector.buildSelector import BuildSelector
from Models.Selector.attackSelector import AttackSelector
from Models.MachineLearning.ActorCriticAgent import ActorCriticAgent


class Selector:

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
            return self.actor_critic_agent.predict(self.game_state)

                # 16 steps per sekund, men kompenserar också för att step_mul = 5. 1.4 kompenserar för in-game time.
                #if self.steps < 16 * 60 * 5 / 5 * 1.4:
                #    return BuildSelector.buildSelector(self, obs)
                #else:
                #    if self.reqSteps == -1:  # Kollar om AttackSelectorn precis räknade armén
                #        return AttackSelector.attackSelector(self, obs)
                #    else:
                #        action = random.random()
                #       if action <= 0.25:
                #            return AttackSelector.attackSelector(self, obs)
                #        else:
                #            return BuildSelector.buildSelector(self, obs)

        #return BuildSelector.buildSelector(self, obs)
