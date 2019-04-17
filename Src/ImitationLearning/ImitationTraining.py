import keras
from keras import models, layers, optimizers
import pickle
from pysc2.lib import units
from collections import defaultdict
import numpy as np
import random
import os
import h5py
import matplotlib.pyplot as plt

all_states = []
train_attack_data_dir = "C:/Users/Claes/Desktop/DAT02X-19-03-MachineLearning-Starcraft2/Src/Data/attack/"

all_files = os.listdir(train_attack_data_dir)
current = 0
increment = 1743 #length of starport folder
random.shuffle(all_files)
attack_states = []
for file in all_files[current:current+increment]:
    full_path = os.path.join(train_attack_data_dir, file)
    data = np.load(full_path)
    data = list(data)
    for d in data:
        attack_states.append(d)

#print(len(attack_states))


train_build_barracks_data_dir = "C:/Users/Claes/Desktop/DAT02X-19-03-MachineLearning-Starcraft2/Src/Data/build_barracks/"
all_files = os.listdir(train_build_barracks_data_dir)
random.shuffle(all_files)
build_barracks_states = []
for file in all_files[current:current+increment]:
    full_path = os.path.join(train_build_barracks_data_dir, file)
    data = np.load(full_path)
    data = list(data)
    for d in data:
        build_barracks_states.append(d)

#print(len(build_barracks_states))

train_build_factory_data_dir = "C:/Users/Claes/Desktop/DAT02X-19-03-MachineLearning-Starcraft2/Src/Data/build_factory/"
all_files = os.listdir(train_build_factory_data_dir)
random.shuffle(all_files)
build_factory_states = []
for file in all_files[current:current+increment]:
    full_path = os.path.join(train_build_factory_data_dir, file)
    data = np.load(full_path)
    data = list(data)
    for d in data:
        build_factory_states.append(d)

#print(len(build_factory_states))

train_build_hellion_data_dir = "C:/Users/Claes/Desktop/DAT02X-19-03-MachineLearning-Starcraft2/Src/Data/build_hellion/"
all_files = os.listdir(train_build_hellion_data_dir)
random.shuffle(all_files)
build_hellion_states = []
for file in all_files[current:current+increment]:
    full_path = os.path.join(train_build_hellion_data_dir, file)
    data = np.load(full_path)
    data = list(data)
    for d in data:
        build_hellion_states.append(d)

#print(len(build_hellion_states))

train_build_marine_data_dir = "C:/Users/Claes/Desktop/DAT02X-19-03-MachineLearning-Starcraft2/Src/Data/build_marine/"
all_files = os.listdir(train_build_marine_data_dir)
random.shuffle(all_files)
build_marine_states = []
for file in all_files[current:current+increment]:
    full_path = os.path.join(train_build_marine_data_dir, file)
    data = np.load(full_path)
    data = list(data)
    for d in data:
        build_marine_states.append(d)

#print(len(build_marine_states))

train_build_medivac_data_dir = "C:/Users/Claes/Desktop/DAT02X-19-03-MachineLearning-Starcraft2/Src/Data/build_medivac/"
all_files = os.listdir(train_build_medivac_data_dir)
random.shuffle(all_files)
build_medivac_states = []
for file in all_files[current:current+increment]:
    full_path = os.path.join(train_build_medivac_data_dir, file)
    data = np.load(full_path)
    data = list(data)
    for d in data:
        build_medivac_states.append(d)

#print(len(build_medivac_states))

train_build_reaper_data_dir = "C:/Users/Claes/Desktop/DAT02X-19-03-MachineLearning-Starcraft2/Src/Data/build_reaper/"
all_files = os.listdir(train_build_reaper_data_dir)
random.shuffle(all_files)
build_reaper_states = []
for file in all_files[current:current+increment]:
    full_path = os.path.join(train_build_reaper_data_dir, file)
    data = np.load(full_path)
    data = list(data)
    for d in data:
        build_reaper_states.append(d)

#print(len(build_reaper_states))

train_build_refinery_data_dir = "C:/Users/Claes/Desktop/DAT02X-19-03-MachineLearning-Starcraft2/Src/Data/build_refinery/"
all_files = os.listdir(train_build_refinery_data_dir)
random.shuffle(all_files)
build_refinery_states = []
for file in all_files[current:current+increment]:
    full_path = os.path.join(train_build_refinery_data_dir, file)
    data = np.load(full_path)
    data = list(data)
    for d in data:
        build_refinery_states.append(d)

