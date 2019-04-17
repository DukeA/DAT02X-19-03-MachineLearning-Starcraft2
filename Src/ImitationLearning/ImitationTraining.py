from keras import models, layers, optimizers
import pickle
from pysc2.lib import units
from collections import defaultdict
import numpy as np
import random
import os
import h5py
#import matplotlib.pyplot as plt

all_states = []
train_attack_data_dir = "C:/Users/Claes/Desktop/old_data/attack/"

all_files = os.listdir(train_attack_data_dir)
current = 0
increment = len(all_files)
maximum = len(all_files)
random.shuffle(all_files)
attack_states = []
for file in all_files[current:current+increment]:
    full_path = os.path.join(train_attack_data_dir, file)
    data = np.load(full_path)
    data = list(data)
    for d in data:
        attack_states.append(d)

print(len(attack_states))


train_build_barracks_data_dir = "C:/Users/Claes/Desktop/old_data/build_barracks/"
all_files = os.listdir(train_build_barracks_data_dir)
random.shuffle(all_files)
build_barracks_states = []
for file in all_files[current:current+increment]:
    full_path = os.path.join(train_build_barracks_data_dir, file)
    data = np.load(full_path)
    data = list(data)
    for d in data:
        build_barracks_states.append(d)

print(len(build_barracks_states))

train_build_factory_data_dir = "C:/Users/Claes/Desktop/old_data/build_factory/"
all_files = os.listdir(train_build_factory_data_dir)
random.shuffle(all_files)
build_factory_states = []
for file in all_files[current:current+increment]:
    full_path = os.path.join(train_build_factory_data_dir, file)
    data = np.load(full_path)
    data = list(data)
    for d in data:
        build_factory_states.append(d)

print(len(build_factory_states))

train_build_hellion_data_dir = "C:/Users/Claes/Desktop/old_data/build_hellion/"
all_files = os.listdir(train_build_hellion_data_dir)
random.shuffle(all_files)
build_hellion_states = []
for file in all_files[current:current+increment]:
    full_path = os.path.join(train_build_hellion_data_dir, file)
    data = np.load(full_path)
    data = list(data)
    for d in data:
        build_hellion_states.append(d)

print(len(build_hellion_states))

train_build_marine_data_dir = "C:/Users/Claes/Desktop/old_data/build_marine/"
all_files = os.listdir(train_build_marine_data_dir)
random.shuffle(all_files)
build_marine_states = []
for file in all_files[current:current+increment]:
    full_path = os.path.join(train_build_marine_data_dir, file)
    data = np.load(full_path)
    data = list(data)
    for d in data:
        build_marine_states.append(d)

print(len(build_marine_states))

train_build_medivac_data_dir = "C:/Users/Claes/Desktop/old_data/build_medivac/"
all_files = os.listdir(train_build_medivac_data_dir)
random.shuffle(all_files)
build_medivac_states = []
for file in all_files[current:current+increment]:
    full_path = os.path.join(train_build_medivac_data_dir, file)
    data = np.load(full_path)
    data = list(data)
    for d in data:
        build_medivac_states.append(d)

print(len(build_medivac_states))

train_build_reaper_data_dir = "C:/Users/Claes/Desktop/old_data/build_reaper/"
all_files = os.listdir(train_build_reaper_data_dir)
random.shuffle(all_files)
build_reaper_states = []
for file in all_files[current:current+increment]:
    full_path = os.path.join(train_build_reaper_data_dir, file)
    data = np.load(full_path)
    data = list(data)
    for d in data:
        build_reaper_states.append(d)

print(len(build_reaper_states))

train_build_refinery_data_dir = "C:/Users/Claes/Desktop/old_data/build_refinery/"
all_files = os.listdir(train_build_refinery_data_dir)
random.shuffle(all_files)
build_refinery_states = []
for file in all_files[current:current+increment]:
    full_path = os.path.join(train_build_refinery_data_dir, file)
    data = np.load(full_path)
    data = list(data)
    for d in data:
        build_refinery_states.append(d)

print(len(build_refinery_states))

train_build_scv_data_dir = "C:/Users/Claes/Desktop/old_data/build_scv/"
all_files = os.listdir(train_build_scv_data_dir)
random.shuffle(all_files)
build_scv_states = []
for file in all_files[current:current+increment]:
    full_path = os.path.join(train_build_scv_data_dir, file)
    data = np.load(full_path)
    data = list(data)
    for d in data:
       build_scv_states.append(d)

