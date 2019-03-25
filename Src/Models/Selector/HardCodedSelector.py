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
                if self.earlier_action == "build_supply_depot":
                    return "distribute_scv"


                if selection <= 0.1:
                    if IsPossible.build_scv_possible(self, obs):
                        return "build_scv"

                elif selection <= 0.2:
                    if IsPossible.build_supply_depot_possible(self, obs):
                        return "build_supply_depot"
                
                elif selection <= 0.25:
                    return "expand"
                
                elif selection <= 0.3:
                    return "no_op"

                elif selection <= 0.4:
                    if IsPossible.build_barracks_possible(self, obs):
                        return "build_barracks"

                elif selection <= 0.5:
                    if IsPossible.build_marines_possible(self, obs):
                        return "build_refinery"
                
                elif selection <= 1.0:
                    return Selector.selector(self, obs)
            
                else:
                    return "no_op"
    

#########################################################################################
        
            if self.steps < 16 * 60 * 2 / 5 * 1.4:   #min 2
                selection = random.random()
                if self.earlier_action == "build_supply_depot":
                    return "distribute_scv"


                if selection <= 0.1:
                    if IsPossible.build_scv_possible(self, obs):
                        return "build_scv"

                elif selection <= 0.2:
                    if IsPossible.build_supply_depot_possible(self, obs):
                        return "build_supply_depot"
                
                elif selection <= 0.25:
                    return "expand"
                
                elif selection <= 0.3:
                    return "no_op"

                elif selection <= 0.4:
                    if IsPossible.build_barracks_possible(self, obs):
                        return "build_barracks"

                elif selection <= 0.5:
                    if IsPossible.build_marines_possible(self, obs):
                        return "build_refinery"
                
                elif selection <= 0.7:
                    if IsPossible.build_marines_possible(self, obs):
                        return "build_marines"

                elif selection <= 1.0:
                    return Selector.selector(self, obs)
            
                else:
                    return "no_op"


############################################################################################3
            if self.steps < 16 * 60 * 3 / 5 * 1.4:   #min 3
                selection = random.random()
                if self.earlier_action == "build_supply_depot":
                    return "distribute_scv"


                if selection <= 0.1:
                    if IsPossible.build_scv_possible(self, obs):
                        return "build_scv"

                elif selection <= 0.2:
                    if IsPossible.build_supply_depot_possible(self, obs):
                        return "build_supply_depot"
                
                elif selection <= 0.25:
                    return "expand"
                
                elif selection <= 0.3:
                    return "no_op"

                elif selection <= 0.4:
                    if IsPossible.build_barracks_possible(self, obs):
                        return "build_barracks"

                elif selection <= 0.5:
                    if IsPossible.build_marines_possible(self, obs):
                        return "build_refinery"
                
                elif selection <= 0.7:
                    if IsPossible.build_marines_possible(self, obs):
                        return "build_marines"
                
                elif selection <= 1.0:
                    return Selector.selector(self, obs)
            
                else:
                    return "no_op"


###############################################################################################
            if self.steps < 16 * 60 * 4 / 5 * 1.4:   #min 4
                selection = random.random()
                if self.earlier_action == "build_supply_depot":
                    return "distribute_scv"


                if selection <= 0.1:
                    if IsPossible.build_scv_possible(self, obs):
                        return "build_scv"

                elif selection <= 0.2:
                    if IsPossible.build_supply_depot_possible(self, obs):
                        return "build_supply_depot"
                
                elif selection <= 0.25:
                    return "expand"
                
                elif selection <= 0.3:
                    return "no_op"

                elif selection <= 0.4:
                    if IsPossible.build_barracks_possible(self, obs):
                        return "build_barracks"

                elif selection <= 0.5:
                    if IsPossible.build_marines_possible(self, obs):
                        return "build_refinery"
                
                elif selection <= 0.7:
                    if IsPossible.build_marines_possible(self, obs):
                        return "build_marines"

                elif selection <= 1.0:
                    return Selector.selector(self, obs)
            
                else:
                    return "no_op"


############################################################################################
            if self.steps < 16 * 60 * 5 / 5 * 1.4:   #min 5
                selection = random.random()
                if self.earlier_action == "build_supply_depot":
                    return "distribute_scv"


                if selection <= 0.1:
                    if IsPossible.build_scv_possible(self, obs):
                        return "build_scv"

                elif selection <= 0.2:
                    if IsPossible.build_supply_depot_possible(self, obs):
                        return "build_supply_depot"
                
                elif selection <= 0.25:
                    return "expand"
                
                elif selection <= 0.3:
                    return "no_op"

                elif selection <= 0.4:
                    if IsPossible.build_barracks_possible(self, obs):
                        return "build_barracks"

                elif selection <= 0.5:
                    if IsPossible.build_marines_possible(self, obs):
                        return "build_refinery"
                
                elif selection <= 0.7:
                    if IsPossible.build_marines_possible(self, obs):
                        return "build_marines"
                        
                elif selection <= 1.0:
                    return Selector.selector(self, obs)
            
                else:
                    return "no_op"            

############################################################################################

            else:
                return Selector.selector(self,obs)
            
         