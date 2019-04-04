

class CriticBuildAgent:

    def __init__(self, build_dim,build_out_dim,network,learning_rate):
        BuildAgent.__init__()
        self.build = self.addHead(network)
