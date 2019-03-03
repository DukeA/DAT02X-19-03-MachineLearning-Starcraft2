import random


class AttackSelector():
    def attackSelector(self):

        possible_actions = AttackSelector.possible_attack_actions(self)
        return (random.choice(possible_actions))

    # True ska buytas ut mot is possible metoderna
    def possible_attack_actions(self):
        poss_actions = ["do_nothing"]
        if True:
            poss_actions.append("attack")
        if True:
            poss_actions.append("retreat")
        if True:
            poss_actions.append("scout")
        if True:
            poss_actions.append("no_op")
        return poss_actions
