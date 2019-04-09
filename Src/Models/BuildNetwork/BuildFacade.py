

from Models.BuildNetwork.BuildModelGather import BuildModelGather
from Models.BuildNetwork.BuildModelLocations import BuildModelLocations
from Models.BuildNetwork.BuildNetwork import BuildNetwork
from Models.BotFile.State import State

STACKED_VALUES = 4

class BuildFacade():
    def __init__(self):
        self.state = State()
        self.build_state =[]
        self.build_model =[]
        self.value =[]
        self.score = 0
        self.total


    def set_up(self, obs):
        BuildFacade.build_state = BuildModelGather.set_locations(self, obs)
        list = BuildFacade.build_state
        BuildFacade.build_model = BuildModelLocations.set_building_location(self, list)

    """
        An method for printing out the  environment on the screen
    """
    def print_enviroment(self, list):
        value = 0
        for i in list:
            if value % 82 == 0:
                print("\n")
            print(i, end="")
            value = value + 1

    """
        Stacked the frames for the  list which is entered
    """
    def stacked_enviorment(self, list):
        if len(list) <= 0:
            return list
        n_list = list
        result = []
        for i in range(STACKED_VALUES):
            result.append(i)
        return result


