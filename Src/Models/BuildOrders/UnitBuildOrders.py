
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
                    if obs.observation.multi_select[i].unit_type == units.Terran.Barracks or\
                            obs.observation.multi_select[i].unit_type == units.Terran.BarracksTechLab or\
                            obs.observation.multi_select[i].unit_type == units.Terran.BarracksReactor:
                        new_action = [actions.FUNCTIONS.select_unit("select_all_type", i)]
                        break

        if self.reqSteps == 1:
            if HelperClass.is_unit_selected(self, obs, units.Terran.Barracks) or\
                    HelperClass.is_unit_selected(self, obs, units.Terran.BarracksTechLab) or\
                    HelperClass.is_unit_selected(self, obs, units.Terran.BarracksReactor):
                if HelperClass.do_action(self, obs, actions.FUNCTIONS.Train_Marine_quick.id):
                    new_action = [actions.FUNCTIONS.Train_Marine_quick("now")]
        self.reqSteps -= 1
        ActionSingleton().set_action(new_action)

    def build_marauder(self, obs):
        new_action = [actions.FUNCTIONS.no_op()]

        if self.reqSteps == 0:
            self.reqSteps = 3

        if self.reqSteps == 3:
            new_action = HelperClass.select_all_buildings(self, obs)

        if self.reqSteps == 2:
            if len(obs.observation.multi_select > 0):
                for i in range(len(obs.observation.multi_select)):
                    if obs.observation.multi_select[i].unit_type == units.Terran.BarracksTechLab:
                        new_action = [actions.FUNCTIONS.select_unit("select_all_type", i)]
                        break

        if self.reqSteps == 1:
            if HelperClass.is_unit_selected(self, obs, units.Terran.BarracksTechLab):
                if HelperClass.do_action(self, obs, actions.FUNCTIONS.Train_Marauder_quick.id):
                    new_action = [actions.FUNCTIONS.Train_Marauder_quick("now")]
        self.reqSteps -= 1
        ActionSingleton().set_action(new_action)

    def build_reaper(self, obs):
        new_action = [actions.FUNCTIONS.no_op()]

        if self.reqSteps == 0:
            self.reqSteps = 3

        if self.reqSteps == 3:
            new_action = HelperClass.select_all_buildings(self, obs)

        if self.reqSteps == 2:
            if len(obs.observation.multi_select > 0):
                for i in range(len(obs.observation.multi_select)):
                    if obs.observation.multi_select[i].unit_type == units.Terran.Barracks or \
                            obs.observation.multi_select[i].unit_type == units.Terran.BarracksTechLab or \
                            obs.observation.multi_select[i].unit_type == units.Terran.BarracksReactor:
                        new_action = [actions.FUNCTIONS.select_unit("select_all_type", i)]
                        break

        if self.reqSteps == 1:
            if HelperClass.is_unit_selected(self, obs, units.Terran.Barracks) or \
                    HelperClass.is_unit_selected(self, obs, units.Terran.BarracksTechLab) or \
                    HelperClass.is_unit_selected(self, obs, units.Terran.BarracksReactor):
                if HelperClass.do_action(self, obs, actions.FUNCTIONS.Train_Reaper_quick.id):
                    new_action = [actions.FUNCTIONS.Train_Reaper_quick("now")]
        self.reqSteps -= 1
        ActionSingleton().set_action(new_action)

    def build_hellion(self, obs):
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

    def build_medivac(self, obs):
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

    def build_scv(self, obs):
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

    def build_viking(self, obs):
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
