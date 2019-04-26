
class Selector():

    def __init__(self):
        super(Selector, self).__init__()

    def selector(self, obs):

        if self.reqSteps == 0 and not self.game_state_updated:
            return "updateState"
        else:
            self.game_state_updated = False
            return self.actor_critic_agent.predict(self.game_state, obs)

        return "no_op"
