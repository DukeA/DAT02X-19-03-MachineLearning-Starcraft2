import random

from pysc2.agents import base_agent
from pysc2.lib import actions, units

from Models.Predefines.Coordinates import Coordinates
from Models.BuildOrders.ActionSingelton import ActionSingelton
from Models.HelperClass.HelperClass import HelperClass

"""
The Class belongs to the Build Order request 
to build certain elements such as supply depots and
refinarys.  
"""

class BuildOrders(base_agent.BaseAgent):
    def __init__(self):
        super(BuildOrders, self).__init__()
        self.base_location = None
        self.expo_loc = 0
        self.new_action = None

    def build_barracks(self, obs):
        new_action = [actions.FUNCTIONS.no_op()]
        if self.reqSteps == 0:
            self.reqSteps = 2

        if self.reqSteps == 2:
            self.reqSteps = 1
            new_action = HelperClass.select_scv(self, obs)

        elif self.reqSteps == 1:
            self.reqSteps = 0
            barracks = HelperClass.get_units(self, obs, units.Terran.Barracks)
            if len(barracks) < 2  and HelperClass.not_in_progress(self, obs, units.Terran.Barracks):
                if HelperClass.select_unit(self, obs, units.Terran.SCV):
                    if HelperClass.do_action(self, obs, actions.FUNCTIONS.Build_Barracks_screen.id):
                        x = Coordinates.BARRACKS_X
                        y = Coordinates.BARRACKS_Y

                        new_action = [actions.FUNCTIONS.Build_Barracks_screen("queued", (x, y))]
        ActionSingelton().set_action(new_action)


    def build_supply_depot(self, obs, free_supply):
        new_action = [actions.FUNCTIONS.no_op()]
        if self.reqSteps == 0:
            self.reqSteps = 2

        if self.reqSteps == 2:
            self.reqSteps = 1
            new_action = HelperClass.select_scv(self, obs)

        elif self.reqSteps == 1:
            self.reqSteps = 0
            supply_depot = HelperClass.get_units(self,obs,units.Terran.SupplyDepot)
            if free_supply <= 4 and len(supply_depot) < 1  and HelperClass.not_in_progress(self, obs, units.Terran.SupplyDepot):
                if HelperClass.select_unit(self, obs, units.Terran.SCV):
                    if HelperClass.do_action(self, obs, actions.FUNCTIONS.Build_SupplyDepot_screen.id):
                        x = random.randint(2, 81)
                        y = random.randint(2, 81)

                        new_action = [actions.FUNCTIONS.Build_SupplyDepot_screen("now", (x, y))]
        ActionSingelton().set_action(new_action)


    def build_refinery(self, obs):
        new_action = [actions.FUNCTIONS.no_op()]
        if self.reqSteps == 0:
            self.reqSteps = 3

        if self.reqSteps == 3:
            self.reqSteps = 2
            new_action = HelperClass.select_scv(self, obs)

        elif self.reqSteps == 2:
            self.reqSteps = 1
            new_action = [
                HelperClass.move_camera_to_base_location(self, obs)]

        elif self.reqSteps == 1:
            self.reqSteps = 0
            if obs.observation.player.food_used >= 20:
                if HelperClass.select_unit(self, obs, units.Terran.SCV):
                    if HelperClass.do_action(self, obs, actions.FUNCTIONS.Build_Refinery_screen.id):
                        geyser = HelperClass.get_units(self, obs, units.Neutral.VespeneGeyser)

                        new_action = [actions.FUNCTIONS.Build_Refinery_screen("now",
                                                                              (HelperClass.sigma(self, geyser[0].x),
                                                                               HelperClass.sigma(self, geyser[0].y)))]
        ActionSingelton().set_action(new_action)


    def build_scv(self, obs, free_supply):
        
        new_action = [actions.FUNCTIONS.no_op()]
        command_centers = HelperClass.get_units(self, obs, units.Terran.CommandCenter)
        if self.reqSteps == 0:
            self.reqSteps = 3

        elif self.reqSteps == 3:
            self.reqSteps = 2
            new_action = [
                HelperClass.move_camera_to_base_location(self, obs)
            ]
        elif self.reqSteps == 2:
            self.reqSteps = 1
            if len(command_centers) > 0:
                new_action = [actions.FUNCTIONS.select_point("select",
                                                             (HelperClass.sigma(self, command_centers[0].x),
                                                              HelperClass.sigma(self, command_centers[0].y)))]
        elif self.reqSteps == 1:
            self.reqSteps = 0
            suv_units = HelperClass.get_units(self,obs,units.Terran.SCV)
            if len(suv_units)< 15:
                if HelperClass.select_unit(self, obs, units.Terran.CommandCenter):
                    if HelperClass.do_action(self, obs, actions.FUNCTIONS.Train_SCV_quick.id
                                         ) and HelperClass.not_in_queue(self, obs, units.Terran.CommandCenter
                                                                        ) and free_supply > 0 and command_centers[0].assigned_harvesters < command_centers[0].ideal_harvesters:
                        new_action = [actions.FUNCTIONS.Train_SCV_quick("now")]
        ActionSingelton().set_action(new_action)



    def return_scv(self, obs):
        new_action = [actions.FUNCTIONS.no_op()]
        if self.reqSteps == 0:
            self.reqSteps = 3

        elif self.reqSteps == 3:
            self.reqSteps = 2
            if(obs.observation.player.idle_worker_count > 0):
                new_action = [actions.FUNCTIONS.select_idle_worker(
                    "select", obs, units.Terran.SCV)]

        elif self.reqSteps == 2:
            self.reqSteps = 1
            new_action = [
                HelperClass.move_camera_to_base_location(self, obs)]

        elif self.reqSteps == 1:
            self.reqSteps = 0
            if HelperClass.select_unit(self, obs, units.Terran.SCV):
                minerals = HelperClass.get_units(self, obs, units.Neutral.MineralField)
                new_action = [actions.FUNCTIONS.Harvest_Gather_screen(
                    "now", (HelperClass.sigma(self, minerals[0].x),
                            HelperClass.sigma(self, minerals[0].y)))]
        ActionSingelton().set_action(new_action)


    def expand(self, obs, top_start):
        new_action = [actions.FUNCTIONS.no_op()]
        if obs.observation.player.minerals >= 400:  # check if it is possible
            if self.reqSteps == 0:
                self.expo_loc = 0
                self.reqSteps = 4

            if self.reqSteps == 4:  # move to base
                new_action = [
                    HelperClass.move_camera_to_base_location(self, obs)]

            if self.reqSteps == 3:  # select scv
                command_scv = HelperClass.get_units(self, obs, units.Terran.SCV)
                if len(command_scv) > 0 and not HelperClass.select_unit(self, obs, units.Terran.SCV):
                    if (obs.observation.player.idle_worker_count > 0):
                        new_action = [actions.FUNCTIONS.select_idle_worker(
                            "select", obs, units.Terran.SCV)]
                    else:
                        command = random.choice(command_scv)
                        new_action = [actions.FUNCTIONS.select_point(
                            "select", (HelperClass.sigma(self, command.x),
                                       HelperClass.sigma(self, command.y)))]

            if self.reqSteps == 2:  # move to expansion location
                target = BuildOrders.choose_location(self, top_start)
                new_action = [
                    actions.FUNCTIONS.move_camera(target)]

            if self.reqSteps == 1:  # check if there is a commandcenter there if there is move to the next location or build one
                command_center = HelperClass.get_units(self, obs, units.Terran.CommandCenter)
                if len(command_center) > 0:
                    if len(Coordinates.EXPO_LOCATIONS) >= self.expo_loc+1:
                        self.reqSteps = 2
                        self.expo_loc += 1
                        if self.expo_loc < len(Coordinates.CC_LOCATIONS):
                            target = BuildOrders.choose_location(self, top_start)
                            new_action = [
                                actions.FUNCTIONS.move_camera(target)]
                        else:
                            self.reqSteps = 1
                else:
                    if HelperClass.select_unit(self, obs, units.Terran.SCV):
                        if HelperClass.do_action(self, obs, actions.FUNCTIONS.Build_CommandCenter_screen.id):
                            target = BuildOrders.choose_screen_location(self, top_start)
                            new_action = [
                                actions.FUNCTIONS.Build_CommandCenter_screen("now", target)]
            self.reqSteps -= 1
        ActionSingelton().set_action(new_action)

    def choose_screen_location(self, top_start):  # returns a location based on the start location
        if top_start:
            return Coordinates().CC_LOCATIONS[self.expo_loc]
        else:
            return Coordinates().CC_LOCATIONS2[self.expo_loc]

    def choose_location(self, top_start):
        value =self.expo_loc
        # returns a location based on the start location
        if top_start:
            return Coordinates().EXPO_LOCATIONS[self.expo_loc]
        else:
            return Coordinates().EXPO_LOCATIONS2[self.expo_loc]

    def build_marine(self, obs, free_supply):
        new_action = [actions.FUNCTIONS.no_op()]
        barracks = HelperClass.get_units(self, obs, units.Terran.Barracks)
        if self.reqSteps == 0:
            self.reqSteps = 3

        elif self.reqSteps == 3:
            self.reqSteps = 2
            new_action = [
                HelperClass.move_camera_to_base_location(self, obs)
            ]

        elif self.reqSteps == 2:
            self.reqSteps = 1
            if len(barracks) > 0:
                new_action = [actions.FUNCTIONS.select_point("select",
                                                             (HelperClass.sigma(self, barracks[0].x),
                                                              HelperClass.sigma(self, barracks[0].y)))]

        elif self.reqSteps == 1:
            self.reqSteps = 0
            if HelperClass.select_unit(self, obs, units.Terran.Barracks):
                if HelperClass.do_action(self, obs, actions.FUNCTIONS.Train_Marine_quick.id
                                         ) and HelperClass.not_in_queue(self, obs, units.Terran.Barracks
                                                                        ) and free_supply > 0:
                    new_action = [actions.FUNCTIONS.Train_Marine_quick("now")]

        return new_action






 
