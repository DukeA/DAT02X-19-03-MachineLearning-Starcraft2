
from pysc2.agents import base_agent
from pysc2.lib import actions, units

from Models.BuildOrders.ActionSingelton import ActionSingelton
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

    def build_marines(self, obs, free_supply):
        new_action = [actions.FUNCTIONS.no_op()]

        barracks_location = UnitBuildOrders.findall_barracks(self, obs)
        if self.reqSteps == 0:
            self.reqSteps = 3

        elif self.reqSteps == 3:
            self.reqSteps = 2
            new_action = [
                        actions.FUNCTIONS.move_camera(self.base_location)
                    ]
        elif self.reqSteps == 2:
            self.reqSteps = 1
            barracks = HelperClass.get_units(self, obs, units.Terran.Barracks)
            if len(barracks) > 0:
                    new_action = \
                        [actions.FUNCTIONS.select_point("select_all_type", (HelperClass.sigma(self, barracks[0].x),
                                                                            HelperClass.sigma(self, barracks[0].y)))]
        elif self.reqSteps == 1:
            self.reqSteps=0
            if len(barracks_location) > 0:
                if HelperClass.select_unit(self,obs,units.Terran.Barracks):
                    if HelperClass.do_action(self,obs,actions.FUNCTIONS.Train_Marine_quick.id)\
                        and free_supply > 0:
                        new_action = [actions.FUNCTIONS.Train_Marine_quick("now")]
        ActionSingelton().set_action(new_action)

    def build_marauder(self, obs, free_supply):
        new_action = [actions.FUNCTIONS.no_op()]

        if self.reqSteps == 0:
            self.reqSteps = 3

        if self.reqSteps == 3:
            self.reqSteps = 2
            # or maybe another location if we have one for barracks
            new_action = [actions.FUNCTIONS.move_camera(self.base_location)]

        elif self.reqSteps == 2:
            self.reqSteps = 1
            barracks = HelperClass.get_units(self, obs, units.Terran.Barracks)
            if len(barracks) > 0:
                new_action = \
                    [actions.FUNCTIONS.select_point("select_all_type", (HelperClass.sigma(self, barracks[0].x),
                                                                        HelperClass.sigma(self, barracks[0].y)))]
        elif self.reqSteps == 1:
            self.reqSteps = 0
            if HelperClass.select_unit(self, obs, units.Terran.Barracks):
                if HelperClass.do_action(self, obs, actions.FUNCTIONS.Train_Marauder_quick.id):
                    new_action = [actions.FUNCTIONS.Train_Marauder_quick("now")]
        ActionSingelton().set_action(new_action)

    def build_reaper(self, obs, free_supply):
        new_action = [actions.FUNCTIONS.no_op()]

        if self.reqSteps == 0:
            self.reqSteps = 3

        if self.reqSteps == 3:
            self.reqSteps = 2
            # or maybe another location if we have one for barracks
            new_action = [actions.FUNCTIONS.move_camera(self.base_location)]

        elif self.reqSteps == 2:
            self.reqSteps = 1
            barracks = HelperClass.get_units(self, obs, units.Terran.Barracks)
            if len(barracks) > 0:
                new_action = \
                    [actions.FUNCTIONS.select_point("select_all_type", (HelperClass.sigma(self, barracks[0].x),
                                                                        HelperClass.sigma(self, barracks[0].y)))]
        elif self.reqSteps == 1:
            self.reqSteps = 0
            if HelperClass.select_unit(self, obs, units.Terran.Barracks):
                if HelperClass.do_action(self, obs, actions.FUNCTIONS.Train_Reaper_quick.id):
                    new_action = [actions.FUNCTIONS.Train_Reaper_quick("now")]
        ActionSingelton().set_action(new_action)

    def build_hellion(self, obs, free_supply):
        new_action = [actions.FUNCTIONS.no_op()]

        if self.reqSteps == 0:
            self.reqSteps = 3

        if self.reqSteps == 3:
            self.reqSteps = 2
            # or maybe another location if we have one for barracks
            new_action = [actions.FUNCTIONS.move_camera(self.base_location)]

        elif self.reqSteps == 2:
            self.reqSteps = 1
            factories = HelperClass.get_units(self, obs, units.Terran.Factory)
            if len(factories) > 0:
                new_action = \
                    [actions.FUNCTIONS.select_point("select_all_type", (HelperClass.sigma(self, factories[0].x),
                                                                        HelperClass.sigma(self, factories[0].y)))]
        elif self.reqSteps == 1:
            self.reqSteps = 0
            if HelperClass.select_unit(self, obs, units.Terran.Factory):
                if HelperClass.do_action(self, obs, actions.FUNCTIONS.Train_Hellion_quick.id):
                    new_action = [actions.FUNCTIONS.Train_Hellion_quick("now")]
        ActionSingelton().set_action(new_action)

    def build_medivac(self, obs, free_supply):
        new_action = [actions.FUNCTIONS.no_op()]
        if self.reqSteps == 0:
            self.reqSteps = 3

        if self.reqSteps == 3:
            self.reqSteps = 2
            # or maybe another location if we have one for starport
            new_action = [actions.FUNCTIONS.move_camera(self.base_location)]

        elif self.reqSteps == 2:
            self.reqSteps = 1
            starports = HelperClass.get_units(self, obs, units.Terran.Starport)
            if len(starports) > 0:
                new_action = \
                    [actions.FUNCTIONS.select_point("select_all_type", (HelperClass.sigma(self, starports[0].x),
                                                                        HelperClass.sigma(self, starports[0].y)))]
        elif self.reqSteps == 1:
            self.reqSteps = 0
            if HelperClass.select_unit(self, obs, units.Terran.Starport):
                if HelperClass.do_action(self, obs, actions.FUNCTIONS.Train_Medivac_quick.id):
                    new_action = [actions.FUNCTIONS.Train_Medivac_quick("now")]
        ActionSingelton().set_action(new_action)

    def build_viking(self, obs, free_supply):
        new_action = [actions.FUNCTIONS.no_op()]
        if self.reqSteps == 0:
            self.reqSteps = 3

        if self.reqSteps == 3:
            self.reqSteps = 2
            # or maybe another location if we have one for starport
            new_action = [actions.FUNCTIONS.move_camera(self.base_location)]

        elif self.reqSteps == 2:
            self.reqSteps = 1
            starports = HelperClass.get_units(self, obs, units.Terran.Starport)
            if len(starports) > 0:
                new_action = \
                    [actions.FUNCTIONS.select_point("select_all_type", (HelperClass.sigma(self, starports[0].x),
                                                                        HelperClass.sigma(self, starports[0].y)))]
        elif self.reqSteps == 1:
            self.reqSteps = 0
            if HelperClass.select_unit(self, obs, units.Terran.Starport):
                if HelperClass.do_action(self, obs, actions.FUNCTIONS.Train_VikingFighter_quick.id):
                    new_action = [actions.FUNCTIONS.Train_VikingFighter_quick("now")]
        ActionSingelton().set_action(new_action)

    def transform_viking_to_ground(self, obs):
        """ Transforms all available Vikings to their ground mode (Assault mode)
                :param obs: The observer.
        """
        new_action = [actions.FUNCTIONS.no_op()]
        if self.reqSteps == 0:
            self.reqSteps = 3

        if self.reqSteps == 3:
            if actions.FUNCTIONS.select_army.id in obs.observation.available_actions:
                new_action = [actions.FUNCTIONS.select_army("select")]
                self.reqSteps = 2
            else:
                self.reqSteps = 0

        elif self.reqSteps == 2:
            self.reqSteps = 1
            vikings_air = HelperClass.get_units(self, obs, units.Terran.VikingFighter)
            if len(vikings_air) > 0:
                if HelperClass.do_action(self, obs, actions.FUNCTIONS.select_unit.id):
                    for i in range(len(obs.observation.multi_select)):
                        if obs.observation.multi_select[i].unit_type == units.Terran.VikingFighter:
                            new_action = [actions.FUNCTIONS.select_unit("select_all_type", i)]
                            break

        elif self.reqSteps == 1:
            self.reqSteps = 0
            vikings_air = HelperClass.get_units(self, obs, units.Terran.VikingFighter)
            if len(vikings_air) > 0:
                if HelperClass.do_action(self, obs, actions.FUNCTIONS.Morph_VikingAssaultMode_quick.id):
                    new_action = [actions.FUNCTIONS.Morph_VikingAssaultMode_quick("now")]

        ActionSingelton().set_action(new_action)

    def transform_viking_to_air(self, obs):
        """ Transforms all available Vikings to their air mode (Fighter mode)
                :param obs: The observer.
        """
        new_action = [actions.FUNCTIONS.no_op()]
        if self.reqSteps == 0:
            self.reqSteps = 3

        if self.reqSteps == 3:
            if actions.FUNCTIONS.select_army.id in obs.observation.available_actions:
                new_action = [actions.FUNCTIONS.select_army("select")]
                self.reqSteps = 2
            else:
                self.reqSteps = 0

        elif self.reqSteps == 2:
            self.reqSteps = 1
            vikings_ground = HelperClass.get_units(self, obs, units.Terran.VikingAssault)
            if len(vikings_ground) > 0:
                if HelperClass.do_action(self, obs, actions.FUNCTIONS.select_unit.id):
                    for i in range(len(obs.observation.multi_select)):
                        if obs.observation.multi_select[i].unit_type == units.Terran.VikingAssault:
                            new_action = [actions.FUNCTIONS.select_unit("select_all_type", i)]
                            break

        elif self.reqSteps == 1:
            self.reqSteps = 0
            vikings_ground = HelperClass.get_units(self, obs, units.Terran.VikingAssault)
            if len(vikings_ground) > 0:
                if HelperClass.do_action(self, obs, actions.FUNCTIONS.Morph_VikingFighterMode_quick.id):
                    new_action = [actions.FUNCTIONS.Morph_VikingFighterMode_quick("now")]

        ActionSingelton().set_action(new_action)

    def findall_barracks(self, obs):
        barracks_location = []
        barracks = HelperClass.get_units(self, obs, units.Terran.Barracks)
        for barrack_unit in barracks:
            if HelperClass.not_in_queue(self,obs,units.Terran.Barracks):
                barracks_location.append(barrack_unit)
        return barracks_location
