
from pysc2.agents import base_agent
from pysc2.lib import actions, units

from Models.BuildOrders.ActionSingleton import ActionSingleton
from Models.HelperClass.HelperClass import HelperClass
import random

"""
@Author :Adam Grandén
The UnitBuildOrders  is the class which builds units
from the specfic infrastrucutre in this case to build marines from barracks
"""


class UnitBuildOrders(base_agent.BaseAgent):
    def __init__(self):
        super(UnitBuildOrders, self).__init__()
        self.new_action = None

    def build_marines(self, obs):
        new_action = [actions.FUNCTIONS.no_op()]

        barracks_location = UnitBuildOrders.findall_barracks(self, obs)

        if self.reqSteps == 0:
            self.reqSteps = 3

        elif self.reqSteps == 3:
            new_action = [
                        actions.FUNCTIONS.move_camera(self.base_location)
                    ]
        elif self.reqSteps == 2:
            barracks = HelperClass.get_units(self, obs, units.Terran.Barracks)
            if len(barracks) > 0:
                    new_action = \
                        [actions.FUNCTIONS.select_point("select_all_type", (HelperClass.sigma(self, barracks[0].x),
                                                                            HelperClass.sigma(self, barracks[0].y)))]
        elif self.reqSteps == 1:
            if len(barracks_location) > 0:
                if HelperClass.is_unit_selected(self, obs, units.Terran.Barracks):
                    if HelperClass.do_action(self,obs,actions.FUNCTIONS.Train_Marine_quick.id):
                            new_action = [actions.FUNCTIONS.Train_Marine_quick("now")]

        self.reqSteps -= 1
        ActionSingleton().set_action(new_action)

    def build_marauder(self, obs, free_supply):
        new_action = [actions.FUNCTIONS.no_op()]

        if self.reqSteps == 0:
            self.reqSteps = 3

        if self.reqSteps == 3:
            # or maybe another location if we have one for barracks
            new_action = [actions.FUNCTIONS.move_camera(self.base_location)]

        elif self.reqSteps == 2:
            barracks = HelperClass.get_units(self, obs, units.Terran.Barracks)
            if len(barracks) > 0:
                new_action = \
                    [actions.FUNCTIONS.select_point("select_all_type", (HelperClass.sigma(self, barracks[0].x),
                                                                        HelperClass.sigma(self, barracks[0].y)))]
        elif self.reqSteps == 1:
            if HelperClass.is_unit_selected(self, obs, units.Terran.Barracks):
                if HelperClass.do_action(self, obs, actions.FUNCTIONS.Train_Marauder_quick.id):
                    new_action = [actions.FUNCTIONS.Train_Marauder_quick("now")]

        self.reqSteps -= 1
        ActionSingleton().set_action(new_action)

    def build_medivac(self, obs, free_supply):
        new_action = [actions.FUNCTIONS.no_op()]

        if self.reqSteps == 0:
            self.reqSteps = 3

        if self.reqSteps == 3:
            # or maybe another location if we have one for starport
            new_action = [actions.FUNCTIONS.move_camera(self.base_location)]

        elif self.reqSteps == 2:
            starports = HelperClass.get_units(self, obs, units.Terran.Starport)
            if len(starports) > 0:
                new_action = \
                    [actions.FUNCTIONS.select_point("select_all_type", (HelperClass.sigma(self, starports[0].x),
                                                                        HelperClass.sigma(self, starports[0].y)))]
        elif self.reqSteps == 1:
            if HelperClass.is_unit_selected(self, obs, units.Terran.Starport):
                if HelperClass.do_action(self, obs, actions.FUNCTIONS.Train_Medivac_quick.id):
                    new_action = [actions.FUNCTIONS.Train_Medivac_quick("now")]
        self.reqSteps -= 1
        ActionSingleton().set_action(new_action)

    def build_scv(self, obs, free_supply):
        new_action = [actions.FUNCTIONS.no_op()]
        command_centers = HelperClass.get_units(self, obs, units.Terran.CommandCenter)

        if self.reqSteps == 0:
            self.reqSteps = 3

        elif self.reqSteps == 3:
            new_action = [
                HelperClass.move_camera_to_base_location(self, obs)
            ]
        elif self.reqSteps == 2:
            if len(command_centers) > 0:
                new_action = [actions.FUNCTIONS.select_point("select",
                                                             (HelperClass.sigma(self, command_centers[0].x),
                                                              HelperClass.sigma(self, command_centers[0].y)))]
        elif self.reqSteps == 1:
            suv_units = HelperClass.get_units(self, obs, units.Terran.SCV)
            if len(suv_units) < 15:
                if HelperClass.is_unit_selected(self, obs, units.Terran.CommandCenter):
                    if HelperClass.do_action(self, obs, actions.FUNCTIONS.Train_SCV_quick.id
                                             ) and HelperClass.not_in_queue(self, obs, units.Terran.CommandCenter
                                                                            ) and free_supply > 0 and command_centers[0].assigned_harvesters < command_centers[0].ideal_harvesters:
                        new_action = [actions.FUNCTIONS.Train_SCV_quick("now")]
        self.reqSteps -= 1
        ActionSingleton().set_action(new_action)

    def findall_barracks(self, obs):
        barracks_location = []
        barracks = HelperClass.get_units(self, obs, units.Terran.Barracks)
        for barrack_unit in barracks:
            if HelperClass.not_in_queue(self,obs,units.Terran.Barracks):
                barracks_location.append(barrack_unit)
        return barracks_location
