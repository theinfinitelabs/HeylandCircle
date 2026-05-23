#%%
# ---------------------------------------------------------------------
# ./examples/motor_equivalent_circuit.py
#
# Sample script to demonstrate the Equivalent Circuit calculations using
# no-load and blocked-rotor test data.
#
# Author:       Anubhav Gupta
# Affiliation:  University of Colorado Boulder
#               In Orbit Aerospace
# Organization: Infinite Labs
# License:      MIT
# ---------------------------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt

from heylandcircle.equivalent_circuit import calculate_equivalent_circuit
from heylandcircle.data_structures import MachineTestData


def main():
    # Test data: 415V three-phase induction machine (two-wattmeter method)
    test_data = MachineTestData(
        I_0=3.85,            # No-load current [A]
        phi_0_deg=85.85,     # No-load power factor angle [deg]
        I_sc=8.4,           # Blocked-rotor current [A]
        phi_sc_deg=66.18,   # Blocked-rotor power factor angle [deg]
        V_rated=415,        # Rated line voltage [V]
        V_sc=80,            # Blocked-rotor test line voltage [V]
        P_rated_kw=None     # Rated power not required for EC calculation
    )

    # Calculate equivalent circuit parameters
    ec = calculate_equivalent_circuit(test_data)

    # Print equivalent circuit parameters
    print("=" * 40)
    print("  Equivalent Circuit Parameters")
    print("=" * 40)
    print(f"  R1  = {ec.R1:.4f}  Ω  (Stator resistance)")
    print(f"  X1  = {ec.X1:.4f}  Ω  (Stator reactance)")
    print(f"  Rc  = {ec.Rc:.4f}  Ω  (Core loss resistance)")
    print(f"  Xm  = {ec.Xm:.4f}  Ω  (Magnetizing reactance)")
    print(f"  R2' = {ec.R2:.4f}  Ω  (Rotor resistance, referred)")
    print(f"  X2' = {ec.X2:.4f}  Ω  (Rotor reactance, referred)")
    print("=" * 40)


if __name__ == "__main__":
    main()