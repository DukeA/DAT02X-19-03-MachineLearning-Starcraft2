from keras import models, layers, optimizers
import pickle
from pysc2.lib import units
from collections import defaultdict
import numpy as np
import os
import h5py


def main():
    number_of_games = 300
    states = []
    actions = []
    all_length = []
    good_length = []
    is_training_session = True
    good_games = 0
    total_games = 0
    # Load data and format it correctly
    #names = ["marinetest_random", "marinetest_scvagent"]
    #names = ["marinetest_random"]
    #names = ["marinetestII"]
    for j in range(len(names)):
        for i in range(number_of_games):
            path = "C:/Users/Edvin/Documents/Python/SC2MachineLearning/" + \
                   "DAT02X-19-03-MachineLearning-Starcraft2/Src/TrainingData/" +\
                    names[j] + str(i+1) + ".data"
            if os.path.isfile(path):
                next_states, next_actions, next_length = fetch_data(path)
                states = states+next_states
                actions = actions+next_actions
                all_length.append(next_length)
                total_games += 1
                if len(next_states) > 0:
                    good_games += 1
                    good_length.append(next_length)

    print("Total games = "+str(total_games))
    print("Total good games = "+str(good_games))
    states = np.asarray(states)
    actions = np.asarray(actions)
    #print(actions.shape)
    #print(states.shape)
    print("Mean game length = "+str(sum(all_length)/len(all_length)))
    if len(good_length) > 0:
        print("Mean good game length = "+str(sum(good_length)/len(good_length)))

    if is_training_session:
        network = build_model()
        #network = models.load_model("C:/Users/Edvin/Documents/Python/SC2MachineLearning/" +
        #                            "DAT02X-19-03-MachineLearning-Starcraft2/Src/TrainingData/" +
        #                            "baselinescvproductions.h5")
        #network.fit(states, actions, epochs=10)
        #network.save("C:/Users/Edvin/Documents/Python/SC2MachineLearning/DAT02X-19-03-MachineLearning-Starcraft2/" +
        #             "Src/TrainingData/quickmarinetest.h5")
        #test_state = np.asarray([0.5, 0, 0.1, 0/30, 0, 0/30, 0, 0, 0.06, 0])
        #test_state = test_state.reshape(1, 10)
        #prediction = network.predict(test_state)
        #print(prediction.shape)
        #print(prediction)
        #print(sum(sum(prediction)))


def build_model():
    network = models.Sequential()
    network.add(layers.Dense(128, activation='relu', input_shape=(10,)))
    network.add(layers.Dense(52, activation='relu'))
    network.add(layers.Dense(17, activation='softmax'))
    #network.summary()
    network.compile(loss='categorical_crossentropy',
                    optimizer='rmsprop',
                    metrics=['accuracy'])
    return network


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
        length = imported_data[len(imported_data)-1][4]
    if is_good_data(imported_data):
        for i in range(len(imported_data)):
            # Discards first state/action pair
            if i > 0:
                # Formats the state array
                # TODO: Tech lab and tech labbed barracks
                units_amount = defaultdict(int, imported_data[i][2])
                minerals = int(imported_data[i][0]/25)
                if minerals > 40:
                    minerals = 40
                minerals = minerals/40
                gas = int(imported_data[i][1]/25)
                if gas > 40:
                    gas = 40
                gas = gas/40
                command_centers = units_amount[units.Terran.CommandCenter.value]/10
                supply_depot = units_amount[units.Terran.SupplyDepot.value]/30
                refineries = units_amount[units.Terran.Refinery.value]/30
                barracks = units_amount[units.Terran.Barracks.value]/30
                factories = units_amount[units.Terran.Factory.value]/30
                starports = units_amount[units.Terran.Starport.value]/30
                scvs = units_amount[units.Terran.SCV.value]/200
                marines = units_amount[units.Terran.Marine.value]/200

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

    return [state, action, length]


def is_good_data(data):
    """Checks if the data is good or not. Currently, the data is good if
        the game terminates before maximum_game_length.

    :param data: the data to be evaluated
    :return: boolean
    """
    maximum_game_length = 3.2    # in minutes
    if data[len(data)-1][4] < (16*60*maximum_game_length*1.4/5):
        return True
    else:
        return False


if __name__ == '__main__':
    main()
