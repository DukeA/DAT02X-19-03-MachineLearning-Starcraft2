import random
from Models.HelperClass.IsPossible import IsPossible
from Models.Selector.attackSelector import AttackSelector
from Models.Selector.buildSelector import BuildSelector
from Models.Selector.selector import Selector

class HardCodedSelector():

    def hardCodedSelector(self, obs):
        
        allActions = [
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

        if self.reqSteps == 0 and not self.game_state_updated:
            return "updateState"
        else:
            self.game_state_updated = False

#################################################################################       
            if self.steps < 16 * 60 * 1 / 5 * 1.4:   #First min
                selection = random.random()
                if self.earlier_action == "build_supply_depot" or self.earlier_action == "build_barracks":
                    return "return_scv"
                
                if selection <= 0.1:
                    if IsPossible.build_scv_possible(self, obs):
                        return "build_scv"

                elif selection <= 0.3:
                    if IsPossible.build_supply_depot_possible(self, obs):
                        return "build_supply_depot"
                
                elif selection <= 0.5:
                    if IsPossible.build_barracks_possible(self, obs):
                        return "build_barracks"

                elif selection <= 0.6:
                    if IsPossible.build_refinery_possible(self, obs):
                        return "build_refinery"
                
                elif selection <= 0.75:
                    return "build_factory"
                
                elif selection <= 0.95:
                    return "no_op"

                elif selection <= 1.0:
                    return BuildSelector.buildSelector(self, obs)
            
                else:
                    return "no_op"
    

#########################################################################################
        
            if self.steps < 16 * 60 * 2 / 5 * 1.4:   #min 2
                selection = random.random()
                if self.earlier_action == "build_supply_depot" or self.earlier_action == "build_barracks":
                    return "return_scv"

                if selection <= 0.1:
                    if IsPossible.build_scv_possible(self, obs):
                        return "build_scv"

                elif selection <= 0.15:
                    if IsPossible.build_supply_depot_possible(self, obs):
                        return "build_supply_depot"
                elif selection <= 0.3:
                    if IsPossible.build_starport_possible(self, obs):
                        return "build_starport"
                
                elif selection <= 0.4:
                    if IsPossible.build_barracks_possible(self, obs):
                        return "build_barracks"

                elif selection <= 0.5:
                    if IsPossible.build_refinery_possible(self, obs):
                        return "build_refinery"
                
                elif selection <= 0.6:
                    if IsPossible.build_factory_possible(self, obs):
                        return "build_factory"
                
                elif selection <= 0.8:
                    if IsPossible.build_marines_possible(self, obs):
                        return "build_marines"
                
                elif selection <= 0.95:
                    return "no_op"

                elif selection <= 1.0:
                    return BuildSelector.buildSelector(self, obs)
            
                else:
                    return "no_op"


############################################################################################3
            if self.steps < 16 * 60 * 3 / 5 * 1.4:   #min 3
                selection = random.random()
                if self.earlier_action == "build_supply_depot" or self.earlier_action == "build_barracks":
                    return "return_scv"

                if selection <= 0.05:
                    if IsPossible.build_supply_depot_possible(self, obs):
                        return "build_supply_depot"

                elif selection <= 0.3:
                    if IsPossible.build_marines_possible(self, obs):
                        return "build_marines"

                elif selection <= 0.4:
                    if IsPossible.build_refinery_possible(self, obs):
                        return "build_refinery"

                elif selection <= 0.5:
                    if IsPossible.build_factory_possible(self, obs):
                        return "build_factory"
                
                elif selection <= 0.6:
                    if IsPossible.build_starport_possible(self, obs):
                        return "build_starport"
                
                elif selection <= 0.7:
                    if IsPossible.build_techlab_possible(self, obs):
                        return "build_tech_lab_barracks"
                
                elif selection <= 0.8:
                    if IsPossible.build_reaper_possible(self, obs):
                        return "build_reaper"
                
                elif selection <= 0.85:
                    if IsPossible.build_barracks_possible(self, obs):
                        return "build_barracks"

                elif selection <= 0.95:
                    return "no_op"            

                elif selection <= 1.0:
                    return BuildSelector.buildSelector(self, obs)
            
                else:
                    return "no_op"


###############################################################################################
            if self.steps < 16 * 60 * 4 / 5 * 1.4:   #min 4
                selection = random.random()
                if self.earlier_action == "build_supply_depot" or self.earlier_action == "build_barracks":
                    return "return_scv"

                elif selection <= 0.1:
                    if IsPossible.build_barracks_possible(self, obs):
                        return "build_barracks"
                
                elif selection <= 0.2:
                    if IsPossible.build_factory_possible(self, obs):
                        return "build_factory"
                
                elif selection <= 0.3:
                    if IsPossible.build_starport_possible(self, obs):
                        return "build_starport"
                
                elif selection <= 0.4:
                    if IsPossible.build_techlab_possible(self, obs):
                        return "build_tech_lab_barracks"

                elif selection <= 0.5:
                    if IsPossible.build_marines_possible(self, obs):
                        return "build_marines"

                elif selection <= 0.7:
                    return "no_op"

                elif selection <= 0.8:
                    return "retreat"

                elif selection <= 0.9:
                    return "expand"
                

                elif selection <= 1.0:
                    return BuildSelector.buildSelector(self, obs)
            
                else:
                    return "no_op"


############################################################################################
            if self.steps < 16 * 60 * 5 / 5 * 1.4:   #min 5
                selection = random.random()
                if self.earlier_action == "build_supply_depot" or self.earlier_action == "build_barracks":
                    return "return_scv"

                if selection <= 0.2:
                    if IsPossible.build_marauder_possible(self, obs):
                        return "build_marauder"

                elif selection <= 0.4:
                    if IsPossible.build_viking_possible(self, obs):
                        return "build_viking"
                
                elif selection <= 0.6:
                    if IsPossible.build_marines_possible(self, obs):
                        return "build_marines"

                elif selection <= 0.8:
                    return "no_op"
                
                elif selection <= 0.8:
                    return "retreat"

                elif selection <= 1.0:
                    return BuildSelector.buildSelector(self, obs)
            
                else:
                    return "no_op"            

############################################################################################
            if self.steps < 16 * 60 * 10 / 5 * 1.4:   #min 10
                
                selection = random.random()
                if self.earlier_action == "build_supply_depot" or self.earlier_action == "build_barracks":
                    return "return_scv"

                if selection <= 0.1:
                    if IsPossible.build_marines_possible(self, obs):
                        return "build_marines"  

                elif selection <= 0.2:
                    if IsPossible.build_marauder_possible(self, obs):
                        return "build_marauder"
                
                elif selection <= 0.3:
                    if IsPossible.build_reaper_possible(self, obs):
                        return "build_reaper"

                elif selection <= 0.4:
                    if IsPossible.build_medivac_possible(self, obs):
                        return "build_medivac"

                elif selection <= 0.5:
                    if IsPossible.build_viking_possible(self, obs):
                        return "build_viking"
                
                elif selection <= 0.5:
                    if IsPossible.build_hellion_possible(self, obs):
                        return "build_hellion"
                
                elif selection <= 0.6:
                    if IsPossible.build_techlab_possible(self, obs):
                        return "build_tech_lab_barracks"

                elif selection <= 0.7:
                    if IsPossible.build_starport_possible(self, obs):
                        return "build_starport"
                
                elif selection <= 0.8:
                    if IsPossible.build_factory_possible(self, obs):
                        return "build_factory"

                elif selection <= 0.9:
                        return "retreat"
                
                if selection <= 0.95 and not self.attacking:
                    return "build_supply_depot"

                else:
                    return BuildSelector.buildSelector(self, obs)
##################################################################################################

            if self.steps < 16 * 60 * 30 / 5 * 1.4:   #min 30
                
                selection = random.random()
                if self.earlier_action == "build_supply_depot" or self.earlier_action == "build_barracks":
                    return "return_scv"

                if selection <= 0.1:
                    if IsPossible.build_marines_possible(self, obs):
                        return "build_marines"  

                elif selection <= 0.2:
                    if IsPossible.build_marauder_possible(self, obs):
                        return "build_marauder"
                
                elif selection <= 0.3:
                    if IsPossible.build_reaper_possible(self, obs):
                        return "build_reaper"

                elif selection <= 0.4:
                    if IsPossible.build_medivac_possible(self, obs):
                        return "build_medivac"

                elif selection <= 0.5:
                    if IsPossible.build_viking_possible(self, obs):
                        return "build_viking"
                
                elif selection <= 0.5:
                    if IsPossible.build_hellion_possible(self, obs):
                        return "build_hellion"
                
                elif selection <= 0.6:
                    if IsPossible.build_techlab_possible(self, obs):
                        return "build_tech_lab_barracks"

                elif selection <= 0.7:
                    if IsPossible.build_starport_possible(self, obs):
                        return "build_starport"
                
                elif selection <= 0.8:
                    if IsPossible.build_factory_possible(self, obs):
                        return "build_factory"

                elif selection <= 0.9 and not self.attacking:
                    return "retreat"

                if selection <= 0.91:
                    self.attacking = True
                    return "attack"

                else:
                    return BuildSelector.buildSelector(self, obs)



##############################################################################################

            else:
                return BuildSelector.buildSelector(self, obs)
            
         