
import Models.BuildNetwork.BuildFacade as BuildFacade
import tensorflow as tf



class BuildAgent:

    def __init__(self,sess, build_state,action_state, optimizer = tf.train.AdamOptimizer(1e-4)):
        self.sess = sess
        self.build_state = build_state
        self.action_state = action_state
        self.frames = 0
        self.memory = []
        self.reward = 0



    def build_Agent_network(self ):
        self.build_state,self.policy,self.value = BuildFacade