print(len(build_scv_states))

train_build_starport_data_dir = "C:/Users/Claes/Desktop/old_data/build_starport/"
all_files = os.listdir(train_build_starport_data_dir)
random.shuffle(all_files)
build_starport_states = []
for file in all_files[current:current+increment]:
    full_path = os.path.join(train_build_starport_data_dir, file)
    data = np.load(full_path)
    data = list(data)
    for d in data:
        build_starport_states.append(d)

print(len(build_starport_states))

train_build_supply_depot_data_dir = "C:/Users/Claes/Desktop/old_data/build_supply_depot/"
all_files = os.listdir(train_build_supply_depot_data_dir)
random.shuffle(all_files)
build_supply_depot_states = []
for file in all_files[current:current+increment]:
    full_path = os.path.join(train_build_supply_depot_data_dir, file)
    data = np.load(full_path)
    data = list(data)
    for d in data:
        build_supply_depot_states.append(d)

print(len(build_supply_depot_states))

train_build_viking_data_dir = "C:/Users/Claes/Desktop/old_data/build_viking/"
all_files = os.listdir(train_build_viking_data_dir)
random.shuffle(all_files)
build_viking_states = []
for file in all_files[current:current+increment]:
    full_path = os.path.join(train_build_viking_data_dir, file)
    data = np.load(full_path)
    data = list(data)
    for d in data:
        build_viking_states.append(d)

print(len(build_viking_states))

train_expand_data_dir = "C:/Users/Claes/Desktop/old_data/expand/"
all_files = os.listdir(train_expand_data_dir)
random.shuffle(all_files)
expand_states = []
for file in all_files[current:current+increment]:
    full_path = os.path.join(train_expand_data_dir, file)
    data = np.load(full_path)
    data = list(data)
    for d in data:
        expand_states.append(d)

print(len(expand_states))

train_no_op_data_dir = "C:/Users/Claes/Desktop/old_data/no_op/"
all_files = os.listdir(train_no_op_data_dir)
random.shuffle(all_files)
no_op_states = []
for file in all_files[current:current+increment]:
    full_path = os.path.join(train_no_op_data_dir, file)
    data = np.load(full_path)
    data = list(data)
    for d in data:
        no_op_states.append(d)

print(len(no_op_states))

train_retreat_data_dir = "C:/Users/Claes/Desktop/old_data/retreat/"
all_files = os.listdir(train_retreat_data_dir)
random.shuffle(all_files)
retreat_states = []
for file in all_files[current:current+increment]:
    full_path = os.path.join(train_retreat_data_dir, file)
    data = np.load(full_path)
    data = list(data)
    for d in data:
        retreat_states.append(d)

print(len(retreat_states))

train_return_scv_data_dir = "C:/Users/Claes/Desktop/old_data/return_scv/"
all_files = os.listdir(train_return_scv_data_dir)
random.shuffle(all_files)
return_scv_states = []
for file in all_files[current:current+increment]:
    full_path = os.path.join(train_return_scv_data_dir, file)
    data = np.load(full_path)
    data = list(data)
    for d in data:
        return_scv_states.append(d)

print(len(return_scv_states))

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

lowest_length = 1 #check from print or choose a lower number
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
+ expand_states + no_op_states + retreat_states + return_scv_states


#print(len(all_states))

random.shuffle(all_states)
x_train = []
y_train = []

for state in all_states:
    y_train.append(state[7])

for i in range(len(all_states)):
    minerals = all_states[i][0]
    gas = all_states[i][1]
    food_used = all_states[i][2]
    food_cap = all_states[i][3]
    idle_workers =  all_states[i][4]
    units_amount = defaultdict(int, all_states[i][5])
    enemy_units_amount = defaultdict(int, all_states[i][6])
    step = all_states[i][8]

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

    x_train.append([minerals, gas, food_used, food_cap, idle_workers, command_centers, supply_depots,
    refineries, barracks, factories, starports, scvs, marines, hellions, medivacs, reapers, vikings, 
    enemy_command_centers, enemy_supply_depots, enemy_refineries, enemy_barracks, enemy_factories, 
    enemy_starports, enemy_scvs, enemy_marines, enemy_hellions, enemy_medivacs, enemy_reapers,
     enemy_vikings, step])

#print(y_train)
print(x_train)

