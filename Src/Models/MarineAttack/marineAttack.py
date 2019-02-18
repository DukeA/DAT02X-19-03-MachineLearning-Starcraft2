from pysc2.agents import base_agent
from pysc2.lib import actions, units
import random

# The following class should use a neural network to predict outcome. Not implemented yet.
class marineAttack(base_agent.BaseAgent):
    screen_has_moved = False
    has_issued_attack = False
    own_marines = []
    enemy_marines = []
    enemy_x = []
    enemy_y = []
    minimap_size = 64  # HARDCODED, DEPENDS ON INITIALIZATION IN runMarineAttack.py
    predicted_outcome = []

    def attack(self, obs):
        self.predicted_outcome = 1
        # Hardocoded to always think it's going to win. Switch this out for a neural network sometime.
        if self.predicted_outcome == 0:
            # Will lose (but attack anyway)
            self.has_issued_attack = True
            return self.attack_location_minimap(obs, self.enemy_x, self.enemy_y)
        elif self.predicted_outcome == 1:
            # Will win
            self.has_issued_attack = True
            return self.attack_location_minimap(obs, self.enemy_x, self.enemy_y)

    def step(self, obs):
        super(marineAttack, self).step(obs)

        if obs.first():
            self.own_marines = get_own_units(obs, units.Terran.Marine)
            print('Own marines: ' + str(len(self.own_marines)))
            self.enemy_x = []
            self.enemy_y = []
            self.enemy_marines = []
            self.screen_has_moved = False
            self.has_issued_attack = False

            # Hardcoding resets. It doesn't loop properly in runMarineAttack.py

        if not self.enemy_x:
            for x in range(self.minimap_size):
                for y in range(self.minimap_size):
                    if obs.observation.feature_minimap[5][x][y] == 4:  # Finds enemy units on minimap
                        self.enemy_x.append(x)
                        self.enemy_y.append(y)
            random_location = random.randrange(0, len(self.enemy_x))
            self.enemy_x = self.enemy_x[random_location]
            self.enemy_y = self.enemy_y[random_location]
            print("Enemy found")

        if len(self.own_marines) > 0:
            if not select_unit(obs, units.Terran.Marine):
                select = random.choice(self.own_marines)
                print("Marines selected")
                return actions.FUNCTIONS.select_point("select_all_type", (select.x, select.y))

        if not self.screen_has_moved:
            return self.move_camera_to_location(obs, self.enemy_x, self.enemy_y)

        if not self.enemy_marines:
            self.enemy_marines = get_enemy_units(obs, units.Terran.Marine)
            print('Enemy marines: ' + str(len(self.enemy_marines)))

        if not self.has_issued_attack:
            if self.screen_has_moved:
                return self.attack(obs)

        return actions.FUNCTIONS.no_op()

    def attack_location_minimap(self, obs, x, y):
        if do_action(obs, actions.FUNCTIONS.Attack_minimap.id):
            self.has_issued_attack = True
            return actions.FUNCTIONS.Attack_minimap("now", [y, x])

    def move_camera_to_location(self, obs, x, y):
        if do_action(obs, actions.FUNCTIONS.move_camera.id):
            self.screen_has_moved = True
            return actions.FUNCTIONS.move_camera([y, x])

# The following class randomly predicts outcome.
class marineAttackGenerator(marineAttack):

    def attack(self, obs):
        print("This is a random prediction")
        self.predicted_outcome = random.randrange(0, 2)
        if self.predicted_outcome == 0:
            # Will lose (but attack anyway)
            self.has_issued_attack = True
            return self.attack_location_minimap(obs, self.enemy_x, self.enemy_y)
        elif self.predicted_outcome == 1:
            # Will win
            self.has_issued_attack = True
            return self.attack_location_minimap(obs, self.enemy_x, self.enemy_y)


def get_own_units(obs, unit_type):
        return [unit for unit in obs.observation.feature_units
                if (unit.unit_type == unit_type) & (unit[1] == 1)]


def get_enemy_units(obs, unit_type):
        return [unit for unit in obs.observation.feature_units
                if (unit.unit_type == unit_type) & (unit[1] == 4)]


def select_unit(obs, unit_type):
        if (len(obs.observation.single_select) > 0 and
                obs.observation.single_select[0].unit_type == unit_type):
            return True

        if (len(obs.observation.multi_select) > 0 and
                obs.observation.multi_select[0].unit_type == unit_type):
            return True

        return False


def do_action(obs, action):
        return action in obs.observation.available_actions
