

from Models.BuildNetwork.BuildModelGather import BuildModelGather
from Models.BotFile.State import State

class BuildFacade():
    def __init__(self):
        self.state = State()
        self.build_state =[]
        self.build_model =[]


    def set_up(self, obs):
     BuildFacade.build_state = BuildModelGather.set_locations(self,obs)
