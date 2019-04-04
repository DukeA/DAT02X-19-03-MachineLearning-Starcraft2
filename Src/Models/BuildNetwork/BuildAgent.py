



class BuildAgent:

    def __init__(self,sess, build_state,action_state, optimizer):
        self.sess = sess
        self.build_state = build_state
        self.action_state = action_state

