from keras import models, layers, optimizers
import pickle
from pysc2.lib import units
from collections import defaultdict
import numpy as np
import random
import os
import h5py
import matplotlib.pyplot as plt

time_steps = 5  # For the LSTM layer
model_path = ("C:/Users/Edvin/Documents/Python/SC2MachineLearning/DAT02X-19-03-MachineLearning-Starcraft2/" +
              "Src/TrainingData/10Marines/LSTM_nops_A.h5")
number_of_games = 1000
is_training_session = True
validation = False

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

def main():

    states = []
    actions = []
    all_length = []
    good_length = []
    good_games = 0
    total_games = 0

    # Load data and format it correctly
    names = ["random_game"]
    #names = ["3m18sPII"]
    #names = ["StateIIIB"]
    for j in range(len(names)):
        for i in range(number_of_games):
            path = "C:/Users/Edvin/Documents/Python/SC2MachineLearning/" + \
                   "DAT02X-19-03-MachineLearning-Starcraft2/Src/TrainingData/10Marines/" +\
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
    print(states.shape)

    m_g_length = sum(all_length)/len(all_length) * 5 / (1.4 * 60 * 16)

    print("Mean game length = "+str((int(m_g_length)))+"m"+str(round(60*(m_g_length-int(m_g_length))))+"s")
    if len(good_length) > 0:
        m_g_g_length = sum(good_length) / len(good_length) * 5 / (1.4 * 60 * 16)
        print("Mean good game length = "+str((int(m_g_g_length)))+"m"+str(round(60*(m_g_g_length-int(m_g_g_length))))+"s")

    if is_training_session:
        # It can either build a model from scratch or train an existing model. Not sure if the latter is advised.
        network = build_model()

        if validation:
            states, actions = shuffle(states, actions)

            validation_amount = 2000
            states_val = states[:validation_amount]
            states_train = states[validation_amount:]
            actions_val = actions[:validation_amount]
            actions_train = actions[validation_amount:]
            history = network.fit(states_train,
                                  actions_train,
                                  epochs=10,
                                  batch_size=512,
                                  validation_data=(states_val, actions_val))
            loss = history.history['loss']
            val_loss = history.history['val_loss']

            epochs = range(1, len(loss) + 1)

            plt.figure(0)
            plt.plot(epochs, loss, 'bo', label='Training loss')
            plt.plot(epochs, val_loss, 'b', label='Validation loss')
            plt.title('Training and validation loss')
            plt.xlabel('Epochs')
            plt.ylabel('Loss')
            plt.legend()

            plt.figure(1)

            acc = history.history['acc']
            val_acc = history.history['val_acc']
            plt.plot(epochs, acc, 'bo', label='Training acc')
            plt.plot(epochs, val_acc, 'b', label='Validation acc')
            plt.title('Training and validation accuracy')
            plt.xlabel('Epochs')
            plt.ylabel('Accuracy')
            plt.legend()

            plt.show()
        else:
            history = network.fit(states,
                                  actions,
                                  epochs=10,
                                  batch_size=512)
            loss = history.history['loss']
            epochs = range(1, len(loss) + 1)

            plt.figure(0)
            plt.plot(epochs, loss, 'bo', label='Training loss')
            plt.title('Training and validation loss')
            plt.xlabel('Epochs')
            plt.ylabel('Loss')
            plt.legend()
            plt.figure(1)

            acc = history.history['acc']
            plt.plot(epochs, acc, 'bo', label='Training acc')
            plt.title('Training and validation accuracy')
            plt.xlabel('Epochs')
            plt.ylabel('Accuracy')
            plt.legend()

            plt.show()

        network.save(model_path)


