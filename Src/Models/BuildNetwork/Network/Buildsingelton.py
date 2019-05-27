
from Models.HelperClass.Singelton import Singelton

"""
    An singelton class for getting all the x and y coordinates
"""

class Buildsingelton( metaclass=Singelton):
    def __init__(self):
        super(Buildsingelton,self).__init__()
        self.build_location = []

    def get_location(self):
        return self.build_location

    def set_location(self, build_location):
        self.build_location = build_location
