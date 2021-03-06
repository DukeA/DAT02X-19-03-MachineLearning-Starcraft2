import numpy as np

from Models.BuildNetwork.BuildingTerranQueue import BuildingTerranQueue

"""
    The class takes a value form the enviroment 
    and places the locations where the bot should place the builiding
"""


class BuildModelLocations:

    def __init__(self, state):
        self.reward = state.reward

    """
    :param An array of the environment
        It takes the environment and returns an new environment where the 
        bot should place the object in this case.
    """

    def set_building_location(self, obs, build_state):
        view = BuildModelLocations.set_buildlocations(self)
        x = len(build_state)
        y = len(build_state[0])
        height_map = obs.observation.feature_screen.height_map
        for i in range(x):
            for j in range(y):
                if BuildModelLocations.check_startLocation_Of_Base(self, build_state):
                    if height_map[i][j] == 255:
                        if (j >= 41 and i >= 41) or (j >= 41 and i <= 41) or (j <= 41 and i >= 41):
                            if build_state[i][j] == 0:
                                view[i][j] = 1
                            elif build_state[i][j] != 0:
                                view[i][j] = 0
                    else:
                        view[i][j] = -1
                else:
                    if height_map[i][j] == 255:
                        if (j <= 41 and i <= 41) or (j >= 41 and i <= 41) or (j <= 41 and i >= 41):
                            if build_state[i][j] == 0:
                                view[i][j] = 1
                            elif build_state[i][j] != 0:
                                view[i][j] = 0
                    else:
                        view[i][j] = -1
        return view

    """
        :param takes in a value of list 
            The class takes in a value of a list and then flattens 
            the value of that list into a single list.
    """

    def flatten_values(self, list):
        n_list = []
        for i in list:
            for j in i:
                n_list.append(j)
        return n_list

    """
        :param build_state, An Array with the all the locations
        The method works by checking if the middle section for the   

    """

    def check_startLocation_Of_Base(self, build_state):
        if build_state[41][41] == BuildingTerranQueue.commandcenter.value:
            return True
        else:
            return False

    """
        The method creates an array of arrays 
        which are 82* 82 big for the array
    """

    def set_buildlocations(self):
        viewlist = np.full((82, 82), 0)
        return viewlist
