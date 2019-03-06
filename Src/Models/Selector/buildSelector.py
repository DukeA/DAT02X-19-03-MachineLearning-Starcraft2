import random


class BuildSelector():
    def buildSelector(self):
        possible_actions = BuildSelector.possible_build_actions(self)
        return random.choice(possible_actions)

    # True ska buytas ut mot is possible metoderna
    def possible_build_actions(self):
        poss_actions = ["do_nothing"]
        if True:
            poss_actions.append("build_scv")
        if True:
            poss_actions.append("build_supply_depot")
        if True:
            poss_actions.append("build_marine")
        if True:
            poss_actions.append("build_marauder")
        if True:
            poss_actions.append("build_reaper")
        if True:
            poss_actions.append("build_hellion")
        if True:
            poss_actions.append("build_medivac")
        if True:
            poss_actions.append("build_viking")
        if True:
            poss_actions.append("transform_viking_to_ground")
        if True:
            poss_actions.append("transform_viking_to_air")
        if True:
            poss_actions.append("build_barracks")
        if True:
            poss_actions.append("build_refinery")
        if True:
            poss_actions.append("return_scv")
        if True:
            poss_actions.append("expand")
        if True:
            poss_actions.append("build_factory")
        if True:
            poss_actions.append("build_starport")
        if True:
            poss_actions.append("build_tech_lab")
        if True:
            poss_actions.append("no_op")
        return poss_actions