#print(len(build_refinery_states))

train_build_scv_data_dir = "C:/Users/Claes/Desktop/DAT02X-19-03-MachineLearning-Starcraft2/Src/Data/build_scv/"
all_files = os.listdir(train_build_scv_data_dir)
random.shuffle(all_files)
build_scv_states = []
for file in all_files[current:current+increment]:
    full_path = os.path.join(train_build_scv_data_dir, file)
    data = np.load(full_path)
    data = list(data)
    for d in data:
       build_scv_states.append(d)

#print(len(build_scv_states))

train_build_starport_data_dir = "C:/Users/Claes/Desktop/DAT02X-19-03-MachineLearning-Starcraft2/Src/Data/build_starport/"
all_files = os.listdir(train_build_starport_data_dir)
random.shuffle(all_files)
build_starport_states = []
for file in all_files[current:current+increment]:
    full_path = os.path.join(train_build_starport_data_dir, file)
    data = np.load(full_path)
    data = list(data)
    for d in data:
        build_starport_states.append(d)

#print(len(build_starport_states))

train_build_supply_depot_data_dir = "C:/Users/Claes/Desktop/DAT02X-19-03-MachineLearning-Starcraft2/Src/Data/build_supply_depot/"
all_files = os.listdir(train_build_supply_depot_data_dir)
random.shuffle(all_files)
build_supply_depot_states = []
for file in all_files[current:current+increment]:
    full_path = os.path.join(train_build_supply_depot_data_dir, file)
    data = np.load(full_path)
    data = list(data)
    for d in data:
        build_supply_depot_states.append(d)

#print(len(build_supply_depot_states))

train_build_viking_data_dir = "C:/Users/Claes/Desktop/DAT02X-19-03-MachineLearning-Starcraft2/Src/Data/build_viking/"
all_files = os.listdir(train_build_viking_data_dir)
random.shuffle(all_files)
build_viking_states = []
for file in all_files[current:current+increment]:
    full_path = os.path.join(train_build_viking_data_dir, file)
    data = np.load(full_path)
    data = list(data)
    for d in data:
        build_viking_states.append(d)

#print(len(build_viking_states))

train_expand_data_dir = "C:/Users/Claes/Desktop/DAT02X-19-03-MachineLearning-Starcraft2/Src/Data/expand/"
all_files = os.listdir(train_expand_data_dir)
random.shuffle(all_files)
expand_states = []
for file in all_files[current:current+increment]:
    full_path = os.path.join(train_expand_data_dir, file)
    data = np.load(full_path)
    data = list(data)
    for d in data:
        expand_states.append(d)

#print(len(expand_states))

train_no_op_data_dir = "C:/Users/Claes/Desktop/DAT02X-19-03-MachineLearning-Starcraft2/Src/Data/no_op/"
all_files = os.listdir(train_no_op_data_dir)
random.shuffle(all_files)
no_op_states = []
for file in all_files[current:current+increment]:
    full_path = os.path.join(train_no_op_data_dir, file)
    data = np.load(full_path)
    data = list(data)
    for d in data:
        no_op_states.append(d)

#print(len(no_op_states))

train_retreat_data_dir = "C:/Users/Claes/Desktop/DAT02X-19-03-MachineLearning-Starcraft2/Src/Data/retreat/"
all_files = os.listdir(train_retreat_data_dir)
random.shuffle(all_files)
retreat_states = []
for file in all_files[current:current+increment]:
    full_path = os.path.join(train_retreat_data_dir, file)
    data = np.load(full_path)
    data = list(data)
    for d in data:
        retreat_states.append(d)

#print(len(retreat_states))

train_return_scv_data_dir = "C:/Users/Claes/Desktop/DAT02X-19-03-MachineLearning-Starcraft2/Src/Data/return_scv/"
all_files = os.listdir(train_return_scv_data_dir)
random.shuffle(all_files)
return_scv_states = []
for file in all_files[current:current+increment]:
    full_path = os.path.join(train_return_scv_data_dir, file)
    data = np.load(full_path)
    data = list(data)
    for d in data:
        return_scv_states.append(d)

#print(len(return_scv_states))

