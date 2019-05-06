
from Models.HelperClass.Singelton import Singelton

"""
    An singelton class for getting the x and y coordinates
"""

class Buildsingelton( metaclass=Singelton):
    def __init__(self):
        super(Buildsingelton,self).__init__()
        self.location_x = -1
        self.location_y = -1

    def get_location(self):
        return self.location_x,self.location_y

    def set_location(self, x, y):
        self.location_x = x
        self.location_y = y
