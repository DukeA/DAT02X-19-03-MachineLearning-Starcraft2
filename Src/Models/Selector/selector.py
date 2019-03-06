import random

from Models.Selector.buildSelector import BuildSelector
from Models.Selector.attackSelector import AttackSelector


class Selector():

    def selector(self):

        #if self.reqSteps == 0:
        if not self.game_state_updated:
            return "updateState"
        else:
            self.game_state_updated = False
            # 16 steps per sekund, men kompenserar också för att step_mul = 5. 1.4 kompenserar för in-game time.
            if self.steps < 16 * 60 * 5 / 5 * 1.4:
                return BuildSelector.buildSelector(self)
            else:
                if self.reqSteps == -1:  # Kollar om AttackSelectorn precis räknade armén
                    return AttackSelector.attackSelector(self)
                else:
                    action = random.random()
                    if action <= 0.25:
                        return AttackSelector.attackSelector(self)
                    else:
                        return BuildSelector.buildSelector(self)
            #self.game_state_updated = False
            #if self.steps < 16*60*5/5*1.4:  # 16 steps per sekund, men kompenserar också för att step_mul = 5. 1.4 kompenserar för in-game time.
            #    self.selector = 'buildSelector'
            #else:
            #    self.selector = random.choice(selectors)

        return BuildSelector.buildSelector(self)
