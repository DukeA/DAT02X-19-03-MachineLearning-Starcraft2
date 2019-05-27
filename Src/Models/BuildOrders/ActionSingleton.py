
from Models.HelperClass.Singelton import Singelton

"""
The class is a singleton pattern to get the actions to the ai robot.
"""


class ActionSingleton(metaclass=Singelton):

    def __init__(self):
        super(ActionSingleton, self).__init__()
        self.new_action = None

    def get_action(self):
        return self.new_action

    def set_action(self, action):
        self.new_action = action
