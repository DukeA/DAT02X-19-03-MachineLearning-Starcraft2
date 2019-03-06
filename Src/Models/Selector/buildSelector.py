import random

from Models.HelperClass.IsPossible import IsPossible


class BuildSelector():
    def buildSelector(self, obs):
        possible_actions = BuildSelector.possible_build_actions(self, obs)
        return (random.choice(possible_actions))

    # True ska buytas ut mot is possible metoderna
    def possible_build_actions(self, obs):
        poss_actions = ["do_nothing"]
        if IsPossible.build_scv_possible(self, obs):
            poss_actions.append("build_scv")
        if IsPossible.build_supply_depot_possible(self, obs):
            poss_actions.append("build_supply_depot")
        if IsPossible.build_marines_possible(self, obs):
            poss_actions.append("build_marine")
        if IsPossible.build_marauder_possible(self, obs):
            poss_actions.append("build_marauder")
        if True:
            poss_actions.append("build_reaper")
        if True:
            poss_actions.append("build_hellion")
        if IsPossible.build_medivac_possible(self, obs):
            poss_actions.append("build_medivac")
        if True:
            poss_actions.append("build_viking")
        if True:
            poss_actions.append("transform_viking_to_ground")
        if True:
            poss_actions.append("transform_viking_to_air")
        if IsPossible.build_barracks_possible(self, obs):
            poss_actions.append("build_barracks")
        if IsPossible.build_refinery_possible(self, obs):
            poss_actions.append("build_refinery")
        if True:
            poss_actions.append("distribute_scv")
        if True:
            poss_actions.append("return_scv")
        if IsPossible.build_command_center_possible(self, obs):
            poss_actions.append("expand")
        if IsPossible.build_factory_possible(self, obs):
            poss_actions.append("build_factory")
        if IsPossible.build_starport_possible(self, obs):
            poss_actions.append("build_starport")
        if IsPossible.build_techlab_possible(self, obs):
            poss_actions.append("build_tech_lab")
        if True:
            poss_actions.append("no_op")
        return poss_actions
