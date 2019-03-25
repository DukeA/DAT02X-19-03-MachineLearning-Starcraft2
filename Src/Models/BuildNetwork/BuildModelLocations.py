import numpy as np

class BuildModelLocations:


    def __init__(self,state):
        self.reward = state.reward



    def set_building_location(self, build_state):
         view = BuildModelLocations.set_buildlocations(self)
         build_place = []
         x = len(build_state)
         y = len(build_state[0])
         for i in range(x):
             for j in range(y):
                if j <= 41 and i <= 41:
                    if build_state[i][j] == 0:
                        view[i][j] = 10
                    else:
                        view[i][j] = build_state[i][j]
                elif j >= 41 and i >= 41:
                    if build_state[i][j] == 0:
                        view[i][j] = 5
                    else:
                        view[i][j] =build_state[i][j]
                elif j <= 41 and i >= 41:
                    if build_state[i][j] == 0:
                        view[i][j] = 5
                    else:
                        view[i][j] = build_state[i][j]
                else:
                    view[i][j] = build_state[i][j]
         return view


    def check_startLocation_Of_Base(self):


    def set_buildlocations(self):
        viewlist = np.full((82, 82), 0)
        return viewlist
