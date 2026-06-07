# ---------------------------------------------------------------------
# src/heylandcircle/equivalent_circuit.py
#
# Equivalent circuit per phase calculations for induction machines.
#
# Author:       Anubhav Gupta
# Affiliation:  University of Colorado Boulder
#               In Orbit Aerospace
# Organization: Infinite Labs
# License:      MIT
# ---------------------------------------------------------------------

from dataclasses import dataclass
import numpy as np

from heylandcircle.data_structures import EquivalentCircuit

def calculate_equivalent_circuit(test_data) -> EquivalentCircuit:
    """Calculate equivalent circuit parameters from machine test data.

    Args:
        test_data: MachineTestData containing no-load and blocked-rotor test results.

    Returns:
        EquivalentCircuit: Calculated equivalent circuit parameters.
    """
    # --- No-load test: shunt branch (Rc, Xm) ---
    V0 = test_data.V_rated / np.sqrt(3)      # Per-phase voltage
    I_0 = test_data.I_0
    phi0_rad = np.deg2rad(test_data.phi_0_deg)

    Rc = V0 / (I_0 * np.cos(phi0_rad))        # Core loss resistance
    Xm = V0 / (I_0 * np.sin(phi0_rad))        # Magnetizing reactance

    # --- Blocked rotor test: series branch (R1, X1, R2, X2) ---
    V_sc = test_data.V_sc / np.sqrt(3)       # Per-phase voltage
    I_sc = test_data.I_sc
    phi_sc_rad = np.deg2rad(test_data.phi_sc_deg)

    Z_sc = V_sc / I_sc
    R_sc = Z_sc * np.cos(phi_sc_rad)         # Total series resistance
    X_sc = Z_sc * np.sin(phi_sc_rad)         # Total series reactance

    # Equal split assumption (general-purpose motor; use 0.4/0.6 for wound rotor)
    if test_data.R1_dc is None:
        R1 = R_sc / 2
        R2 = R_sc / 2
    X1 = X_sc / 2
    X2 = X_sc / 2

    return EquivalentCircuit(R1=R1, X1=X1, Rc=Rc, Xm=Xm, R2=R2, X2=X2)