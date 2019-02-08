from pysc2.agents import base_agent
from pysc2.lib import actions, units
import random


class marineAttack(base_agent.BaseAgent):
    screen_has_moved = False

    own_marines = []
    enemy_marines = []

    def step(self, obs):
        super(marineAttack, self).step(obs)

        if obs.first():
            self.own_marines = len(self.get_own_units(obs, units.Terran.Marine))
            print('Own marines: ' + str(self.own_marines))
        if not self.screen_has_moved:
            return self.move_camera_to_enemy(obs)
        if not self.enemy_marines:
            self.enemy_marines = len(self.get_enemy_units(obs, units.Terran.Marine))
            print('Enemy marines: ' + str(self.enemy_marines))

        # TODO: Attacking...

        return actions.FUNCTIONS.no_op()


    def move_camera_to_enemy(self, obs):
        enemy_x = []
        enemy_y = []
        minimap_size = 64
        for x in range(minimap_size):
            for y in range(minimap_size):
                if obs.observation.feature_minimap[5][x][y] == 4:
                    enemy_x.append(x)
                    enemy_y.append(y)
        if self.do_action(obs, actions.FUNCTIONS.move_camera.id):
            random_loc = random.randrange(len(enemy_x))
            self.screen_has_moved = True
            return actions.FUNCTIONS.move_camera([enemy_y[random_loc], enemy_x[random_loc]])

    def get_own_units(self, obs, unit_type):
        return [unit for unit in obs.observation.feature_units
                if (unit.unit_type == unit_type) & (unit[1] == 1)]


    def get_enemy_units(self, obs, unit_type):
        return [unit for unit in obs.observation.feature_units
                if (unit.unit_type == unit_type) & (unit[1] == 4)]


    def do_action(self, obs, action):
        return action in obs.observation.available_actions
