import numpy as np
from Models.BuildNetwork.BuildModelGather import BuildModelGather
from Models.BuildNetwork.BuildModelLocations import BuildModelLocations
from Models.BuildNetwork.Build_location import Build_location

from Models.BotFile.State import State


class BuildFacade:
    def __init__(self):
        self.state = State()
        self.build_state = []
        self.build_model = []
        self.value = []
        self.score = 0
        self.total_reward = 0
        self.action_list = []
        self.good_locations = []
        self.oldScore = 0

    def set_up(self, obs):
        build_state = BuildModelGather.set_locations(self, obs)
        list = build_state
        flatten_list = BuildFacade.flatten_list(self, list)
        BuildFacade.build_model = BuildModelLocations.set_building_location(self, list)
        good_locations = Build_location.get_good_locations(self, BuildFacade.build_model)
        action_list = BuildFacade.set_Actions(self)
        oldScore = self.oldScore
        score = obs.observation.score_cumulative.score
        if score != oldScore:
            self.reward = (score - self.oldScore) / 200
        else:
            self.reward = 0
        return np.array([[
            good_locations, flatten_list, action_list]]), \
               oldScore, obs.observation.feature_minimap.player_relative

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
        if (len(lists)) <= 0:
            return lists
        n_list = lists
        location = 0
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

    def flatten_list(self, list):
        if len(list) <= 0:
            return []
        n_list = []
        for list_row in list:
            for list_col in list_row:
                n_list.append(list_col)
        return n_list
