import random
from Models.HelperClass.IsPossible import IsPossible


class BuildSelector():
    def buildSelector(self, obs, agent):
        agent_or_not = random.random()
        if agent_or_not < 2:
            return agent.predict_lstm(self.game_state.get_state())
        else:
            possible_actions = BuildSelector.possible_build_actions(self, obs)
            selection = random.random()
            if selection < 0.15:
                action = possible_actions[1]    # build scv
            elif selection < 0.2:
                action = possible_actions[2]    # build supply depot
            elif selection < 0.35:
                action = possible_actions[3]    # build marine
            elif selection < 0.4:
                action = possible_actions[9]    # build barracks
            elif selection < 0.45:
                action = possible_actions[10]    # build refinery
            elif selection < 0.5:
                action = possible_actions[11]    # distribute scv
            elif selection < 0.55:
                action = possible_actions[12]    # return scv
            else:
                action = possible_actions[17]    # no op
            # action = random.choice(possible_actions)
            return action

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
