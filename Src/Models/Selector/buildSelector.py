import random
import os
import pandas as pd
import numpy as np
from pysc2.lib import units


from Models.HelperClass.IsPossible import IsPossible
from Models.Selector.dqn import DQN



actions = ["no_op", "build_scv", "build_supply_depot", "build_marine", "build_marauder", "build_reaper",
           "build_hellion", "build_medivac", "build_viking", "build_barracks", "build_refinery",
           "return_scv", "expand", "build_factory", "build_starport", "build_tech_lab_barracks"]


class BuildSelector():
    def myround(x, base=5):
        return int(base * round(float(x)/base))

    def buildSelector(self, obs):

        state = BuildSelector.format_state(self, obs)
        state = np.reshape(state, [1, 4])
        s = state[0, :]

        if self.agent is None:
            self.agent = DQN(state_size = 4, action_size=len(actions))
            if os.path.isfile('shortgames.h5'):
                self.agent.load('shortgames.h5')

        action = self.agent.act(state)



        self.agent.remember(self.previous_state, self.previous_action, 0, state, False)


        self.previous_state = state
        self.previous_action = action

        translatedaction = actions[action]

        if len(self.agent.memory) > 32:
            self.agent.replay(32)
        return translatedaction

    def format_state(self, obs):
        current_state = np.zeros(4)

        if self.game_state.units_amount[units.Terran.CommandCenter.value] > 3:
            current_state[0] = 3
        else:
            current_state[0] = self.game_state.units_amount[units.Terran.CommandCenter.value]

        if self.game_state.units_amount[units.Terran.SupplyDepot.value] > 5:
            current_state[1] = 5
        else:
            current_state[1] = self.game_state.units_amount[units.Terran.SupplyDepot.value]

        if self.game_state.units_amount[units.Terran.Barracks.value] > 3:
            current_state[2] = 3
        else:
            current_state[2] = self.game_state.units_amount[units.Terran.Barracks.value]

        current_state[3] = BuildSelector.myround(obs.observation.player.food_workers)




        return current_state


    # True ska buytas ut mot is possible metoderna
    def excluded_actions(self, obs):
        excluded_actions = []

        if not IsPossible.build_scv_possible(self, obs):
            excluded_actions.append(actions.index("build_scv"))

        if not IsPossible.build_supply_depot_possible(self, obs):
            excluded_actions.append(actions.index("build_supply_depot"))

        if not IsPossible.build_marines_possible(self, obs):
            excluded_actions.append(actions.index("build_marine"))

        if not IsPossible.build_marauder_possible(self, obs):
            excluded_actions.append(actions.index("build_marauder"))

        if not IsPossible.build_reaper_possible(self, obs):
            excluded_actions.append(actions.index("build_reaper"))

        if not IsPossible.build_hellion_possible(self, obs):
            excluded_actions.append(actions.index("build_hellion"))

        if not IsPossible.build_medivac_possible(self, obs):
            excluded_actions.append(actions.index("build_medivac"))

        if not IsPossible.build_viking_possible(self, obs):
            excluded_actions.append(actions.index("build_viking"))

        if not IsPossible.build_barracks_possible(self, obs):
            excluded_actions.append(actions.index("build_barracks"))

        if not IsPossible.build_refinery_possible(self, obs):
            excluded_actions.append(actions.index("build_refinery"))

        # if not  True:
        #     excluded_actions.append("distribute_scv")

        if not True:
            excluded_actions.append(actions.index("return_scv"))

        if not IsPossible.build_command_center_possible(self, obs):
            excluded_actions.append(actions.index("expand"))

        if not IsPossible.build_factory_possible(self, obs):
            excluded_actions.append(actions.index("build_factory"))

        if not IsPossible.build_starport_possible(self, obs):
            excluded_actions.append(actions.index("build_starport"))

        if not IsPossible.build_techlab_possible(self, obs):
            excluded_actions.append(actions.index("build_tech_lab_barracks"))

        return excluded_actions
