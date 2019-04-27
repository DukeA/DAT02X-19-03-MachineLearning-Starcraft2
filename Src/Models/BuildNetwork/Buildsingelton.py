
from Models.BuildOrders.Singelton import Singelton

"""
    An singelton class for getting the x and y coordinates
"""

class Buildsingelton( metaclass=Singelton):
    def __init__(self):
        super(Buildsingelton,self).__init__()
        self.location = []

    def get_location(self):
        return self.location

    def set_location(self, x, y):
        self.location.append(x)
        self.location.append(y)
