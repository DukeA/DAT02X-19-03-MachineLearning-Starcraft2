from pysc2.agents import base_agent
from Models.ArmyControl.ArmyControl import ArmyControl
from Models.HelperClass.HelperClass import HelperClass
"""
 @Author Adam Grandén
 @Class Description:
 The code  is a controller for the method  Build Methods which sends a
 call to the  BuildOrder method and execute
 the following methods to make it run

 Adapted for ArmyControl
"""


class ArmyControlController(base_agent.BaseAgent):
    def __init__(self):
        super(ArmyControlController).__init__()
        self.ArmyControl()

    def attack(self, obs, location=None):
        ArmyControl.attack(self, obs, location)

    def retreat(self, obs, location=None):
        ArmyControl.retreat(self, obs, location)

    def scout(self, obs):
        ArmyControl.scout(self, obs)

    def transform_vikings_to_ground(self, obs):
        ArmyControl.transform_vikings_to_ground(self, obs)

    def transform_vikings_to_air(self, obs):
        ArmyControl.transform_vikings_to_air(self, obs)

    def count_army(self, obs):
        ArmyControl.count_army(self, obs)

    # Might need to be in its own controller class.

    def no_op(self, obs):
        HelperClass.no_op(self, obs)

    # Currently unused.

    def attack_aa(self, obs):
        ArmyControl.attack(self, obs, location=[11, 12])

    def attack_ab(self, obs):
        ArmyControl.attack(self, obs, location=[11, 19])

    def attack_ac(self, obs):
        ArmyControl.attack(self, obs, location=[11, 26])

    def attack_ad(self, obs):
        ArmyControl.attack(self, obs, location=[11, 33])

    def attack_ae(self, obs):
        ArmyControl.attack(self, obs, location=[11, 39])

    def attack_af(self, obs):
        ArmyControl.attack(self, obs, location=[11, 46])

    def attack_ag(self, obs):
        ArmyControl.attack(self, obs, location=[11, 53])

    def attack_ba(self, obs):
        ArmyControl.attack(self, obs, location=[18, 12])

    def attack_bb(self, obs):
        ArmyControl.attack(self, obs, location=[18, 19])

    def attack_bc(self, obs):
        ArmyControl.attack(self, obs, location=[18, 26])

    def attack_bd(self, obs):
        ArmyControl.attack(self, obs, location=[18, 33])

    def attack_be(self, obs):
        ArmyControl.attack(self, obs, location=[18, 39])

    def attack_bf(self, obs):
        ArmyControl.attack(self, obs, location=[18, 46])

    def attack_bg(self, obs):
        ArmyControl.attack(self, obs, location=[18, 53])

    def attack_ca(self, obs):
        ArmyControl.attack(self, obs, location=[25, 12])

    def attack_cb(self, obs):
        ArmyControl.attack(self, obs, location=[25, 19])

    def attack_cc(self, obs):
        ArmyControl.attack(self, obs, location=[25, 26])

    def attack_cd(self, obs):
        ArmyControl.attack(self, obs, location=[25, 33])

    def attack_ce(self, obs):
        ArmyControl.attack(self, obs, location=[25, 39])

    def attack_cf(self, obs):
        ArmyControl.attack(self, obs, location=[25, 46])

    def attack_cg(self, obs):
        ArmyControl.attack(self, obs, location=[25, 53])

    def attack_da(self, obs):
        ArmyControl.attack(self, obs, location=[32, 12])

    def attack_db(self, obs):
        ArmyControl.attack(self, obs, location=[32, 19])

    def attack_dc(self, obs):
        ArmyControl.attack(self, obs, location=[32, 26])

    def attack_dd(self, obs):
        ArmyControl.attack(self, obs, location=[32, 33])

    def attack_de(self, obs):
        ArmyControl.attack(self, obs, location=[32, 39])

    def attack_df(self, obs):
        ArmyControl.attack(self, obs, location=[32, 46])

    def attack_dg(self, obs):
        ArmyControl.attack(self, obs, location=[32, 53])

    def attack_ea(self, obs):
        ArmyControl.attack(self, obs, location=[38, 12])

    def attack_eb(self, obs):
        ArmyControl.attack(self, obs, location=[38, 19])

    def attack_ec(self, obs):
        ArmyControl.attack(self, obs, location=[38, 26])

    def attack_ed(self, obs):
        ArmyControl.attack(self, obs, location=[38, 33])

    def attack_ee(self, obs):
        ArmyControl.attack(self, obs, location=[38, 39])

    def attack_ef(self, obs):
        ArmyControl.attack(self, obs, location=[38, 46])

    def attack_eg(self, obs):
        ArmyControl.attack(self, obs, location=[38, 53])

    def attack_fa(self, obs):
        ArmyControl.attack(self, obs, location=[45, 12])

    def attack_fb(self, obs):
        ArmyControl.attack(self, obs, location=[45, 19])

    def attack_fc(self, obs):
        ArmyControl.attack(self, obs, location=[45, 26])

    def attack_fd(self, obs):
        ArmyControl.attack(self, obs, location=[45, 33])

    def attack_fe(self, obs):
        ArmyControl.attack(self, obs, location=[45, 39])

    def attack_ff(self, obs):
        ArmyControl.attack(self, obs, location=[45, 46])

    def attack_fg(self, obs):
        ArmyControl.attack(self, obs, location=[45, 53])

    def attack_ga(self, obs):
        ArmyControl.attack(self, obs, location=[52, 12])

    def attack_gb(self, obs):
        ArmyControl.attack(self, obs, location=[52, 19])

    def attack_gc(self, obs):
        ArmyControl.attack(self, obs, location=[52, 26])

    def attack_gd(self, obs):
        ArmyControl.attack(self, obs, location=[52, 33])

    def attack_ge(self, obs):
        ArmyControl.attack(self, obs, location=[52, 39])

    def attack_gf(self, obs):
        ArmyControl.attack(self, obs, location=[52, 46])

    def attack_gg(self, obs):
        ArmyControl.attack(self, obs, location=[52, 53])

    def retreat_aa(self, obs):
        ArmyControl.retreat(self, obs, location=[11, 12])

    def retreat_ab(self, obs):
        ArmyControl.retreat(self, obs, location=[11, 19])

    def retreat_ac(self, obs):
        ArmyControl.retreat(self, obs, location=[11, 26])

    def retreat_ad(self, obs):
        ArmyControl.retreat(self, obs, location=[11, 33])

    def retreat_ae(self, obs):
        ArmyControl.retreat(self, obs, location=[11, 39])

    def retreat_af(self, obs):
        ArmyControl.retreat(self, obs, location=[11, 46])

    def retreat_ag(self, obs):
        ArmyControl.retreat(self, obs, location=[11, 53])

    def retreat_ba(self, obs):
        ArmyControl.retreat(self, obs, location=[18, 12])

    def retreat_bb(self, obs):
        ArmyControl.retreat(self, obs, location=[18, 19])

    def retreat_bc(self, obs):
        ArmyControl.retreat(self, obs, location=[18, 26])

    def retreat_bd(self, obs):
        ArmyControl.retreat(self, obs, location=[18, 33])

    def retreat_be(self, obs):
        ArmyControl.retreat(self, obs, location=[18, 39])

    def retreat_bf(self, obs):
        ArmyControl.retreat(self, obs, location=[18, 46])

    def retreat_bg(self, obs):
        ArmyControl.retreat(self, obs, location=[18, 53])

    def retreat_ca(self, obs):
        ArmyControl.retreat(self, obs, location=[25, 12])

    def retreat_cb(self, obs):
        ArmyControl.retreat(self, obs, location=[25, 19])

    def retreat_cc(self, obs):
        ArmyControl.retreat(self, obs, location=[25, 26])

    def retreat_cd(self, obs):
        ArmyControl.retreat(self, obs, location=[25, 33])

    def retreat_ce(self, obs):
        ArmyControl.retreat(self, obs, location=[25, 39])

    def retreat_cf(self, obs):
        ArmyControl.retreat(self, obs, location=[25, 46])

    def retreat_cg(self, obs):
        ArmyControl.retreat(self, obs, location=[25, 53])

    def retreat_da(self, obs):
        ArmyControl.retreat(self, obs, location=[32, 12])

    def retreat_db(self, obs):
        ArmyControl.retreat(self, obs, location=[32, 19])

    def retreat_dc(self, obs):
        ArmyControl.retreat(self, obs, location=[32, 26])

    def retreat_dd(self, obs):
        ArmyControl.retreat(self, obs, location=[32, 33])

    def retreat_de(self, obs):
        ArmyControl.retreat(self, obs, location=[32, 39])

    def retreat_df(self, obs):
        ArmyControl.retreat(self, obs, location=[32, 46])

    def retreat_dg(self, obs):
        ArmyControl.retreat(self, obs, location=[32, 53])

    def retreat_ea(self, obs):
        ArmyControl.retreat(self, obs, location=[38, 12])

    def retreat_eb(self, obs):
        ArmyControl.retreat(self, obs, location=[38, 19])

    def retreat_ec(self, obs):
        ArmyControl.retreat(self, obs, location=[38, 26])

    def retreat_ed(self, obs):
        ArmyControl.retreat(self, obs, location=[38, 33])

    def retreat_ee(self, obs):
        ArmyControl.retreat(self, obs, location=[38, 39])

    def retreat_ef(self, obs):
        ArmyControl.retreat(self, obs, location=[38, 46])

    def retreat_eg(self, obs):
        ArmyControl.retreat(self, obs, location=[38, 53])

    def retreat_fa(self, obs):
        ArmyControl.retreat(self, obs, location=[45, 12])

    def retreat_fb(self, obs):
        ArmyControl.retreat(self, obs, location=[45, 19])

    def retreat_fc(self, obs):
        ArmyControl.retreat(self, obs, location=[45, 26])

    def retreat_fd(self, obs):
        ArmyControl.retreat(self, obs, location=[45, 33])

    def retreat_fe(self, obs):
        ArmyControl.retreat(self, obs, location=[45, 39])

    def retreat_ff(self, obs):
        ArmyControl.retreat(self, obs, location=[45, 46])

    def retreat_fg(self, obs):
        ArmyControl.retreat(self, obs, location=[45, 53])

    def retreat_ga(self, obs):
        ArmyControl.retreat(self, obs, location=[52, 12])

    def retreat_gb(self, obs):
        ArmyControl.retreat(self, obs, location=[52, 19])

    def retreat_gc(self, obs):
        ArmyControl.retreat(self, obs, location=[52, 26])

    def retreat_gd(self, obs):
        ArmyControl.retreat(self, obs, location=[52, 33])

    def retreat_ge(self, obs):
        ArmyControl.retreat(self, obs, location=[52, 39])

    def retreat_gf(self, obs):
        ArmyControl.retreat(self, obs, location=[52, 46])

    def retreat_gg(self, obs):
        ArmyControl.retreat(self, obs, location=[52, 53])
