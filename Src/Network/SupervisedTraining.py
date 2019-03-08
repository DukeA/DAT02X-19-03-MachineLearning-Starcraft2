#import keras
import pickle
from pysc2.lib import units
from collections import defaultdict
import numpy as np


def main():
    number_of_games = 4
    states = []
    actions = []
    # Load data and format it correctly
    for i in range(number_of_games):
        path = "C:/Users/Edvin/Documents/Python/SC2MachineLearning/DAT02X-19-03-MachineLearning-Starcraft2/Src/test"\
               + str(i+1) + ".data"
        next_states, next_actions = fetch_data(path)
        states = states+next_states
        actions = actions+next_actions
    states = np.asarray(states)
    actions = np.asarray(actions)
    print(actions.shape)
    print(states.shape)

    for i in range(len(actions)):
        print(actions[i][3])


def fetch_data(path):
    """
    Fetches and correctly formats data. Also only includes "good" data, as defined by is_good_data().
    :param path: the path to the data
    :return:
    """
    state = []
    action = []
    with open(path, 'rb') as filehandle:
        imported_data = pickle.load(filehandle)
    if is_good_data(imported_data):
        for i in range(len(imported_data)):
            # Discards first state/action pair
            if i > 0:
                # Formats the state array
                units_amount = defaultdict(int, imported_data[i][2])
                minerals = imported_data[i][0]
                gas = imported_data[i][1]
                command_centers = units_amount[units.Terran.CommandCenter.value]
                supply_depot = units_amount[units.Terran.SupplyDepot.value]
                refineries = units_amount[units.Terran.Refinery.value]
                barracks = units_amount[units.Terran.Barracks.value]
                factories = units_amount[units.Terran.Factory.value]
                starports = units_amount[units.Terran.Starport.value]
                scvs = units_amount[units.Terran.SCV.value]
                marines = units_amount[units.Terran.Marine.value]

                state.append([minerals, gas, command_centers, supply_depot, refineries, barracks,
                             factories, starports, scvs, marines])

                # Formats the action array
                action_space = {
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
                action_vector = [0] * 17
                action_vector[action_space.get(imported_data[i][3], 0)] = 1
                action.append(action_vector)

    return [state, action]


def is_good_data(data):
    """Checks if the data is good or not. Currently, the data is good if the game terminates before 600 agent steps.

    :param data: the data to be evaluated
    :return: boolean
    """
    if data[len(data)-1][4] < 600:
        return True
    else:
        return False


if __name__ == '__main__':
    main()
