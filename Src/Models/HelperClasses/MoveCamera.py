from pysc2.agents import base_agent
from pysc2.lib import actions

from Models.Predefines.Coordinates import Coordinates

"""
Helper class that moves the camera.
"""

class MoveCamera(base_agent.BaseAgent):

    #Moves to camera to a standard location defined in Models.Predefines.Coordinates 
    def move_camera_to_standard_location(self, obs):
        return actions.FUNCTIONS.move_camera(Coordinates.CAMERA_STANDARD_LOCATION)
