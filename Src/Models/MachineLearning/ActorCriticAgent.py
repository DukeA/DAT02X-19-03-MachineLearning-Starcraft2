import numpy as np
import random
import argparse
from keras.models import model_from_json, Model
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.optimizers import Adam
import tensorflow as tf
#from keras.engine.training import _collect_trainable_weights
import json

from Models.MachineLearning.ReplayBuffer import ReplayBuffer
from Models.MachineLearning.ActorNetwork import ActorNetwork
from Models.MachineLearning.CriticNetwork import CriticNetwork
from Models.MachineLearning.OU import OU
import timeit

OU = OU()       #Ornstein-Uhlenbeck Process

class ActorCriticAgent:
    def __init__(self):
        self.train_indicator = True
        self.BUFFER_SIZE = 100000
        self.BATCH_SIZE = 32
        self.GAMMA = 0.99
        self.TAU = 0.001     #Target Network HyperParameters
        self.LRA = 0.0001    #Learning rate for Actor
        self.LRC = 0.001     #Lerning rate for Critic

        self.action_dim = 3  #Steering/Acceleration/Brake
        self.state_dim = 29  #of sensors input

        self.np.random.seed(1337)

        self.vision = False

        self.EXPLORE = 100000.
        self.episode_count = 2000
        self.max_steps = 1000
        self.reward = 0
        self.done = False
        self.step = 0
        self.epsilon = 1
        self.indicator = 0

        # Tensorflow GPU optimization
        self.config = tf.ConfigProto()
        self.config.gpu_options.allow_growth = True
        self.sess = tf.Session(config=self.config)
        from keras import backend as k
        k.set_session(self.sess)

        self.actor = ActorNetwork(self.sess, self.state_dim, self.action_dim, self.BATCH_SIZE, self.TAU, self.LRA)
        self.critic = CriticNetwork(self.sess, self.state_dim, self.action_dim, self.BATCH_SIZE, self.TAU, self.LRC)
        self.buff = ReplayBuffer(self.BUFFER_SIZE)    #Create replay buffer

        self.total_reward = 0
        self.prev_state = None
        self.prev_action = None


        # Now load the weight
        print("Now we load the weight")
        try:
            self.actor.model.load_weights("actormodel.h5")
            self.critic.model.load_weights("criticmodel.h5")
            self.actor.target_model.load_weights("actormodel.h5")
            self.critic.target_model.load_weights("criticmodel.h5")
            print("Weight load successfully")
        except:
            print("Cannot find the weight")

        # Batch variables
        #self.loss = 0

        print("TORCS Experiment Start.")

    def predict(self, game_state):
        #for i in range(episode_count):

            #print("Episode : " + str(i) + " Replay Buffer " + str(buff.count()))

            #if np.mod(i, 3) == 0:
            #    ob = env.reset(relaunch=True)  # relaunch TORCS every 3 episode because of the memory leak error
            #else:
            #    ob = env.reset()

            #s_t = np.hstack((ob.angle, ob.track, ob.trackPos, ob.speedX, ob.speedY,  ob.speedZ, ob.wheelSpinVel/100.0, ob.rpm))


            #for j in range(max_steps):
                state = [game_state.minerals]

                loss = 0
                self.epsilon -= 1.0 / self.EXPLORE
                #a_t = np.zeros([1,self.action_dim])
                noise_t = np.zeros([1,self.action_dim])

                chosen_action = self.actor.model.predict(state.reshape(1, state.shape[0]))

                #noise_t[0][0] = self.train_indicator * max(self.epsilon, 0) * OU.function(a_t_original[0][0],  0.0 , 0.60, 0.30)
                #noise_t[0][1] = self.train_indicator * max(self.epsilon, 0) * OU.function(a_t_original[0][1],  0.5 , 1.00, 0.10)
                #noise_t[0][2] = self.train_indicator * max(self.epsilon, 0) * OU.function(a_t_original[0][2], -0.1 , 1.00, 0.05)

                # The following code do the stochastic brake
                # if random.random() <= 0.1:
                #    print("********Now we apply the brake***********")
                #    noise_t[0][2] = train_indicator * max(epsilon, 0) * OU.function(a_t_original[0][2],  0.2 , 1.00, 0.10)

                #a_t[0][0] = a_t_original[0][0] + noise_t[0][0]
                #a_t[0][1] = a_t_original[0][1] + noise_t[0][1]
                #a_t[0][2] = a_t_original[0][2] + noise_t[0][2]

                #ob, r_t, done, info = env.step(a_t[0])

                #s_t1 = np.hstack((ob.angle, ob.track, ob.trackPos, ob.speedX, ob.speedY, ob.speedZ, ob.wheelSpinVel/100.0, ob.rpm))

                self.buff.add(state, chosen_action, reward, s_t1, done)      #Add replay buffer

                #Do the batch update
                batch = self.buff.getBatch(self.BATCH_SIZE)
                states = np.asarray([e[0] for e in batch])
                actions = np.asarray([e[1] for e in batch])
                rewards = np.asarray([e[2] for e in batch])
                new_states = np.asarray([e[3] for e in batch])
                dones = np.asarray([e[4] for e in batch])
                y_t = np.asarray([e[1] for e in batch])

                target_q_values = self.critic.target_model.predict([new_states, self.actor.target_model.predict(new_states)])

                for k in range(len(batch)):
                    if dones[k]:
                        y_t[k] = rewards[k]
                    else:
                        y_t[k] = rewards[k] + self.GAMMA*target_q_values[k]

                if self.train_indicator:
                    loss += self.critic.model.train_on_batch([states,actions], y_t)
                    a_for_grad = self.actor.model.predict(states)
                    grads = self.critic.gradients(states, a_for_grad)
                    self.actor.train(states, grads)
                    self.actor.target_train()
                    self.critic.target_train()

                self.total_reward += r_t
                s_t = s_t1

                print("Episode", i, "Step", step, "Action", a_t, "Reward", r_t, "Loss", loss)

                step += 1
                if done:
                    break

            if np.mod(i, 3) == 0:
                if (train_indicator):
                    print("Now we save model")
                    actor.model.save_weights("actormodel.h5", overwrite=True)
                    with open("actormodel.json", "w") as outfile:
                        json.dump(actor.model.to_json(), outfile)

                    critic.model.save_weights("criticmodel.h5", overwrite=True)
                    with open("criticmodel.json", "w") as outfile:
                        json.dump(critic.model.to_json(), outfile)

            print("TOTAL REWARD @ " + str(i) +"-th Episode  : Reward " + str(total_reward))
            print("Total Step: " + str(step))
            print("")

            if self.step % self.max_steps == 0:
                # Train network
                self.total_reward = 0

        print("Finish.")