random.shuffle(attack_states)
random.shuffle(build_barracks_states)
random.shuffle(build_factory_states)
random.shuffle(build_hellion_states)
random.shuffle(build_marine_states)
random.shuffle(build_medivac_states)
random.shuffle(build_reaper_states)
random.shuffle(build_refinery_states)
random.shuffle(build_scv_states)
random.shuffle(build_starport_states)
random.shuffle(build_supply_depot_states)
random.shuffle(build_viking_states)
random.shuffle(expand_states)
random.shuffle(no_op_states)
random.shuffle(retreat_states)
random.shuffle(return_scv_states)

lowest_length = 2500 #check from #print or choose a lower number
attack_states = attack_states[:lowest_length]
build_barracks_states = build_barracks_states[:lowest_length]
build_factory_states = build_factory_states[:lowest_length]
build_hellion_states = build_hellion_states[:lowest_length]
build_marine_states = build_marine_states[:lowest_length]
build_medivac_states = build_medivac_states[:lowest_length]
build_reaper_states = build_reaper_states[:lowest_length]
build_refinery_states = build_refinery_states[:lowest_length]
build_scv_states = build_scv_states[:lowest_length]
build_starport_states = build_starport_states[:lowest_length]
build_supply_depot_states = build_supply_depot_states[:lowest_length]
build_viking_states = build_viking_states[:lowest_length]
expand_states = expand_states[:lowest_length]
no_op_states = no_op_states[:lowest_length]
retreat_states = retreat_states[:lowest_length]
return_scv_states = return_scv_states[:lowest_length]

all_states = attack_states + build_barracks_states + build_factory_states + build_hellion_states \
+ build_marine_states + build_medivac_states + build_reaper_states +  build_refinery_states \
+ build_scv_states + build_starport_states + build_supply_depot_states + build_viking_states \
+ expand_states + no_op_states + return_scv_states #+ retreat_states 


##print(len(all_states))

random.shuffle(all_states)

x_train = []
action_taken = []
y_train = []

for state in all_states:
    action_taken.append(state[7])

action_space = {
                    "attack": 0,
                    "build_barracks": 1,
                    "build_factory": 2,
                    "build_hellion": 3,
                    "build_marine": 4,
                    "build_medivac": 5,
                    "build_reaper": 6,
                    "build_refinery": 7,
                    "build_scv": 8,
                    "build_starport": 9,
                    "build_supply_depot": 10,
                    "build_viking": 11,
                    "expand": 12,
                    "no_op": 13,
                    "retreat": 14,
                    "return_scv": 15
                }
for i in range(len(all_states)):
    action_vector = [0] * 16
    action_vector[action_space.get(all_states[i][7], 0)] = 1
    y_train.append(action_vector)

