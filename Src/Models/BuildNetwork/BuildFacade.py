

from Models.BuildNetwork.BuildModelGather import BuildModelGather
from Models.BuildNetwork.BuildModelLocations import BuildModelLocations
from Models.BotFile.State import State



class BuildFacade():
    def __init__(self):
        self.state = State()
        self.build_state =[]
        self.build_model =[]


    def set_up(self, obs):
     BuildFacade.build_state = BuildModelGather.set_locations(self , obs)
    # BuildFacade.build_model = BuildModelLocations.set_building_location(self , obs,  BuildFacade.build_state)
