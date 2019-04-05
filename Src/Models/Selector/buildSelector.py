import random
import os
import pandas as pd
import numpy as np
from pysc2.lib import units


from Models.HelperClass.IsPossible import IsPossible
from Models.Selector.dqn import DQN


actions = ["no_op", "build_scv", "build_supply_depot", "build_marine", "build_barracks",
           "return_scv", "attack"]


class BuildSelector():
    def myround(x, base=50):
        return int(base * round(float(x)/base))

    def buildSelector(self, obs):

        state = BuildSelector.format_state(self, obs)
        state = np.reshape(state, [1, 9])

        if self.agent is None:
            self.agent = DQN(state_size=9, action_size=len(actions))
            if os.path.isfile('shortgames.h5'):
                self.agent.load('shortgames.h5')

        action = self.agent.act(state)

        if action == 20:
            rand_act = random.choice(BuildSelector.availableaction(self, obs))
            translate = BuildSelector.translaterandact(self, rand_act)
            action = translate

        self.agent.remember(self.previous_state, self.previous_action, 0, state, False)

        self.minerals = self.game_state.minerals
        self.previous_state = state
        self.previous_action = action

        translatedaction = actions[action]

        if len(self.agent.memory) > 32:
            self.agent.replay(32)
        return translatedaction

    def format_state(self, obs):
        current_state = np.zeros(9)

        current_state[0] = self.game_state.units_amount[units.Terran.CommandCenter]
        current_state[1] = self.game_state.units_amount[units.Terran.SupplyDepot]
        current_state[2] = self.game_state.units_amount[units.Terran.Barracks]
        current_state[3] = self.game_state.units_amount[units.Terran.SCV]
        current_state[4] = self.game_state.units_amount[units.Terran.Marine]
        current_state[5] = self.game_state.food_cap
        current_state[6] = self.game_state.food_used
        current_state[7] = self.game_state.food_cap - self.game_state.food_used
        current_state[8] = self.game_state.minerals

        # normalizing
        u = (1/current_state.size) * np.sum(current_state)
        sig = (1/current_state.size) * np.square(np.sum(current_state))

        current_state = current_state - u
        current_state = current_state / sig

        return current_state

    def actionpossible(self, action, obs):
        ok = True
        if action == 0:
            pass
        elif action == 1:
            ok = IsPossible.build_scv_possible(self, obs)
        elif action == 2:
            ok = IsPossible.build_supply_depot_possible(self, obs)
        elif action == 3:
            ok = IsPossible.build_marines_possible(self, obs)
        elif action == 4:
            ok = IsPossible.build_barracks_possible(self, obs)
        elif action == 5:
            pass
        elif action == 6:
            ok = IsPossible.attack_possible(self, obs)

        return ok

    def availableaction(self, obs):
        actions = ["no_op"]
        if IsPossible.build_scv_possible(self, obs):
            actions.append("build_scv")
        if IsPossible.build_supply_depot_possible(self, obs):
            actions.append("build_supply_depot")
        if IsPossible.build_marines_possible(self, obs):
            actions.append("build_marine")
        if IsPossible.build_barracks_possible(self, obs):
            actions.append("build_barracks")
        if obs.observation.player.idle_worker_count > 1:
            actions.append("return_scv")
        if IsPossible.attack_possible(self, obs):
            actions.append("attack")
        return actions

    def translaterandact(self, act):
        if act == "no_op":
            return 0
        if act == "build_scv":
            return 1
        if act == "build_supply_depot":
            return 2
        if act == "build_marine":
            return 3
        if act == "build_barracks":
            return 4
        if act == "return_scv":
            return 5
        if act == "attack":
            return 6