def shuffle(states, actions):
    """
    A very naive shuffling algorithm. Probably can be done a lot better without the shuffler list, but I don't care.
    :param states: the states
    :param actions: the actions
    :return: states, actions
    """
    states_space_len = 11
    shuffler = list(range(len(states)))
    new_states1 = np.array([states[shuffler[0]]])
    new_actions1 = np.array([actions[shuffler[0]]])
    if len(shuffler) >= 10000:
        new_states2 = np.array([states[shuffler[10000]]])
        new_actions2 = np.array([actions[shuffler[10000]]])
    if len(shuffler) >= 20000:
        new_states3 = np.array([states[shuffler[20000]]])
        new_actions3 = np.array([actions[shuffler[20000]]])
    if len(shuffler) >= 30000:
        new_states4 = np.array([states[shuffler[30000]]])
        new_actions4 = np.array([actions[shuffler[30000]]])
    if len(shuffler) >= 40000:
        new_states5 = np.array([states[shuffler[40000]]])
        new_actions5 = np.array([actions[shuffler[40000]]])
    if len(shuffler) >= 50000:
        new_states6 = np.array([states[shuffler[50000]]])
        new_actions6 = np.array([actions[shuffler[50000]]])
    if len(shuffler) >= 60000:
        new_states7 = np.array([states[shuffler[60000]]])
        new_actions7 = np.array([actions[shuffler[60000]]])
    if len(shuffler) >= 70000:
        new_states8 = np.array([states[shuffler[70000]]])
        new_actions8 = np.array([actions[shuffler[70000]]])
    random.shuffle(shuffler)
    for i in range(len(shuffler)):
        print("Shuffling index "+str(i)+" out of "+str(len(shuffler))+".")
        if 0 < i < 10000:
            new_states1 = np.append(new_states1, states[shuffler[i]].reshape(1, time_steps, states_space_len), axis=0)
            new_actions1 = np.append(new_actions1, actions[shuffler[i]].reshape(1, 17), axis=0)
        elif 10000 < i < 20000:
            new_states2 = np.append(new_states2, states[shuffler[i]].reshape(1, time_steps, states_space_len), axis=0)
            new_actions2 = np.append(new_actions2, actions[shuffler[i]].reshape(1, 17), axis=0)
        elif 20000 < i < 30000:
            new_states3 = np.append(new_states3, states[shuffler[i]].reshape(1, time_steps, states_space_len), axis=0)
            new_actions3 = np.append(new_actions3, actions[shuffler[i]].reshape(1, 17), axis=0)
        elif 30000 < i < 40000:
            new_states4 = np.append(new_states4, states[shuffler[i]].reshape(1, time_steps, states_space_len), axis=0)
            new_actions4 = np.append(new_actions4, actions[shuffler[i]].reshape(1, 17), axis=0)
        elif 40000 < i < 50000:
            new_states5 = np.append(new_states5, states[shuffler[i]].reshape(1, time_steps, states_space_len), axis=0)
            new_actions5 = np.append(new_actions5, actions[shuffler[i]].reshape(1, 17), axis=0)
        elif 50000 < i < 60000:
            new_states6 = np.append(new_states6, states[shuffler[i]].reshape(1, time_steps, states_space_len), axis=0)
            new_actions6 = np.append(new_actions6, actions[shuffler[i]].reshape(1, 17), axis=0)
        elif 60000 < i < 70000:
            new_states7 = np.append(new_states7, states[shuffler[i]].reshape(1, time_steps, states_space_len), axis=0)
            new_actions7 = np.append(new_actions7, actions[shuffler[i]].reshape(1, 17), axis=0)
        elif i > 70000:
            new_states8 = np.append(new_states8, states[shuffler[i]].reshape(1, time_steps, states_space_len), axis=0)
            new_actions8 = np.append(new_actions8, actions[shuffler[i]].reshape(1, 17), axis=0)
    if len(shuffler) < 10000:
        states = new_states1
        actions = new_actions1
    if len(shuffler) >= 10000:
        states = np.append(new_states1, new_states2, axis=0)
        actions = np.append(new_actions1, new_actions2, axis=0)
    if len(shuffler) >= 20000:
        states = np.append(states, new_states3, axis=0)
        actions = np.append(actions, new_actions3, axis=0)
    if len(shuffler) >= 30000:
        states = np.append(states, new_states4, axis=0)
        actions = np.append(actions, new_actions4, axis=0)
    if len(shuffler) >= 40000:
        states = np.append(states, new_states5, axis=0)
        actions = np.append(actions, new_actions5, axis=0)
    if len(shuffler) >= 50000:
        states = np.append(states, new_states6, axis=0)
        actions = np.append(actions, new_actions6, axis=0)
    if len(shuffler) >= 60000:
        states = np.append(states, new_states7, axis=0)
        actions = np.append(actions, new_actions7, axis=0)
    if len(shuffler) >= 70000:
        states = np.append(states, new_states8, axis=0)
        actions = np.append(actions, new_actions8, axis=0)

    return states, actions


def remove_no_ops(states, actions, fraction):
    """
    Removes no_op actions. The amount removed is specified by 'fraction'
    :param states: the states
    :param actions: the actions
    :param fraction: the fraction of no_ops to remove
    :return: states, actions
    """
    no_op_indices = []
    for i in range(len(actions)):
        if actions[i][0] == 1:
            no_op_indices.append(i)

    nbr_of_states, nbr_of_state_elements = states.shape
    nbr_of_actions, nbr_of_action_elements = actions.shape

    new_states = np.zeros((nbr_of_states-int(len(no_op_indices)*fraction), nbr_of_state_elements))
    new_actions = np.zeros((nbr_of_actions-int(len(no_op_indices)*fraction), nbr_of_action_elements))

    random.shuffle(no_op_indices)
    no_op_indices = no_op_indices[0:int(len(no_op_indices)*fraction)]

    k = 0
    for i in range(len(states)):
        print(i)
        if i not in no_op_indices:
            new_states[k] = states[i]
            new_actions[k] = actions[i]
            k += 1

    return new_states, new_actions


