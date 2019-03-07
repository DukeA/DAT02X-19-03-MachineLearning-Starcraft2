
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

        if self.reqSteps == 0:
            self.reqSteps = 3

        if self.reqSteps == 3:
            new_action = HelperClass.select_all_buildings(self, obs)

        if self.reqSteps == 2:
            if len(obs.observation.multi_select > 0):
                for i in range(len(obs.observation.multi_select)):
                    if obs.observation.multi_select[i].unit_type == units.Terran.Barracks:
                        new_action = [actions.FUNCTIONS.select_unit("select_all_type", i)]
                        break

        if self.reqSteps == 1:
            if HelperClass.is_unit_selected(self, obs, units.Terran.Barracks):
                if HelperClass.do_action(self, obs, actions.FUNCTIONS.Train_Marine_quick.id):
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

    def build_reaper(self, obs, free_supply):
        new_action = [actions.FUNCTIONS.no_op()]

        if self.reqSteps == 0:
            self.reqSteps = 3

        if self.reqSteps == 3:
            new_action = HelperClass.select_all_buildings(self, obs)

        if self.reqSteps == 2:
            if len(obs.observation.multi_select > 0):
                for i in range(len(obs.observation.multi_select)):
                    if obs.observation.multi_select[i].unit_type == units.Terran.Barracks:
                        new_action = [actions.FUNCTIONS.select_unit("select_all_type", i)]
                        break

        if self.reqSteps == 1:
            if HelperClass.is_unit_selected(self, obs, units.Terran.Barracks):
                if HelperClass.do_action(self, obs, actions.FUNCTIONS.Train_Reaper_quick.id):
                    new_action = [actions.FUNCTIONS.Train_Marine_quick("now")]
        self.reqSteps -= 1
        ActionSingleton().set_action(new_action)

    def build_hellion(self, obs, free_supply):
        new_action = [actions.FUNCTIONS.no_op()]

        if self.reqSteps == 0:
            self.reqSteps = 3

        if self.reqSteps == 3:
            new_action = HelperClass.select_all_buildings(self, obs)

        if self.reqSteps == 2:
            if len(obs.observation.multi_select > 0):
                for i in range(len(obs.observation.multi_select)):
                    if obs.observation.multi_select[i].unit_type == units.Terran.Factory:
                        new_action = [actions.FUNCTIONS.select_unit("select_all_type", i)]
                        break

        if self.reqSteps == 1:
            if HelperClass.is_unit_selected(self, obs, units.Terran.Factory):
                if HelperClass.do_action(self, obs, actions.FUNCTIONS.Train_Hellion_quick.id):
                    new_action = [actions.FUNCTIONS.Train_Hellion_quick("now")]
        self.reqSteps -= 1
        ActionSingleton().set_action(new_action)

    def build_medivac(self, obs, free_supply):
        new_action = [actions.FUNCTIONS.no_op()]

        if self.reqSteps == 0:
            self.reqSteps = 3

        if self.reqSteps == 3:
            new_action = HelperClass.select_all_buildings(self, obs)

        if self.reqSteps == 2:
            if len(obs.observation.multi_select > 0):
                for i in range(len(obs.observation.multi_select)):
                    if obs.observation.multi_select[i].unit_type == units.Terran.Starport:
                        new_action = [actions.FUNCTIONS.select_unit("select_all_type", i)]
                        break

        if self.reqSteps == 1:
            if HelperClass.is_unit_selected(self, obs, units.Terran.Starport):
                if HelperClass.do_action(self, obs, actions.FUNCTIONS.Train_Medivac_quick.id):
                    new_action = [actions.FUNCTIONS.Train_Medivac_quick("now")]
        self.reqSteps -= 1
        ActionSingleton().set_action(new_action)

    def build_scv(self, obs, free_supply):
        new_action = [actions.FUNCTIONS.no_op()]

        if self.reqSteps == 0:
            self.reqSteps = 3

        if self.reqSteps == 3:
            new_action = HelperClass.select_all_buildings(self, obs)

        if self.reqSteps == 2:
            if len(obs.observation.multi_select > 0):
                for i in range(len(obs.observation.multi_select)):
                    if obs.observation.multi_select[i].unit_type == units.Terran.CommandCenter:
                        new_action = [actions.FUNCTIONS.select_unit("select_all_type", i)]
                        break

        if self.reqSteps == 1:
            if HelperClass.is_unit_selected(self, obs, units.Terran.CommandCenter):
                if HelperClass.do_action(self, obs, actions.FUNCTIONS.Train_SCV_quick.id):
                    new_action = [actions.FUNCTIONS.Train_SCV_quick("now")]
        self.reqSteps -= 1
        ActionSingleton().set_action(new_action)

    def build_viking(self, obs, free_supply):
        new_action = [actions.FUNCTIONS.no_op()]

        if self.reqSteps == 0:
            self.reqSteps = 3

        if self.reqSteps == 3:
            new_action = HelperClass.select_all_buildings(self, obs)

        if self.reqSteps == 2:
            if len(obs.observation.multi_select > 0):
                for i in range(len(obs.observation.multi_select)):
                    if obs.observation.multi_select[i].unit_type == units.Terran.Starport:
                        new_action = [actions.FUNCTIONS.select_unit("select_all_type", i)]
                        break

        if self.reqSteps == 1:
            if HelperClass.is_unit_selected(self, obs, units.Terran.Starport):
                if HelperClass.do_action(self, obs, actions.FUNCTIONS.Train_VikingFighter_quick.id):
                    new_action = [actions.FUNCTIONS.Train_VikingFighter_quick("now")]
        self.reqSteps -= 1
        ActionSingleton().set_action(new_action)

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
            vikings_air = [vikings for vikings in obs.observation.multi_select
                           if vikings.unit_type == units.Terran.VikingFighter]
            if len(vikings_air) > 0:
                if HelperClass.do_action(self, obs, actions.FUNCTIONS.select_unit.id):
                    for i in range(len(obs.observation.multi_select)):
                        if obs.observation.multi_select[i].unit_type == units.Terran.VikingFighter:
                            new_action = [actions.FUNCTIONS.select_unit("select_all_type", i)]
                            break

        elif self.reqSteps == 1:
            self.reqSteps = 0
            vikings_air = [vikings for vikings in obs.observation.multi_select
                           if vikings.unit_type == units.Terran.VikingFighter]
            if len(vikings_air) > 0:
                if HelperClass.do_action(self, obs, actions.FUNCTIONS.Morph_VikingAssaultMode_quick.id):
                    new_action = [actions.FUNCTIONS.Morph_VikingAssaultMode_quick("now")]

        ActionSingleton().set_action(new_action)

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
            vikings_ground = [vikings for vikings in obs.observation.multi_select
                              if vikings.unit_type == units.Terran.VikingAssault]
            if len(vikings_ground) > 0:
                if HelperClass.do_action(self, obs, actions.FUNCTIONS.select_unit.id):
                    for i in range(len(obs.observation.multi_select)):
                        if obs.observation.multi_select[i].unit_type == units.Terran.VikingAssault:
                            new_action = [actions.FUNCTIONS.select_unit("select_all_type", i)]
                            break

        elif self.reqSteps == 1:
            self.reqSteps = 0
            vikings_ground = [vikings for vikings in obs.observation.multi_select
                              if vikings.unit_type == units.Terran.VikingAssault]
            if len(vikings_ground) > 0:
                if HelperClass.do_action(self, obs, actions.FUNCTIONS.Morph_VikingFighterMode_quick.id):
                    new_action = [actions.FUNCTIONS.Morph_VikingFighterMode_quick("now")]

        ActionSingleton().set_action(new_action)

    def findall_barracks(self, obs):
        barracks_location = []
        barracks = HelperClass.get_units(self, obs, units.Terran.Barracks)
        for barrack_unit in barracks:
            if HelperClass.not_in_queue(self,obs,units.Terran.Barracks):
                barracks_location.append(barrack_unit)
        return barracks_location
