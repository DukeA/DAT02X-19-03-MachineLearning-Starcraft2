import random
import numpy as np
from pysc2.lib import actions, units
from collections import defaultdict
from Models.BuildOrders.ActionSingleton import ActionSingleton
from Models.HelperClass.HelperClass import HelperClass


class State:
    def __init__(self, bot_obj):

        # Game state

        self.units_amount = defaultdict(lambda: 0)  # Amount of each unit. Set to 0 by default
        self.units_amount[units.Terran.SCV] = 12
        self.units_amount[units.Terran.CommandCenter] = 1
        self.enemy_units_amount = defaultdict(lambda: 0)
        self.enemy_units_amount[units.Terran.SCV] = 12
        self.enemy_units_amount[units.Terran.CommandCenter] = 1
        self.minerals = 50
        self.vespene = 0
        self.food_used = 12
        self.food_cap = 15
        self.idle_workers = 0
        self.oldscore = 1000
        self.reward = 0

        self.last_attacked = 0
        self.units_attacked = 0
        self.bot_obj = bot_obj

    def get_state(self):
        """
        :return: A list containing all the tuples (minerals, vespene, unit_amount, action_issued, bot_obj.steps)
         since the start of the game
        """
        return self.state_tuple

    def update_state(self, bot_obj, obs):
        """
        Updates the state and adds up to 1 production facility to control group. Always takes 4 steps to execute.
        :param bot_obj: The agent
        :param obs: The observation
        :return: Actions
        """
        new_action = [actions.FUNCTIONS.no_op()]  # No action by default

        if bot_obj.reqSteps == 0:
            bot_obj.reqSteps = 3
            new_action = [actions.FUNCTIONS.select_control_group("recall", 9)]

        # Section for adding unselected production building to control group 9.
        # It only adds one building per state update to keep state update lengths consistent.
        # When at this stage, control group 9 should be selected.
        # This section should be ran even when the control group is correct.
        elif bot_obj.reqSteps == 3:
            unselected_production = self.get_unselected_production_buildings(obs, on_screen=False)
            if len(unselected_production) > 0:
                unit = random.choice(unselected_production)
                new_action = HelperClass.move_screen(obs, (unit.x, unit.y))
            bot_obj.reqSteps = 2

        elif bot_obj.reqSteps == 2:
            unselected_production = self.get_unselected_production_buildings(obs, on_screen=True)
            if len(unselected_production) > 0:
                unit = random.choice(unselected_production)
                new_action = [actions.FUNCTIONS.select_point(
                    "select",
                    (HelperClass.sigma(unit.x+random.randint(0, 3)),
                     HelperClass.sigma(unit.y+random.randint(0, 3))))]
            bot_obj.reqSteps = 1

        elif bot_obj.reqSteps == 1:
            # single_select is an array of zeros if nothing is selected.
            # The following line checks for when hp > 0 (i.e. a unit is actually selected)
            if obs.observation.single_select[0][2] > 0:
                if (obs.observation.single_select[0].unit_type == units.Terran.CommandCenter or
                        obs.observation.single_select[0].unit_type == units.Terran.Barracks or
                        obs.observation.single_select[0].unit_type == units.Terran.Factory or
                        obs.observation.single_select[0].unit_type == units.Terran.Starport):
                    new_action = [actions.FUNCTIONS.select_control_group("append", 9)]
            bot_obj.reqSteps = 0

            # Update the score and reward

            bot_obj.game_state_updated = True

        ActionSingleton().set_action(new_action)

    def get_state_now(self, obs):

        # Update any state that doesn't require actions
        oldscore = self.oldscore
        score = obs.observation.score_cumulative.score
        if score != oldscore:
            self.reward = score - self.oldscore
        else:
            self.reward = 0
        if obs.observation.player.minerals > 3000:
            minerals = 1
        else:
            minerals = obs.observation.player.minerals/3000

        if obs.observation.player.vespene > 3000:
            vespene = 1
        else:
            vespene = obs.observation.player.vespene/3000
        food_used = obs.observation.player.food_used/200
        food_cap = obs.observation.player.food_cap/200
        idle_workers = obs.observation.player.idle_worker_count/200
        self.oldscore = score

        # Filter out SCVs before updating units_amount because they disappear when they go into refineries
        own_units = [u for u in obs.observation.raw_units
                     if u.alliance == 1 and u.unit_type != units.Terran.SCV]
        # Quickly checks if the state has changed. Not sure if actually faster.
        units_amount = defaultdict(lambda: 0)
        own_unit_types = [u.unit_type for u in own_units]
        unit_types, unit_type_counts = np.unique(np.array(own_unit_types), return_counts=True)
        for (unit_type, unit_type_count) in zip(unit_types, unit_type_counts):
            units_amount[unit_type] = unit_type_count
        units_amount[units.Terran.SCV] = obs.observation.player.food_workers
        # Counts enemy units
        enemy_units_amount = defaultdict(lambda: 0)
        enemy_units = [u for u in obs.observation.raw_units
                       if u.alliance == 4]
        enemy_unit_types = [u.unit_type for u in enemy_units]
        unit_types, unit_type_counts = np.unique(np.array(enemy_unit_types), return_counts=True)
        for (unit_type, unit_type_count) in zip(unit_types, unit_type_counts):
            enemy_units_amount[unit_type] = unit_type_count

        enemy_army = len([u for u in enemy_units
                          if u.unit_type in [units.Terran.Marine,
                                             units.Terran.Marauder,
                                             units.Terran.Medivac,
                                             units.Terran.Reaper,
                                             units.Terran.Hellion,
                                             units.Terran.Hellbat,
                                             units.Terran.VikingFighter,
                                             units.Terran.VikingAssault,
                                             units.Terran.Thor,
                                             units.Terran.ThorHighImpactMode,
                                             units.Terran.SiegeTank,
                                             units.Terran.SiegeTankSieged,
                                             units.Terran.Cyclone,
                                             units.Terran.Raven,
                                             units.Terran.Ghost,
                                             units.Terran.Liberator,
                                             units.Terran.LiberatorAG,
                                             units.Terran.Battlecruiser,
                                             units.Terran.Banshee,
                                             units.Terran.WidowMine,
                                             units.Terran.WidowMineBurrowed,
                                             units.Terran.SCV
                                             ]])
        enemy_buildings = len([u for u in enemy_units
                              if u.unit_type in [units.Terran.CommandCenter,
                                                 units.Terran.CommandCenterFlying,
                                                 units.Terran.OrbitalCommand,
                                                 units.Terran.OrbitalCommandFlying,
                                                 units.Terran.PlanetaryFortress,
                                                 units.Terran.SupplyDepot,
                                                 units.Terran.SupplyDepotLowered,
                                                 units.Terran.Refinery,
                                                 units.Terran.Barracks,
                                                 units.Terran.BarracksFlying,
                                                 units.Terran.BarracksReactor,
                                                 units.Terran.BarracksTechLab,
                                                 units.Terran.EngineeringBay,
                                                 units.Terran.MissileTurret,
                                                 units.Terran.SensorTower,
                                                 units.Terran.Bunker,
                                                 units.Terran.Factory,
                                                 units.Terran.FactoryFlying,
                                                 units.Terran.FactoryReactor,
                                                 units.Terran.FactoryTechLab,
                                                 units.Terran.Armory,
                                                 units.Terran.GhostAcademy,
                                                 units.Terran.Starport,
                                                 units.Terran.StarportFlying,
                                                 units.Terran.StarportReactor,
                                                 units.Terran.StarportTechLab,
                                                 units.Terran.FusionCore
                                                 ]])

        return np.array([[minerals, vespene, food_used, food_cap, idle_workers,
                          units_amount[units.Terran.CommandCenter],
                          units_amount[units.Terran.SupplyDepot]/24,
                          units_amount[units.Terran.Barracks]/10,
                          units_amount[units.Terran.Marine]/200,
                          units_amount[units.Terran.SCV]/200,
                          enemy_army,
                          enemy_buildings,
                          self.last_attacked,
                          self.units_attacked / 200,
                          self.bot_obj.steps*8/30000]]), oldscore, obs.observation.feature_minimap.player_relative

    @staticmethod
    def get_unselected_production_buildings(obs, on_screen=False):
        """
        This methods returns a list of production buildings (buildings capable of producing units) that aren't
        in currently selected. Note that it doesn't count Barracks with tech labs.
        :param obs:
        :param on_screen: Whether or not the list should only contain units visible on the screen
        :return:
        """
        if on_screen:
            return [u for u in obs.observation.feature_units
                    if u.alliance == 1 and not u.is_selected
                    and (
                        u.unit_type == units.Terran.CommandCenter or
                        u.unit_type == units.Terran.Barracks or
                        u.unit_type == units.Terran.Factory or
                        u.unit_type == units.Terran.Starport
                    )]
        else:
            return [u for u in obs.observation.raw_units
                    if u.alliance == 1 and not u.is_selected
                    and (
                       u.unit_type == units.Terran.CommandCenter or
                       u.unit_type == units.Terran.Barracks or
                       u.unit_type == units.Terran.Factory or
                       u.unit_type == units.Terran.Starport
                    )]
