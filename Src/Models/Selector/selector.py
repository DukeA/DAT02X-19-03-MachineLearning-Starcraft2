import random

from Models.Selector.buildSelector import BuildSelector
from Models.Selector.attackSelector import AttackSelector


class Selector():

    def selector(self):
        print("hello1")

        # 16 steps per sekund, men kompenserar också för att step_mul = 5. 1.4 kompenserar för in-game time.
        if self.steps < 16*60*5/5*1.4:
            return BuildSelector.buildSelector(self)
        else:
            action = random.random()
            if action <= 0.25:
                return AttackSelector.attackSelector(self)
            else:
                return BuildSelector.buildSelector(self)

        return BuildSelector.buildSelector(self)
