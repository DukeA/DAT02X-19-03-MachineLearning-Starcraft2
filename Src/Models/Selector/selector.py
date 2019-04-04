import random

from Models.Selector.buildSelector import BuildSelector
from Models.Selector.attackSelector import AttackSelector


class Selector():

    def selector(self, obs):

        if self.reqSteps == 0 and not self.game_state_updated:
            return "updateState"
        else:
            self.game_state_updated = False
            # 16 steps per sekund, men kompenserar också för att step_mul = 5. 1.4 kompenserar för in-game time.
            if self.steps < 16 * 60 * 5 / 5 * 1.4:
                selected_action = BuildSelector.buildSelector(self, obs, self.build_agent)
                return BuildSelector.buildSelector(self, obs, self.build_agent)
            else:
                action = random.random()
                if action <= 0.25:
                    selected_action = AttackSelector.attackSelector(self, obs)
                    return AttackSelector.attackSelector(self, obs)
                else:
                    selected_action = BuildSelector.buildSelector(self, obs, self.build_agent)
                    return BuildSelector.buildSelector(self, obs, self.build_agent)

        return BuildSelector.buildSelector(self, obs, self.build_agent)
