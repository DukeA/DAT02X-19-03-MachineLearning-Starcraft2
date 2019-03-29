from keras import models
from pysc2.lib import units
from collections import defaultdict
import random
import numpy as np


class BuildAgent:
    def __init__(self):
        self.network = models.load_model("C:/Users/Edvin/Documents/Python/SC2MachineLearning/" +
                                         "DAT02X-19-03-MachineLearning-Starcraft2/Src/TrainingData/" +
                                         "10Marines/LSTM_ops_B.h5")
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

        self.time_steps = 15
        self.old_states = [[(50/25)/40, 0, 1/10, 0, 0, 0, 0, 0, 12/100, 0, 0]]*(self.time_steps-1)

    def predict_lstm(self, state):
        if not state:
            print("Not sure how we got here")
            return "no_op"
        else:
            corrected_state = self.format_lstm_state(state)
            prediction = self.network.predict(corrected_state)
            prediction = prediction[0]
            print("Predicted action: " + self.action_space.get(np.argmax(prediction), "no_op"))
            return self.action_space.get(np.argmax(prediction), "no_op")
            #choice = random.random()
            #for i in range(len(self.action_space)):
            #    if choice < sum(prediction[0:i+1]):
            #        print("Actual action: " + self.action_space.get(i, "no_op"))
            #        return self.action_space.get(i, "no_op")
            #print("This shouldn't happen (BuildAgent.py)")
            #return "no_op"

    def predict(self, state):
        if not state:
            print("Not sure how we got here")
            return "no_op"
        else:
            corrected_state = self.format_state(state)
            prediction = self.network.predict(corrected_state)
            prediction = prediction[0]
            #return self.action_space.get(np.argmax(prediction), "no_op")
            choice = random.random()
            for i in range(len(self.action_space)):
                if choice < sum(prediction[0:i+1]):
                    print(self.action_space.get(i, "no_op"))
                    return self.action_space.get(i, "no_op")
            print("This shouldn't happen (BuildAgent.py)")
            return "no_op"

    def predict2(self, state):
        """This one tries to skip no_op if the probability is below a certain threshold."""
        if not state:
            print("Not sure how we got here")
            return "no_op"
        else:
            corrected_state = self.format_state(state)
            prediction = self.network.predict(corrected_state)
            prediction = prediction[0]
            non_no_op_action = np.argmax(prediction[1:len(prediction)])+1
            print(prediction[non_no_op_action]/prediction[0])

            if 10*prediction[non_no_op_action] > prediction[0]:
                new_prediction = [x/sum(prediction[1:len(prediction)]) for x in prediction[1:len(prediction)]]
                choice = random.random()
                for i in range(len(new_prediction)):
                    if choice < sum(new_prediction[0:i + 1]):
                        print(self.action_space.get(i+1, "no_op"))
                        return self.action_space.get(i+1, "no_op")
            else:
                return "no_op"

    def predict3(self, state):
        """This one tries to skip no_op if the probability is below a certain threshold."""
        if not state:
            print("Not sure how we got here")
            return "no_op"
        else:
            corrected_state = self.format_state(state)
            prediction = self.network.predict(corrected_state)
            prediction = prediction[0]
            non_no_op_action = np.argmax(prediction[1:len(prediction)])+1
            print(prediction[non_no_op_action]/prediction[0])

            if 100*prediction[non_no_op_action] > prediction[0]:
                new_prediction = [x/sum(prediction[1:len(prediction)]) for x in prediction[1:len(prediction)]]
                choice = random.random()
                for i in range(len(new_prediction)):
                    if choice < sum(new_prediction[0:i + 1]):
                        print(self.action_space.get(i+1, "no_op"))
                        return self.action_space.get(i+1, "no_op")
            else:
                return "no_op"

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

        new_state = [minerals, gas, command_centers, supply_depots, refineries, barracks,
                     factories, starports, scvs, marines, step]

        time_state = self.old_states+[new_state]
        formatted_state = np.asarray([time_state])
        formatted_state.reshape(1, self.time_steps, 11)
        self.old_states = self.old_states[1:len(self.old_states)]+[new_state]
        return formatted_state

    def format_state(self, state):
        """

        :param state: the list that gets fetched from State.get_state()
        :return: A nicely formatted state
        """
        newest_state = len(state)-1
        units_amount = defaultdict(int, state[newest_state][2])
        minerals = int(state[newest_state][0] / 25)
        if minerals > 40:
            minerals = 40
        minerals = minerals / 40
        gas = int(state[newest_state][1] / 25)
        if gas > 40:
            gas = 40
        gas = gas / 40
        command_centers = units_amount[units.Terran.CommandCenter.value] / 10
        if command_centers > 1:
            command_centers = 1
        supply_depots = units_amount[units.Terran.SupplyDepot.value] / 25
        if supply_depots > 1:
            supply_depots = 1
        refineries = units_amount[units.Terran.Refinery.value] / 24
        if refineries > 1:
            refineries = 1
        barracks = units_amount[units.Terran.Barracks.value] / 15
        if barracks > 1:
            barracks = 1
        factories = units_amount[units.Terran.Factory.value] / 15
        if factories > 1:
            factories = 1
        starports = units_amount[units.Terran.Starport.value] / 15
        if starports > 1:
            starports = 1
        scvs = units_amount[units.Terran.SCV.value] / 100
        if scvs > 1:
            scvs = 1
        marines = units_amount[units.Terran.Marine.value] / 100
        if marines > 1:
            marines = 1
        step = int(state[newest_state][4] * 5 / (16 * 1.4 * 5))  # Binning steps to 5 second intervals.
        step = step / 134  # Sets maximum to about 11 minutes
        if step > 1:
            step = 1

        formatted_state = np.asarray([minerals, gas, command_centers, supply_depots, refineries,
                                     barracks, factories, starports, scvs, marines, step])
        return formatted_state.reshape(1, 11)
