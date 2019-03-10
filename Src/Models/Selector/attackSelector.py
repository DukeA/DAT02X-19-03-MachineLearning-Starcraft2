import random


class AttackSelector():
    def attackSelector(self, obs):
        if self.reqSteps == 0:
            return "army_count"
        else:
            self.reqSteps = 0
            possible_actions = AttackSelector.possible_attack_actions(self)
            selection = random.random()
            if selection < 0.15:
                action = possible_actions[1]
            elif selection < 0.2:
                action = possible_actions[2]
            elif selection < 0.25:
                action = possible_actions[3]
            elif selection < 0.31:
                action = possible_actions[4]
            elif selection < 0.32:
                action = possible_actions[5]
            else:
                action = possible_actions[6]
            return action

    # True ska bytas ut mot is possible metoderna
    def possible_attack_actions(self):
        poss_actions = ["do_nothing"]
        if True:
            poss_actions.append("attack")
        elif False:    # Byts ut, som sagt.
            poss_actions.append("no_op")
        if True:
            poss_actions.append("retreat")
        elif False:
            poss_actions.append("no_op")
        if True:
            poss_actions.append("scout")
        elif False:
            poss_actions.append("no_op")
        if True:
            poss_actions.append("transform_vikings_to_ground")
        elif False:
            poss_actions.append("no_op")
        if True:
            poss_actions.append("transform_vikings_to_air")
        elif False:
            poss_actions.append("no_op")
        if True:
            poss_actions.append("no_op")
        return poss_actions
