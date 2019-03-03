import random

from pysc2.agents import base_agent
from pysc2.lib import actions, units

from Models.Predefines.Coordinates import Coordinates
from Models.BuildOrders.ActionSingelton import ActionSingelton

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


        """
            @Author:Arvid , revised :Adam Grandén
            @:param The parameter would be  self which is a aibot
            @:param The other would be the observable universe
            This method would be the barracks which builds the barrack from the start of the base_location 
            and gets an instance where to build that barrack on that location.
        
        """

    def build_barracks(self, obs):
        new_action = [actions.FUNCTIONS.no_op()]
        if self.reqSteps == 0:
            self.reqSteps = 3

        elif self.reqSteps == 3:
            self.reqSteps = 2
            new_action = BuildOrders.select_scv(self, obs)

        elif self.reqSteps == 2:
            self.reqSteps = 1
            new_action = [
                actions.FUNCTIONS.move_camera(self.base_location)]

        elif self.reqSteps == 1:
            self.reqSteps = 0
            if BuildOrders.not_in_progress(self, obs, units.Terran.Barracks):
                if BuildOrders.select_unit(self, obs, units.Terran.SCV):
                    if BuildOrders.do_action(self, obs, actions.FUNCTIONS.Build_Barracks_screen.id):
                        x = random.randint(2, 81)
                        y = random.randint(2, 81)
                        new_action = [actions.FUNCTIONS.Build_Barracks_screen("now", (x, y))]
        ActionSingelton().set_action(new_action)


    def build_supply_depot(self, obs, free_supply):
        new_action = [actions.FUNCTIONS.no_op()]
        if self.reqSteps == 0:
            self.reqSteps = 2

        if self.reqSteps == 2:
            self.reqSteps = 1
            new_action = BuildOrders.select_scv(self, obs)


        elif self.reqSteps == 1:
            self.reqSteps = 0
            if free_supply <= 4  and BuildOrders.not_in_progress(self, obs, units.Terran.SupplyDepot):
                if BuildOrders.select_unit(self, obs, units.Terran.SCV):
                    if BuildOrders.do_action(self, obs, actions.FUNCTIONS.Build_SupplyDepot_screen.id):
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
            new_action = BuildOrders.select_scv(self, obs)

        elif self.reqSteps == 2:
            self.reqSteps = 1
            new_action = [
                actions.FUNCTIONS.move_camera(self.base_location)]

        elif self.reqSteps == 1:
            self.reqSteps = 0
            if obs.observation.player.food_used >= 20:
                if BuildOrders.select_unit(self, obs, units.Terran.SCV):
                    if BuildOrders.do_action(self, obs, actions.FUNCTIONS.Build_Refinery_screen.id):
                        geyser = BuildOrders.get_units(self, obs, units.Neutral.VespeneGeyser)

                        new_action = [actions.FUNCTIONS.Build_Refinery_screen("now",
                                                                              (BuildOrders.sigma(self, geyser[0].x),
                                                                               BuildOrders.sigma(self, geyser[0].y)))]
        ActionSingelton().set_action(new_action)


    def build_scv(self, obs, free_supply):
        new_action = [actions.FUNCTIONS.no_op()]
        command_centers = BuildOrders.get_units(self, obs, units.Terran.CommandCenter)
        if self.reqSteps == 0:
            self.reqSteps = 3

        elif self.reqSteps == 3:
            self.reqSteps = 2
            new_action = [
                actions.FUNCTIONS.move_camera(self.base_location)
            ]
        elif self.reqSteps == 2:
            self.reqSteps = 1
            if len(command_centers) > 0:
                new_action = [actions.FUNCTIONS.select_point("select",
                                                             (BuildOrders.sigma(self, command_centers[0].x),
                                                              BuildOrders.sigma(self, command_centers[0].y)))]
        elif self.reqSteps == 1:
            self.reqSteps = 0
            suv_units = BuildOrders.get_units(self,obs,units.Terran.SCV)
            if len(suv_units)< 15:
                if BuildOrders.select_unit(self, obs, units.Terran.CommandCenter):
                    if BuildOrders.do_action(self, obs, actions.FUNCTIONS.Train_SCV_quick.id
                                         ) and BuildOrders.not_in_queue(self, obs, units.Terran.CommandCenter
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
                actions.FUNCTIONS.move_camera(self.base_location)]

        elif self.reqSteps == 1:
            self.reqSteps = 0
            if BuildOrders.select_unit(self, obs, units.Terran.SCV):
                minerals = BuildOrders.get_units(self, obs, units.Neutral.MineralField)
                new_action = [actions.FUNCTIONS.Harvest_Gather_screen(
                    "now", (BuildOrders.sigma(self, minerals[0].x),
                            BuildOrders.sigma(self, minerals[0].y)))]
        ActionSingelton().set_action(new_action)


    """
        @Author Adam Grandén 
        @:param self- Object aibot
        @:param obs - the observable universe 
        The following code is the action for building an factory this is made from taking the builder 
        then move to the loaction and then get if there was any  other factories being built and return 
        a new build for factory.  
    """
    def build_factory(self, obs):
        new_action = [actions.FUNCTIONS.no_op()]
        if self.reqSteps == 0:
            self.reqSteps = 3

        elif self.reqSteps == 3:
            self.reqSteps = 2
            new_action = [
                actions.FUNCTIONS.move_camera(self.base_location)]


        elif self.reqSteps == 2:
            self.reqSteps = 1
            new_action = BuildOrders.select_scv(self, obs)

        elif self.reqSteps == 1:
            self.reqSteps = 0
            if BuildOrders.not_in_progress(self, obs, units.Terran.Factory):
                if BuildOrders.select_unit(self, obs, units.Terran.SCV):
                    if BuildOrders.do_action(self, obs, actions.FUNCTIONS.Build_Factory_screen.id):
                        x = random.randint(2, 81)
                        y = random.randint(2, 81)
                        new_action =[actions.FUNCTIONS.Build_Factory_screen("now", (x, y))]
        ActionSingelton().set_action( new_action)

        """
            @Author Adam Grandén 
            @:param self-Object aibot
            @:param obs - the observable universe 
            The following code is the action for building an Starport this is made from taking the builder 
            then move to the loaction and then get if there was any  other factories being built and return 
            a new build for starport.  
        """
    def build_starport (self,obs):
        new_action = [actions.FUNCTIONS.no_op()]
        if self.reqSteps == 0:
            self.reqSteps = 3

        elif self.reqSteps == 3:
            self.reqSteps = 2
            new_action = [
                actions.FUNCTIONS.move_camera(self.base_location)]

        elif self.reqSteps == 2:
            self.reqSteps = 1
            new_action = BuildOrders.select_scv(self, obs)

        elif self.reqSteps == 1:
            self.reqSteps = 0
            if BuildOrders.not_in_progress(self, obs, units.Terran.Starport):
                if BuildOrders.select_unit(self, obs, units.Terran.SCV):
                    if BuildOrders.do_action(self, obs, actions.FUNCTIONS.Build_Starport_screen.id):
                        x = random.randint(2, 81)
                        y = random.randint(2, 81)
                        new_action = [actions.FUNCTIONS.Build_Starport_screen("now", (x, y))]
        ActionSingelton().set_action( new_action)

        """
            @Author Adam Grandén 
            @:param self- Object aibot
            @:param obs - the observable universe 
            This code takes the  barracks which are located and then adds 
            an  techlab when the building is built.
        """
    def upgrade_barracks(self, obs):
        new_action = [actions.FUNCTIONS.no_op()]
        barracks = BuildOrders.get_units(self, obs, units.Terran.Barracks)

        if self.reqSteps == 0:
            self.reqSteps = 3

        elif self.reqSteps == 3:
            self.reqSteps = 2
            new_action = [
                actions.FUNCTIONS.move_camera(self.base_location)]

        elif self.reqSteps == 2:
            self.reqSteps = 1
            if len(barracks) > 0 and BuildOrders.not_in_progress(self, obs, units.Terran.Barracks):
                new_action = [actions.FUNCTIONS.select_point("select",
                                                             (BuildOrders.sigma(self, barracks[0].x),
                                                              BuildOrders.sigma(self, barracks[0].y)))]
        elif self.reqSteps == 1:
            self.reqSteps = 0
            if len(barracks) > 0:
                if BuildOrders.select_unit(self, obs, units.Terran.Barracks):
                    if BuildOrders.do_action(self, obs, actions.FUNCTIONS.Build_TechLab_quick.id):
                        new_action = [actions.FUNCTIONS.Build_TechLab_quick("now")]
        ActionSingelton().set_action(new_action)

    def expand(self, obs, top_start):
        new_action = [actions.FUNCTIONS.no_op()]
        if obs.observation.player.minerals >= 400:  # check if it is possible
            if self.reqSteps == 0:
                self.expo_loc = 0
                self.reqSteps = 4

            if self.reqSteps == 4:  # move to base
                new_action = [
                    actions.FUNCTIONS.move_camera(self.base_location)]

            if self.reqSteps == 3:  # select scv
                command_scv = BuildOrders.get_units(self, obs, units.Terran.SCV)
                if len(command_scv) > 0 and not BuildOrders.select_unit(self, obs, units.Terran.SCV):
                    if (obs.observation.player.idle_worker_count > 0):
                        new_action = [actions.FUNCTIONS.select_idle_worker(
                            "select", obs, units.Terran.SCV)]
                    else:
                        command = random.choice(command_scv)
                        new_action = [actions.FUNCTIONS.select_point(
                            "select", (BuildOrders.sigma(self, command.x),
                                       BuildOrders.sigma(self, command.y)))]

            if self.reqSteps == 2:  # move to expansion location
                target = BuildOrders.choose_location(self, top_start)
                new_action = [
                    actions.FUNCTIONS.move_camera(target)]

            if self.reqSteps == 1:  # check if there is a commandcenter there if there is move to the next location or build one
                command_center = BuildOrders.get_units(self, obs, units.Terran.CommandCenter)
                if len(command_center) > 0:
                    if len(Coordinates.EXPO_LOCATIONS) >= self.expo_loc+1:
                        self.reqSteps = 2
                        self.expo_loc += 1
                        target = BuildOrders.choose_location(self, top_start)
                        new_action = [
                            actions.FUNCTIONS.move_camera(target)]
                else:
                    if BuildOrders.select_unit(self, obs, units.Terran.SCV):
                        if BuildOrders.do_action(self, obs, actions.FUNCTIONS.Build_CommandCenter_screen.id):
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
        barracks = BuildOrders.get_units(self, obs, units.Terran.Barracks)
        if self.reqSteps == 0:
            self.reqSteps = 3

        elif self.reqSteps == 3:
            self.reqSteps = 2
            new_action = [
                actions.FUNCTIONS.move_camera(self.base_location)
            ]

        elif self.reqSteps == 2:
            self.reqSteps = 1
            if len(barracks) > 0:
                new_action = [actions.FUNCTIONS.select_point("select",
                                                             (BuildOrders.sigma(self, barracks[0].x),
                                                              BuildOrders.sigma(self, barracks[0].y)))]

        elif self.reqSteps == 1:
            self.reqSteps = 0
            if BuildOrders.select_unit(self, obs, units.Terran.Barracks):
                if BuildOrders.do_action(self, obs, actions.FUNCTIONS.Train_Marine_quick.id
                                         ) and BuildOrders.not_in_queue(self, obs, units.Terran.Barracks
                                                                        ) and free_supply > 0:
                    new_action = [actions.FUNCTIONS.Train_Marine_quick("now")]

        return new_action




    def sigma(self, num):
        if num <= 0:
            return 0
        elif num >= 83:
            return 83
        else:
            return num

    def not_in_queue(self, obs, unit_type):
        queues = obs.observation.build_queue
        if len(queues) > 0:
            for queue in queues:
                if queue[0] == unit_type:
                    return False
        return True

    def do_action(self, obs, action):
        return action in obs.observation.available_actions

    def not_in_progress(self, obs, unit_type):
        units = BuildOrders.get_units(self, obs, unit_type)
        for unit in units:
            if (unit.build_progress != 100):
                return False
        return True

    def get_units(self, obs, unit_type):
        return [unit for unit in obs.observation.feature_units
                if unit.unit_type == unit_type]

    def select_unit(self, obs, unit_type):
        if (len(obs.observation.single_select) > 0 and
                obs.observation.single_select[0].unit_type == unit_type):
            return True

        if (len(obs.observation.multi_select) > 0 and
                obs.observation.multi_select[0].unit_type == unit_type):
            return True

        return False


    def select_scv(self, obs):
        new_action = [actions.FUNCTIONS.no_op()]
        command_scv = BuildOrders.get_units(self, obs, units.Terran.SCV)
        if len(command_scv) > 0 and not BuildOrders.select_unit(self, obs, units.Terran.SCV):
            if (obs.observation.player.idle_worker_count > 0):
                new_action = [actions.FUNCTIONS.select_idle_worker(
                    "select", obs, units.Terran.SCV)]
            else:
                command = random.choice(command_scv)
                new_action = [actions.FUNCTIONS.select_point(
                    "select", (BuildOrders.sigma(self, command.x),
                               BuildOrders.sigma(self, command.y)))]
        return new_action
