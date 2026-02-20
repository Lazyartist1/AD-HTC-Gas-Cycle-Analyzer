import numpy as np
from iapws import IAPWS97

class CycleEngine:
    def __init__(self):
        self.cp_air = 1.005  # kJ/kgK
        self.gamma_air = 1.4
        self.cp_gas = 1.15   # kJ/kgK (exhaust gas)
        self.gamma_gas = 1.33

    def analyze_ad_htc_system(self, gt_temp_c, comp_ratio, htc_press_bar, biomass_flow_kgs):
        """
        Integrated AD-HTC Gas Cycle Analysis
        """
        # 1. Anaerobic Digestion (AD)
        # Assume 0.3 kg biogas per kg biomass
        biogas_flow = biomass_flow_kgs * 0.3
        lcv_biogas = 22000  # kJ/kg (approx 60% CH4)
        heat_input = biogas_flow * lcv_biogas  # kW

        # 2. Gas Turbine Cycle (Brayton)
        t1 = 288.15  # 15°C
        # Compression
        t2s = t1 * (comp_ratio ** ((self.gamma_air - 1) / self.gamma_air))
        eta_c = 0.85
        t2 = t1 + (t2s - t1) / eta_c
        w_comp = self.cp_air * (t2 - t1)

        # Combustion & Expansion
        t3 = gt_temp_c + 273.15
        t4s = t3 * (1 / comp_ratio) ** ((self.gamma_gas - 1) / self.gamma_gas)
        eta_t = 0.88
        t4 = t3 - eta_t * (t3 - t4s)
        w_turb = self.cp_gas * (t3 - t4)

        w_net_gt = w_turb - w_comp
        # Air flow roughly based on heat input
        # Q_in = m_air * cp * (T3 - T2)
        m_air = heat_input / (self.cp_air * (t3 - t2))
        power_gt = w_net_gt * m_air / 1000  # MW

        # 3. HTC Process Integration
        # HTC Reactor at htc_press_bar (~200-250°C)
        t_htc = IAPWS97(P=htc_press_bar/10, x=0).T - 273.15
        # Steam required for HTC heating (simplified energy balance)
        # Heat required = biomass_flow * cp_water * (T_htc - T_ambient)
        q_htc = biomass_flow_kgs * 4.18 * (t_htc - 20)  # kW

        # 4. Heat Recovery Steam Generator (HRSG)
        # Exhaust gas from t4 down to t_stack
        t_stack = 120  # °C
        q_available = m_air * self.cp_gas * (t4 - (t_stack + 273.15))
        
        # Steam cycle power (Rankine)
        # Remaining heat after HTC is used for power
        q_for_steam = q_available - q_htc
        eta_steam = 0.25 # Typical Rankine efficiency for this scale
        power_st = max(0, q_for_steam * eta_steam / 1000) # MW

        # 5. Combined Metrics
        total_power = power_gt + power_st
        total_efficiency = total_power * 1000 / heat_input
        co2_reduction = 15 + (biomass_flow_kgs * 0.8) # Arbitrary based on carbon sequestration in hydrochar

        # Visualization Data
        return {
            "metrics": {
                "efficiency": total_efficiency, # 0-1 scale
                "power": total_power,
                "co2": co2_reduction
            },
            "charts": {
                "hs": self.generate_hs_data(htc_press_bar),
                "th": self.generate_th_data(t4-273.15, gt_temp_c, t_htc, q_available, q_htc)
            }
        }

    def generate_hs_data(self, p_htc):
        """Generates Rankine cycle h-s curve for the steam sub-cycle"""
        # Simplistic cycle points
        p_high = p_htc * 1.5
        p_low = 0.1
        
        s_vals = [1.5, 1.5, 7.5, 7.5, 1.5]
        h_vals = [500, 520, 3200, 2200, 500]
        
        return {"s": s_vals, "h": h_vals}

    def generate_th_data(self, t_exhaust, t_combust, t_htc, q_avail, q_htc):
        """Generates T-H diagram showing heat transfer from GT exhaust"""
        # Gas cooling curve
        gas_h = [0, q_avail]
        gas_t = [t_exhaust, 120]
        
        # Steam/HTC heating curve
        # Water heats to T_htc, stays for reaction, then potential steam power
        steam_h = [0, q_htc, q_avail]
        steam_t = [30, t_htc, t_htc + 50]
        
        return {
            "gas_H": gas_h,
            "gas_T": gas_t,
            "steam_H": steam_h,
            "steam_T": steam_t
        }
