

from Models.BuildNetwork.BuildModelGather import BuildModelGather
from Models.BuildNetwork.BuildModelLocations import BuildModelLocations
from Models.BuildNetwork.Build_location import  Build_location

from Models.BotFile.State import State


class BuildFacade:
    def __init__(self):
        self.state = State()
        self.build_state = []
        self.build_model = []
        self.value = []
        self.score = 0
        self.total_reward = 0
        self.action_list =[]
        self.n_build_list =[]
        self.good_locations =[]


    def set_up(self, obs):
        BuildFacade.build_state = BuildModelGather.set_locations(self, obs)
        list = BuildFacade.build_state
        BuildFacade.build_model = BuildModelLocations.set_building_location(self, list)
        BuildFacade.n_build_list = BuildFacade.flatten_enviorment (self,BuildFacade.build_model)
        BuildFacade.good_locations = Build_location.get_good_locations(self,BuildFacade.n_build_list)
        BuildFacade.action_list = BuildFacade.set_Actions(self)
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
        Check to normalize the value where it is located
    """
    def normalize_evniorment(self, lists):
        if(len(lists)) <= 0:
            return lists
        n_list = lists
        location =0
        for list in n_list:
            list_value = list
            for unit in list:
                location = location % 82
                if unit == 0:
                    list[location] = 0
                else:
                    value = unit / unit
                    list[location] = value
                location = 1 + location
        return list

    """
        Set All the actions for the build_typ
    """
    def set_Actions(self):
        build_action = [
            "build_supply_depot",
            "build_barracks",
        ]
        return build_action

    """
        An Method which flattens the build_enviorment
    """
    def flatten_enviorment(self, list):
        value_list = []
        if len(list) <= 0:
            return list
        n_list = list
        for lists in n_list:
            for units in lists:
                value_list.append(units)
        return value_list






