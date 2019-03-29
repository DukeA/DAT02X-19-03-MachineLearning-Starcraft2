from pysc2.lib import units
from collections import defaultdict
import random
import numpy as np


class BuildAgent:
    def __init__(self, actor, critic, buffer, LSTM_len):
        self.action_space = {
            0: "no_op",
            1: "expand",
            2: "build_supply_depot",
            3: "build_refinery",
            4: "build_barracks",
            5: "build_factory",
            6: "build_starport",
            7: "build_tech_lab_barracks",
            8: "build_scv",
            9: "build_marine",
            10: "build_marauder",
            11: "build_reaper",
            12: "build_hellion",
            13: "build_medivac",
            14: "build_viking",
            15: "distribute_scv",
            16: "return_scv"
        }

        self.action_space_inverted = {
            "no_op": 0,
            "expand": 1,
            "build_supply_depot": 2,
            "build_refinery": 3,
            "build_barracks": 4,
            "build_factory": 5,
            "build_starport": 6,
            "build_tech_lab_barracks": 7,
            "build_scv": 8,
            "build_marine": 9,
            "build_marauder": 10,
            "build_reaper": 11,
            "build_hellion": 12,
            "build_medivac": 13,
            "build_viking": 14,
            "distribute_scv": 15,
            "return_scv": 16
        }

        self.actor = actor
        self.critic = critic
        self.buffer = buffer
        self.state_len = 13

        self.time_steps = LSTM_len
        self.old_states = [[(50/25)/40, 0, 1/10, 0, 0, 0, 0, 0, 12/100, 0, 0, 12/200, 15/200]]*self.time_steps


    def predict_lstm(self, state):
        if not state:
            print("Not sure how we got here")
            return "no_op"
        else:
            state0 = np.asarray([self.old_states])
            state0.reshape((1, self.time_steps, self.state_len))
            state1 = self.format_lstm_state(state)
            old_action_index = self.action_space_inverted.get(state[len(state)-1][3], 0)
            if old_action_index == 0:
                action0 = [1] + [0] * 16
            elif old_action_index == 16:
                action0 = [0] * 16 + [1]
            else:
                action0 = [0] * old_action_index + [1] + [0] * (17 - old_action_index - 1)
            prediction = self.actor.model.predict(state1)
            prediction = prediction[0]

            if random.random() < 0.2:
                index = random.randint(0, 16)
                if index == 0:
                    prediction = [1]+[0]*16
                elif index == 16:
                    prediction = [0]*16+[1]
                else:
                    prediction = [0]*index + [1] + [0]*(17-index-1)

            print("Actual action: " + self.action_space.get(np.argmax(action0), "no_op"))
            print("Predicted action: " + self.action_space.get(np.argmax(prediction), "no_op"))

            if old_action_index == 8:
                reward = 100
            elif old_action_index == 2:
                reward = -10
            else:
                reward = -1

            self.buffer.add(state0, action0, state1, reward)
            return self.action_space.get(np.argmax(prediction), "no_op")
            #choice = random.random()
            #for i in range(len(self.action_space)):
            #    if choice < sum(prediction[0:i+1]):
            #        print("Actual action: " + self.action_space.get(i, "no_op"))
            #        return self.action_space.get(i, "no_op")
            #print("This shouldn't happen (BuildAgent.py)")
            #return "no_op"

    def format_lstm_state(self, state):

        newest_state = len(state) - 1
        units_amount = defaultdict(int, state[newest_state][2])
        minerals = int(state[newest_state][0]/25)
        if minerals > 40:
            minerals = 40
        minerals = minerals/40
        gas = int(state[newest_state][1]/25)
        if gas > 40:
            gas = 40
        gas = gas/40
        command_centers = units_amount[units.Terran.CommandCenter.value]/10
        if command_centers > 1:
            command_centers = 1
        supply_depots = units_amount[units.Terran.SupplyDepot.value]/25
        if supply_depots > 1:
            supply_depots = 1
        refineries = units_amount[units.Terran.Refinery.value]/24
        if refineries > 1:
            refineries = 1
        barracks = units_amount[units.Terran.Barracks.value]/15
        if barracks > 1:
            barracks = 1
        factories = units_amount[units.Terran.Factory.value]/15
        if factories > 1:
            factories = 1
        starports = units_amount[units.Terran.Starport.value]/15
        if starports > 1:
            starports = 1
        scvs = units_amount[units.Terran.SCV.value]/100
        if scvs > 1:
            scvs = 1
        marines = units_amount[units.Terran.Marine.value]/100
        if marines > 1:
            marines = 1
        step = int(state[newest_state][4]*5/(16*1.4*5))    # Binning steps to 5 second intervals.
        step = step/134    # Equivalent to about 11 minutes
        if step > 1:
            step = 1
        food_used = int(state[newest_state][5]/200)
        food_cap = int(state[newest_state][6]/200)

        new_state = [minerals, gas, command_centers, supply_depots, refineries, barracks,
                     factories, starports, scvs, marines, step, food_used, food_cap]

        time_state = self.old_states[1:len(self.old_states)]+[new_state]
        formatted_state = np.asarray([time_state])
        formatted_state.reshape((1, self.time_steps, self.state_len))
        self.old_states = self.old_states[1:len(self.old_states)]+[new_state]
        return formatted_state
