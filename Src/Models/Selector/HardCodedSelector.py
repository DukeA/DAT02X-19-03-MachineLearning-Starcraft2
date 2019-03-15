import random

class HardCodedSelector():

    def hardCodedSelector(self, obs):

        if self.reqSteps == 0 and not self.game_state_updated:
            return "updateState"
        else:
            return "no_op"

        