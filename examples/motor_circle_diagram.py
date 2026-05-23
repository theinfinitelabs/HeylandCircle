#%%
# ---------------------------------------------------------------------
# ./examples/motor_circle_diagram.py
#
# Sample script to demonstrate the Heyland circle diagram using test data.
#
# Author:       Anubhav Gupta
# Affiliation:  University of Colorado Boulder
#               In Orbit Aerospace
# Organization: Infinite Labs
# License:      MIT
# ---------------------------------------------------------------------

import matplotlib.pyplot as plt

from heylandcircle.circle_diagram import CircleDiagram
from heylandcircle.data_structures import CircleDiagramConfig, MachineTestData

def main():
    # Sample test data for a 10 kW induction machine
    test_data = MachineTestData(
        I_0=6,               # No-load current [A]
        phi_0_deg=85,        # No-load current angle [deg]
        I_sc=12.0,           # Blocked-rotor current [A]
        phi_sc_deg=69.0667, # Blocked-rotor current angle [deg]
        V_rated=400,        # Rated voltage [V]
        V_sc=100,           # Blocked-rotor test voltage [V]
        P_rated_kw=5.6      # Rated power [kW]
    )

    # Circle diagram configuration
    config = CircleDiagramConfig(
        power_scale=1.4,          # x kW/cm
        current_scale=1 / 2,       # 1/x implies 1 cm = x Amps
        show_eff_scale=True,       # whether to show slip scale on diagram
        show_slip_scale=True,      # whether to show slip scale on diagram
        show_pf_curve=True,        # whether to show power factor curve scale on diagram
        show_full_circle=False,     # whether to show full circle on diagram
        show_grid=True             # whether to show grid lines on diagram
    )

    cd = CircleDiagram(config, test_data)
    fig, ax = cd.plot()
    plt.show()
    
    
if __name__ == "__main__":
    main()