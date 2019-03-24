import numpy as np

class BuildModelLocations:


    def __init__(self,state):
        self.reward = state.reward



    def set_building_location(self, build_state):
         view = BuildModelLocations.set_buildlocations(self)
         build_place = []
         for i in range(build_state):
             for  j in range(build_state):
                if build_state[i][j] == 0:
                    view[i][j]= 1
                elif build_state[i][j] != 0:
                    view[i][j] = -1
         return view


    def set_buildlocations(self):
        viewlist = np.full((82, 82), 0)
        return viewlist