for i in range(len(all_states)):
    minerals = all_states[i][0]
    gas = all_states[i][1]
    food_used = all_states[i][2]
    food_cap = all_states[i][3]
    idle_workers =  all_states[i][4]
    units_amount = defaultdict(int, all_states[i][5])
    enemy_units_amount = defaultdict(int, all_states[i][6])
    steps = all_states[i][8]

    command_centers = units_amount[units.Terran.CommandCenter.value]
    supply_depots = units_amount[units.Terran.SupplyDepot.value]
    refineries = units_amount[units.Terran.Refinery.value]
    barracks = units_amount[units.Terran.Barracks.value]
    factories = units_amount[units.Terran.Factory.value]
    starports = units_amount[units.Terran.Starport.value]
    scvs = units_amount[units.Terran.SCV.value]
    marines = units_amount[units.Terran.Marine.value]
    hellions = units_amount[units.Terran.Hellion.value]
    medivacs = units_amount[units.Terran.Medivac.value]
    reapers = units_amount[units.Terran.Reaper.value]
    vikings = units_amount[units.Terran.VikingFighter.value]
    
    enemy_command_centers = enemy_units_amount[units.Terran.CommandCenter.value]
    enemy_supply_depots = enemy_units_amount[units.Terran.SupplyDepot.value]
    enemy_refineries = enemy_units_amount[units.Terran.Refinery.value]
    enemy_barracks = enemy_units_amount[units.Terran.Barracks.value]
    enemy_factories = enemy_units_amount[units.Terran.Factory.value]
    enemy_starports = enemy_units_amount[units.Terran.Starport.value]
    enemy_scvs = enemy_units_amount[units.Terran.SCV.value]
    enemy_marines = enemy_units_amount[units.Terran.Marine.value]
    enemy_hellions = enemy_units_amount[units.Terran.Hellion.value]
    enemy_medivacs = enemy_units_amount[units.Terran.Medivac.value]
    enemy_reapers = enemy_units_amount[units.Terran.Reaper.value]
    enemy_vikings = enemy_units_amount[units.Terran.VikingFighter.value]

    minerals = minerals/(25*100)
    if minerals > 1:
        minerals = 1
    gas = gas/(25*100)
    if gas > 1:
        gas = 1
    food_used = food_used/200
    food_cap = food_cap/200
    idle_workers = idle_workers/25
    if idle_workers > 1:
        idle_workers = 1
    steps = int(steps/(1346/(5*12))) #5 second intervalls
    steps = steps/300
    if steps > 1:
        steps = 1
    command_centers = command_centers/10
    if command_centers > 1:
        command_centers = 1
    supply_depots = supply_depots/25
    if supply_depots > 1:
        supply_depots = 1
    refineries = refineries/20
    if refineries > 1:
        refineries = 1
    barracks = barracks/10
    if barracks > 1:
        barracks = 1
    factories = factories/10
    if factories > 1:
        factories = 1
    starports = starports/10
    if starports > 1:
        startports = 1
    scvs = scvs/50
    if scvs > 1:
        scvs = 1
    marines = marines/50
    if marines > 1:
        marines = 1
    hellions = hellions/50
    if hellions > 1:
        hellions = 1
    medivacs = medivacs/50
    if medivacs > 1:
        medivacs = 1
    reapers = reapers/50
    if reapers > 1:
        reapers = 1
    vikings = vikings/50
    if vikings > 1:
        vikings = 1
    enemy_command_centers = enemy_command_centers/10
    if enemy_command_centers > 1:
        enemy_command_centers = 1
    enemy_supply_depots = enemy_supply_depots/25
    if enemy_supply_depots > 1:
        enemy_supply_depots = 1
    enemy_refineries = enemy_refineries/20
    if enemy_refineries > 1:
        enemy_refineries = 1
    enemy_barracks = enemy_barracks/10
    if enemy_barracks > 1:
        enemy_barracks = 1
    enemy_factories = enemy_factories/10
    if enemy_factories > 1:
        enemy_factories = 1
    enemy_starports = enemy_starports/10
    if enemy_starports > 1:
        enemy_startports = 1
    enemy_scvs = enemy_scvs/50
    if enemy_scvs > 1:
        enemy_scvs = 1
    enemy_marines = enemy_marines/50
    if enemy_marines > 1:
        enemy_marines = 1
    enemy_hellions = enemy_hellions/50
    if enemy_hellions > 1:
        enemy_hellions = 1
    enemy_medivacs = enemy_medivacs/50
    if enemy_medivacs > 1:
        enemy_medivacs = 1
    enemy_reapers = enemy_reapers/50
    if enemy_reapers > 1:
        enemy_reapers = 1
    enemy_vikings = enemy_vikings/50
    if enemy_vikings > 1:
        enemy_vikings = 1
    
    x_train.append([minerals, gas, food_used, food_cap, idle_workers, steps, command_centers, supply_depots,
    refineries, barracks, factories, starports, scvs, marines, hellions, medivacs, reapers, vikings, 
    enemy_command_centers, enemy_supply_depots, enemy_refineries, enemy_barracks, enemy_factories, 
    enemy_starports, enemy_scvs, enemy_marines, enemy_hellions, enemy_medivacs, enemy_reapers,
     enemy_vikings])

network = models.Sequential()
network.add(layers.Dense(128, activation='relu', input_shape=(30,)))
network.add(layers.Dense(32, activation='relu'))
network.add(layers.Dense(16, activation='softmax'))
opt = keras.optimizers.adam(lr=0.001, decay=1e-6)
network.compile(loss='categorical_crossentropy',
                    optimizer=opt,
                    metrics=['accuracy'])

validation_amount = 2000
x_train = np.asarray(x_train)
y_train = np.asarray(y_train)
states_val = x_train[:validation_amount]
states_train = x_train[validation_amount:]
actions_val = y_train[:validation_amount]
actions_train = y_train[validation_amount:]
history = network.fit(states_train,
                              actions_train,
                              epochs= 10,
                              batch_size=1, shuffle=True,
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

network.save("C:/Users/Claes/Desktop/DAT02X-19-03-MachineLearning-Starcraft2/Src/imitation_models/test2.h5")