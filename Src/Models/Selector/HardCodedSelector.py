import random
from Models.HelperClass.IsPossible import IsPossible
from Models.Selector.selector import Selector

class HardCodedSelector():

    def hardCodedSelector(self, obs):

        all_actions = [
                "no_op",
                "build_scv",
                "build_supply_depot",
                "build_marine",
                "build_marauder",
                "build_reaper",
                "build_hellion",
                "build_medivac",
                "build_viking",
                "build_barracks",
                "build_refinery",
                "distribute_scv",
                "return_scv",
                "expand",
                "build_factory",
                "build_starport",
                "build_tech_lab_barracks",
                "army_count",
                "attack",
                "retreat",
                "scout",
                "transform_vikings_to_ground",
                "transform_vikings_to_air",
            ]

        build_actions = [
                "no_op",
                "build_scv",
                "build_supply_depot",
                "build_marine",
                "build_marauder",
                "build_reaper",
                "build_hellion",
                "build_medivac",
                "build_viking",
                "build_barracks",
                "build_refinery",
                "distribute_scv",
                "return_scv",
                "expand",
                "build_factory",
                "build_starport",
                "build_tech_lab_barracks",
            ]



        if self.reqSteps == 0 and not self.game_state_updated:
            return "updateState"
        else:
            self.game_state_updated = False

#################################################################################
            if self.steps < 1346/5:   #First min
                selection = random.random()
                if obs.observation.player.idle_worker_count > 1:
                    return "return_scv"

                if selection <= 0.2:
                    if IsPossible.build_scv_possible(self, obs):
                        return "build_scv"

                if selection <= 0.3:
                    if IsPossible.build_supply_depot_possible(self, obs):
                        return "build_supply_depot"

                if selection <= 0.7:
                    if IsPossible.build_barracks_possible(self, obs):
                        self.hasBarrack = True
                        return "build_barracks"

                if selection <= 0.9:
                    if IsPossible.build_refinery_possible(self, obs):
                        return "build_refinery"

                if selection <= 0.95:
                    return "no_op"

                if selection <= 1.0:
                    return (random.choice(Selector.possible_build_actions(self, obs)))

                else:
                    return "no_op"


#########################################################################################

            if self.steps < 1346/5*2:   #min 2
                selection = random.random()
                if obs.observation.player.idle_worker_count > 1:
                    return "return_scv"

                if selection <= 0.2:
                    if IsPossible.build_scv_possible(self, obs):
                        return "build_scv"

                if selection <= 0.25:
                    if IsPossible.build_supply_depot_possible(self, obs):
                        return "build_supply_depot"
                
                if selection <= 0.5:
                    if IsPossible.build_starport_possible(self, obs):
                        self.hasStarport = True
                        return "build_starport"

                if selection <= 0.55:
                    if IsPossible.build_barracks_possible(self, obs):
                        self.hasBarrack = True
                        return "build_barracks"

                if selection <= 0.6:
                    if IsPossible.build_refinery_possible(self, obs):
                        return "build_refinery"

                if selection <= 0.8:
                    if IsPossible.build_factory_possible(self, obs):
                        return "build_factory"

                if selection <= 0.9:
                    if IsPossible.build_marines_possible(self, obs):
                        return "build_marine"

                if selection <= 0.91:
                    return "no_op"
                
                if selection <= 0.95:
                    return "expand"
                    

                if selection <= 1.0:
                    return (random.choice(Selector.possible_build_actions(self, obs)))

                else:
                    return "no_op"


