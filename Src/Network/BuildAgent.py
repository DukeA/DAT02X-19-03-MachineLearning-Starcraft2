from keras import models
from pysc2.lib import units
from collections import defaultdict
import random
import numpy as np


class BuildAgent:
    def __init__(self):
        self.network = models.load_model("C:/Users/Edvin/Documents/Python/SC2MachineLearning/" +
                                         "DAT02X-19-03-MachineLearning-Starcraft2/Src/TrainingData/" +
                                         "quickmarinetest.h5")
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

    def predict(self, state):
        if not state:
            print("Not sure how we got here")
            return "no_op"
        else:
            corrected_state = self.format_state(state)
            prediction = self.network.predict(corrected_state)
            prediction = prediction[0]

            choice = random.random()
            for i in range(len(self.action_space)):
                if choice < sum(prediction[0:i+1]):
                    return self.action_space.get(i, "no_op")
            print("This shouldn't happen (BuildAgent.py)")
            return "no_op"

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
        supply_depot = units_amount[units.Terran.SupplyDepot.value] / 30
        refineries = units_amount[units.Terran.Refinery.value] / 30
        barracks = units_amount[units.Terran.Barracks.value] / 30
        factories = units_amount[units.Terran.Factory.value] / 30
        starports = units_amount[units.Terran.Starport.value] / 30
        scvs = units_amount[units.Terran.SCV.value] / 200
        marines = units_amount[units.Terran.Marine.value] / 200

        formatted_state = np.asarray([minerals, gas, command_centers, supply_depot, refineries,
                                     barracks, factories, starports, scvs, marines])
        return formatted_state.reshape(1, 10)
