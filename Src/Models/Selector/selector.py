import random

from Models.Selector.buildSelector import BuildSelector
from Models.Selector.attackSelector import AttackSelector


class Selector():

    def selector(self):
        # action = random.random()
        #     return AttackSelector.attackSelector(self)
        # else: detta ska vara här
        return BuildSelector.buildSelector(self)