############################################################################################3
            if self.steps < 1346/5*3:   #min 3
                selection = random.random()
                if obs.observation.player.idle_worker_count > 1:
                    return "return_scv"

                if not self.hasStarport:
                    if IsPossible.build_starport_possible(self, obs):
                        self.hasStarport = True
                        return "build_startport"
                    else:
                        return "no_op"
                
                if not self.hasFactory:
                    if IsPossible.build_factory_possible(self, obs):
                        self.hasFactory = True
                        return "build_factory"
                    else:
                        return "no_op"

                if not self.hasBarrack:
                    if IsPossible.build_barracks_possible(self, obs):
                        self.hasBarrack = True
                        return "build_barracks"
                    else:
                        return "no_op"

                if selection <= 0.1:
                    if IsPossible.build_scv_possible(self, obs):
                        return "build_scv"

                if selection <= 0.2:
                    if IsPossible.build_marines_possible(self, obs):
                        return "build_marine"

                if selection <= 0.3:
                    if IsPossible.build_refinery_possible(self, obs):
                        return "build_refinery"

                if selection <= 0.45:
                    if IsPossible.build_factory_possible(self, obs):
                        return "build_factory"

                if selection <= 0.75:
                    if IsPossible.build_starport_possible(self, obs):
                        return "build_starport"

                if selection <= 0.8:
                    if IsPossible.build_barracks_possible(self, obs):
                        return "build_barracks"

                if selection <= 0.85:
                    return "no_op"
                
                if selection <= 0.9:
                    if IsPossible.build_supply_depot_possible(self, obs):
                        return "build_supply_depot"

                if selection <= 0.95:
                    return "expand"

                if selection <= 1.0:
                    return (random.choice(Selector.possible_build_actions(self, obs)))

                else:
                    return "no_op"


###############################################################################################
            if self.steps < 1346/5*4:   #min 4
                selection = random.random()
                if obs.observation.player.idle_worker_count > 1:
                    return "return_scv"
                
                if not self.hasStarport:
                    if IsPossible.build_starport_possible(self, obs):
                        self.hasStarport = True
                        return "build_startport"
                        
                    else:
                        return "no_op"
                
                if not self.hasFactory:
                    if IsPossible.build_factory_possible(self, obs):
                        self.hasFactory = True
                        return "build_factory"
                    else:
                        return "no_op"

                if not self.hasBarrack:
                    if IsPossible.build_barracks_possible(self, obs):
                        self.hasBarrack = True
                        return "build_barracks"
                    else:
                        return "no_op"

                if selection <= 0.05:
                    if IsPossible.build_barracks_possible(self, obs):
                        return "build_barracks"

                if selection <= 0.1:
                    if IsPossible.build_supply_depot_possible(self, obs):
                        return "build_supply_depot"

                if selection <= 0.2:
                    if IsPossible.build_factory_possible(self, obs):
                        return "build_factory"

                if selection <= 0.45:
                    if IsPossible.build_starport_possible(self, obs):
                        return "build_starport"

                if selection <= 0.55:
                    if IsPossible.build_marines_possible(self, obs):
                        return "build_marine"
                
                if selection <= 0.65:
                    if IsPossible.build_viking_possible(self, obs):
                        return "build_viking"

                if selection <= 0.75:
                    if IsPossible.build_medivac_possible(self, obs):
                        return "build_medivac"

    
                if selection <= 0.85:
                    if IsPossible.build_hellion_possible(self, obs):
                        return "build_hellion"


                if selection <= 0.86:
                    return "no_op"


                if selection <= 0.87:
                    if IsPossible.build_scv_possible(self, obs):
                        return "build_scv"

                if selection <= 0.9 and not self.attacking:
                    return "retreat"

                if selection <= 0.95:
                    return "expand"


                if selection <= 1.0:
                    return (random.choice(Selector.possible_build_actions(self, obs)))

                else:
                    return "no_op"


############################################################################################
            if self.steps < 1346/5*5:   #min 5
                selection = random.random()
                if obs.observation.player.idle_worker_count > 1:
                    return "return_scv"
                
                if not self.hasStarport:
                    if IsPossible.build_starport_possible(self, obs):
                        self.hasStarport = True
                        return "build_startport"
                    else:
                        return "no_op"
                
                if not self.hasFactory:
                    if IsPossible.build_factory_possible(self, obs):
                        self.hasFactory = True
                        return "build_factory"
                    else:
                        return "no_op"

                if not self.hasBarrack:
                    if IsPossible.build_barracks_possible(self, obs):
                        self.hasBarrack = True
                        return "build_barracks"
                    else:
                        return "no_op"

                if selection <= 0.0:
                    self.attacking = True
                    return "attack"

                if selection <= 0.05:
                    if IsPossible.build_supply_depot_possible(self, obs):
                        return "build_supply_depot"

                if selection <= 0.2:
                    if IsPossible.build_viking_possible(self, obs):
                        return "build_viking"

                if selection <= 0.4:
                    if IsPossible.build_medivac_possible(self, obs):
                        return "build_medivac"

                if selection <= 0.6:
                    if IsPossible.build_marines_possible(self, obs):
                        return "build_marine"

                if selection <= 0.7:
                    if IsPossible.build_hellion_possible(self, obs):
                        return "build_hellion"

                if selection <= 0.8:
                    return "no_op"


                if selection <= 0.85:
                    if IsPossible.build_scv_possible(self, obs):
                        return "build_scv"


                if selection <= 0.9 and not self.attacking:
                    return "retreat"

                if selection <= 1.0:
                    return (random.choice(Selector.possible_build_actions(self, obs)))

                else:
                    return "no_op"