def filter_data(states, actions):
    """
    Filters the state/action pairs by
    removing some excess no_ops for states that also have corresponding non-no_ops actions.
    :param states: the states
    :param actions: the actions
    :return: states, actions
    """
    no_op_indices = []
    for i in range(len(actions)):
        if actions[i][0] == 1:
            no_op_indices.append(i)
    print(len(no_op_indices))
    print(len(states))

    checked_indices = []
    indices_to_remove = []

    new_states = np.zeros((1, 10))
    new_actions = np.zeros((1, 17))

    for j in range(len(no_op_indices)):
        nbr_of_same_state = []
        nbr_of_no_op = []
        for i in range(no_op_indices[j], len(states)):
            if np.array_equal(states[i], states[no_op_indices[j]]) and i not in checked_indices:
                nbr_of_same_state.append(i)
                checked_indices.append(i)
                if actions[i][0] == 1:
                    nbr_of_no_op.append(i)
                # Note: want to pair as many no_op actions with the state as there are non-no_op actions.
        difference = len(nbr_of_same_state)-len(nbr_of_no_op)
        if difference > 0:
            indices_to_remove = indices_to_remove+nbr_of_no_op[0:difference]

        # print(checked_indices)
        # print("Same state: "+str(nbr_of_same_state))
        # print("No_ops: "+str(nbr_of_no_op))
        print("Iteration: "+str(j)+"/"+str(len(no_op_indices)))
        print("Removing: "+str(len(indices_to_remove)))

    for i in range(len(states)):
        if i not in indices_to_remove:
            new_states = np.append(new_states, states[i].reshape(1, 10), axis=0)
            new_actions = np.append(new_actions, actions[i].reshape(1, 17), axis=0)
    np.save('C:/Users/Edvin/Documents/Python/SC2MachineLearning/DAT02X-19-03-MachineLearning-Starcraft2/Src' +
            '/TrainingData/10Marines/new_states.npy', new_states)
    np.save('C:/Users/Edvin/Documents/Python/SC2MachineLearning/DAT02X-19-03-MachineLearning-Starcraft2/Src' +
            '/TrainingData/10Marines/new_actions.npy', new_actions)
    return new_states, new_actions


def build_model():
    """
    Builds the neural network model
    :return: the network
    """
    network = models.Sequential()
    network.add(layers.LSTM(100, input_shape=(time_steps, 11), return_sequences=False))
    network.add(layers.Dense(32, activation='relu'))
    network.add(layers.Dense(17, activation='softmax'))
    network.compile(loss='categorical_crossentropy',
                    optimizer='adam',
                    metrics=['accuracy'])
    return network


def fetch_data(path):
    """
    Fetches and correctly formats data for LSTM layers. Also only includes "good" data, as defined by is_good_data().
    :param path: the path to the data
    :return:
    """
    state = []
    action = []

    with open(path, 'rb') as filehandle:
        imported_data = pickle.load(filehandle)
        length = imported_data[len(imported_data)-1][4]
    if is_good_data(imported_data):
        dummy_state = [(50/25)/40, 0, 1/10, 0, 0, 0, 0, 0, 12/100, 0, 0]
        old_state = [dummy_state]*(time_steps-1)
        for i in range(len(imported_data)):
            # Discards first state/action pair and no_ops
            if i > 0:
            #if i > 0 and action_space.get(imported_data[i][3], 0) > 0:    # Currently filters no_ops
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
                step = int(imported_data[i][4]*5/(16*1.4*5))    # Binning steps to 5 second intervals.
                step = step/134    # Equivalent to about 11 minutes
                if step > 1:
                    step = 1

                new_state = [minerals, gas, command_centers, supply_depots, refineries, barracks,
                             factories, starports, scvs, marines, step]

                state.append(old_state+[new_state])
                old_state = old_state[1:len(old_state)]+[new_state]

                # Formats the action array
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
    maximum_game_length = 3.7    # in minutes. For reference, 16 (17) SCVs and 10 marines took 2m40s.
    if data[len(data)-1][4] < (16*60*maximum_game_length*1.4/5):
        return True
    else:
        return False


if __name__ == '__main__':
    main()
