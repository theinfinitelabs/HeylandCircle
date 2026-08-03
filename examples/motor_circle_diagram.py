#%%
# ./examples/motor_circle_diagram.py
#
# Sample script to demonstrate the Heyland circle diagram using test data.
#
# Author:       Anubhav Gupta
# Organization: Abruan Aerospace
# License:      MIT
# 


import matplotlib.pyplot as plt

from heylandcircle.circle_diagram import CircleDiagram
from heylandcircle.data_structures import CircleDiagramConfig, MachineTestData

def main():
    # Sample test data for a 10 kW induction machine
    test_data = MachineTestData(
        I_0=6,               # No-load current [A]
        phi_0_deg=85,        # No-load current angle [deg]
        I_sc=12.0,           # Blocked-rotor current [A]
        phi_sc_deg=69.0667,  # Blocked-rotor current angle [deg]
        V_rated=400,         # Rated voltage [V]
        V_sc=100,            # Blocked-rotor test voltage [V]
        P_rated_kw=5.6,      # Rated power [kW]
        R1_dc=None           # Stator resistance at operating temperature [Ω]
    )

    # Circle diagram configuration
    config = CircleDiagramConfig(
        power_scale=1.4,           # x kW/cm
        current_scale=1 / 2,       # 1/x implies 1 cm = x Amps
        show_eff_scale=True,       # whether to show slip scale on diagram
        show_slip_scale=True,      # whether to show slip scale on diagram
        show_pf_curve=True,        # whether to show power factor curve scale on diagram
        show_full_circle=False,    # whether to show full circle on diagram
        show_grid=True             # whether to show grid lines on diagram
    )

    cd = CircleDiagram(config, test_data)
    fig, ax = cd.plot()
    plt.show()
    
    # Build 3-column results table
    r = cd.results
    rows = [
        ["Input Power",         f"{r.power_input:.2f}",        f"{r.power_input_kW:.2f} kW"       if r.power_input_kW else "-"],
        ["Total Loss",          f"{r.total_loss:.2f}",         f"{r.total_loss_kW:.2f} kW"        if r.total_loss_kW else "-"],
        ["Copper Loss",         f"{r.copper_loss:.2f}",        f"{r.copper_loss_kW:.2f} kW"       if r.copper_loss_kW else "-"],
        ["Rotor Cu Loss",       f"{r.rotor_copper_loss:.2f}",  f"{r.rotor_copper_loss_kW:.2f} kW" if r.rotor_copper_loss_kW else "-"],
        ["Fixed Loss",          f"{r.fixed_loss:.2f}",         f"{r.fixed_loss_kW:.2f} kW"        if r.fixed_loss_kW else "-"],
        ["Max Output",          f"{r.max_output:.2f}",         f"{r.max_output_kW:.2f} kW"        if r.max_output_kW else "-"],
        ["Max Torque",          f"{r.max_torque:.2f}",         f"{r.max_torque_kW:.2f} Sync kW"        if r.max_output_kW else "-"],
        ["Efficiency",          f"{r.efficiency/100:.2f}",     f"{r.efficiency:.2f} %"],
        ["Slip (power-based)",  f"{r.slip/100:.2f}",           f"{r.slip:.2f} %"],
        ["Line Current",        f"{r.line_current:.2f}",       f"{r.line_current/config.current_scale:.2f} A"],
        ["Power Factor",        f"{r.power_factor:.2f}",       "-"],
    ]

    # Print the table to console
    print("======================== RESULTS SUMMARY ========================")
    print(f"{'Parameter':<22} {'Geometric Value':<20} {'Calibrated Value':<20}")
    print("-" * 65)

    for param, geom, calib in rows:
        print(f"{param:<22} {geom:<20} {calib:<20}")

    print("=" * 65)
    
if __name__ == "__main__":
    main()