############################################################################################
            if self.steps < 1346/5*10:   #min 10

                selection = random.random()
                if obs.observation.player.idle_worker_count > 1:
                    if selection <= 0.2:
                        return "return_scv"

                if not self.hasStarport:
                    if IsPossible.build_starport_possible(self, obs):
                        self.hasStarport = True
                        return "build_startport"
                    else:
                        return "no_op"
                
                if not self.hasFactory:
                    if IsPossible.build_factory_possible(self, obs):
                        self.hasFactory = True
                        return "build_factory"
                    else:
                        return "no_op"

                if not self.hasBarrack:
                    if IsPossible.build_barracks_possible(self, obs):
                        self.hasBarrack = True
                        return "build_barracks"
                    else:
                        return "no_op"

                if self.attacking:
                    attack = random.random()
                    if attack <= 0.3:
                        return "attack"

                if selection <= 0.01:
                    self.attacking = True
                    return "attack"

                if selection <= 0.1:
                    if IsPossible.build_marines_possible(self, obs):
                        return "build_marine"

                if selection <= 0.3:
                    if IsPossible.build_viking_possible(self, obs):
                        return "build_viking"

                if selection <= 0.35:
                    if IsPossible.build_medivac_possible(self, obs):
                        return "build_medivac"

                if selection <= 0.45:
                    if IsPossible.build_starport_possible(self, obs):
                        return "build_starport"

                if selection <= 0.55:
                    if IsPossible.build_factory_possible(self, obs):
                        return "build_factory"


                if selection <= 0.60:
                    if IsPossible.build_scv_possible(self, obs):
                        return "build_scv"

                if selection <= 0.65:
                        return "expand"

                if selection <= 0.75:
                    if IsPossible.build_supply_depot_possible(self, obs):
                        return "build_starport"

                if selection <= 0.9 and not self.attacking:
                        return "retreat"

                if selection <= 0.95:
                    return "no_op"

                

                else:
                    return (random.choice(Selector.possible_build_actions(self, obs)))
##################################################################################################

            if self.steps < 1346/5*30:   #min 30

                selection = random.random()
                if obs.observation.player.idle_worker_count > 1:
                    if selection <= 0.1:
                        return "return_scv"
                
                if self.attacking:
                    attack = random.random()
                    if attack <= 0.3:
                        return "attack"

                if selection <= 0.15:
                    if IsPossible.build_marines_possible(self, obs):
                        return "build_marine"

                if selection <= 0.3:
                    if IsPossible.build_reaper_possible(self, obs):
                        return "build_reaper"

                if selection <= 0.4:
                    if IsPossible.build_medivac_possible(self, obs):
                        return "build_medivac"

                if selection <= 0.5:
                    if IsPossible.build_viking_possible(self, obs):
                        return "build_viking"

                if selection <= 0.5:
                    if IsPossible.build_hellion_possible(self, obs):
                        return "build_hellion"

                if selection <= 0.7:
                    if IsPossible.build_starport_possible(self, obs):
                        return "build_starport"

                if selection <= 0.8:
                    if IsPossible.build_factory_possible(self, obs):
                        return "build_factory"

                if selection <= 0.81:
                        return "no_op"

                if selection <= 0.85:
                    if IsPossible.build_supply_depot_possible(self, obs):
                        return "build_supply_depot"

                if selection <= 0.9 and not self.attacking:
                    return "retreat"

                if selection <= 0.95:
                    self.attacking = True
                    return "attack"

                else:
                    return (random.choice(Selector.possible_build_actions(self, obs)))



##############################################################################################

            else:
                return (random.choice(Selector.possible_build_actions(self, obs)))
