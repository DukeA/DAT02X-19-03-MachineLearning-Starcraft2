import random

from Models.HelperClass.IsPossible import IsPossible


class BuildSelector():
    def buildSelector(self, obs):
        possible_actions = BuildSelector.possible_build_actions(self, obs)
        return (random.choice(possible_actions))

    # True ska bytas ut mot is possible metoderna
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
