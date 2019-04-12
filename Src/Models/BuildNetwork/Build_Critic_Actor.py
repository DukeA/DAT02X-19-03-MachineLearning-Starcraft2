

from keras.layers import Dense,Input
from keras.models import Model
from keras.backend as Backend
import tensorflow as tf
from keras.optimizers import Adam

class Build_Critic_Actor:

    def __init__(self,sess, build_model,action_model,Learning_rate,
                 Batch_size, Tau):
        self.sess = sess
        self.build_model = build_model
        self.action_model = action_model
        self.Learning_rate = Learning_rate
        self.Batch_size = Batch_size
        self.Tau = Tau

        Backend.set_session(sess)
        self.crtic_model,self.crtic_state,\
        self.crtic_output,self.crtic_weight = Build_Critic_Actor.create_crtic_model(self,build_model,action_model)
        self.target_actor = tf.placeholder(tf.float32)
        self.crtic_build_optimizer = Adam(lr = self.learning_rate)
        self.model.compile(optmizer = self.crtic_build_optimizer,loss ='mse')


    def create_crtic_model(self,build_model,action_state):
        build_crtic_model_state = Input(shape=build_model)
        hidden_layer1 = Dense(600, activation='relu', kernel_initializer='random_normal')(build_crtic_model_state)
        hidden_layer2 = Dense(300, activation='relu', kernel_initializer='random_normal')(hidden_layer1)
        build_crtic_action_state = Dense(action_state, activation='linear', kernel_initializer='random_normal')(hidden_layer2)
        build_crtic_model = Model(input=build_crtic_model_state, output=action_state)
        return build_crtic_model_state, build_crtic_model, \
               build_crtic_action_state, build_crtic_model.trainable_weights

    def train_crtic(self,build_state,action_state):
        self.sess.run(self.optimaize ,feed_dict ={
            self.build_states : build_state,
            self.build_action_state :action_state
        })

    def update_crtic_weights (self):
        build_crtic_weights = self.crtic_model.getWeights()
        build_target_weights = self.target_actor.get_weights()
        for i in range(len(build_crtic_weights)):
            build_target_weights[i] = self.Tau *build_target_weights[i] + (1-self.Tau)*build_target_weights[i]
        self.target_actor.set_weights(build_target_weights)

    def load_weights(self,path):
        self.crtic_model.load_weights(path)

    def save_weights(self,path):
        self.crtic_model.save_weights(path + 'crtic_build_actor.h5')








