import random
from Models.HelperClass.IsPossible import IsPossible

class Selector():

    def selector(self, obs):

        if self.reqSteps == 0 and not self.game_state_updated:
            return "updateState"
        else:
            self.game_state_updated = False
            # 16 steps per sekund, men kompenserar också för att step_mul = 5. 1.4 kompenserar för in-game time.
            if self.steps < 16 * 60 * 5 / 5 * 1.4:
                build_actions = Selector.possible_build_actions(self, obs)
                return (random.choice(build_actions))
            else:
                action = random.random()
                if action <= 0.25:
                    attack_actions = Selector.possible_attack_actions(self)
                    return (random.choice(attack_actions))
                else:
                    build_actions = Selector.possible_build_actions(self, obs)
                return (random.choice(build_actions))

        return (random.choice(Selector.all_possible_actions(self, obs)))


    def possible_build_actions(self, obs):
        poss_actions = ["no_op"]
        if IsPossible.build_scv_possible(self, obs):
            poss_actions.append("build_scv")
        else:
            poss_actions.append("no_op")

        if IsPossible.build_supply_depot_possible(self, obs):
            poss_actions.append("build_supply_depot")
        else:
            poss_actions.append("no_op")

        if IsPossible.build_marines_possible(self, obs):
            poss_actions.append("build_marine")
        else:
            poss_actions.append("no_op")

        if IsPossible.build_marauder_possible(self, obs):
            poss_actions.append("build_marauder")
        else:
            poss_actions.append("no_op")

        if IsPossible.build_reaper_possible(self, obs):
            poss_actions.append("build_reaper")
        else:
            poss_actions.append("no_op")

        if IsPossible.build_hellion_possible(self, obs):
            poss_actions.append("build_hellion")
        else:
            poss_actions.append("no_op")

        if IsPossible.build_medivac_possible(self, obs):
            poss_actions.append("build_medivac")
        else:
            poss_actions.append("no_op")

        if IsPossible.build_viking_possible(self, obs):
            poss_actions.append("build_viking")
        else:
            poss_actions.append("no_op")

        if IsPossible.build_barracks_possible(self, obs):
            poss_actions.append("build_barracks")
        else:
            poss_actions.append("no_op")

        if IsPossible.build_refinery_possible(self, obs):
            poss_actions.append("build_refinery")
        else:
            poss_actions.append("no_op")

        if True:
            poss_actions.append("distribute_scv")

        if True:
            poss_actions.append("return_scv")

        if IsPossible.build_command_center_possible(self, obs):
            poss_actions.append("expand")
        else:
            poss_actions.append("no_op")

        if IsPossible.build_factory_possible(self, obs):
            poss_actions.append("build_factory")
        else:
            poss_actions.append("no_op")

        if IsPossible.build_starport_possible(self, obs):
            poss_actions.append("build_starport")
        else:
            poss_actions.append("no_op")

        if IsPossible.build_techlab_possible(self, obs):
            poss_actions.append("build_tech_lab_barracks")
        else:
            poss_actions.append("no_op")

        return poss_actions

    def possible_attack_actions(self):
        poss_actions = ["no_op"]
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
        return poss_actions

    def all_possible_actions(self, obs):
        return (Selector.possible_build_actions(self, obs) + Selector.possible_attack_actions(self))