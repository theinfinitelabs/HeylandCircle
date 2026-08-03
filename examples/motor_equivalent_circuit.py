#%%
# ./examples/motor_equivalent_circuit.py
#
# Sample script to demonstrate the Equivalent Circuit calculations using
# no-load and blocked-rotor test data.
#
# Author:       Anubhav Gupta
# Organization: Abruan Aerospace
# License:      MIT
# 


import numpy as np
import matplotlib.pyplot as plt

from heylandcircle.equivalent_circuit import calculate_equivalent_circuit
from heylandcircle.data_structures import MachineTestData


def main():
    # Test data: 415V three-phase induction machine (two-wattmeter method)
    test_data = MachineTestData(
        I_0=3.85,            # No-load current [A]
        phi_0_deg=85.85,     # No-load power factor angle [deg]
        I_sc=8.4,            # Blocked-rotor current [A]
        phi_sc_deg=66.18,    # Blocked-rotor power factor angle [deg]
        V_rated=415,         # Rated line voltage [V]
        V_sc=80,             # Blocked-rotor test line voltage [V]
        P_rated_kw=None,     # Rated power not required for EC calculation
        R1_dc=None           # Stator resistance at operating temperature [Ω]
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
    
    # Torque-speed curve over slip range (excluding s=0 singularity)
    slips = np.linspace(0.005, 1.0, 500)
    V_phase = test_data.V_rated / np.sqrt(3)
    omega_s = 2 * np.pi * 50  # Synchronous angular frequency [rad/s] at 50 Hz

    torques = []
    for s in slips:
        # Per-phase input impedance (approximate circuit: shunt branch at terminals)
        Z_series = complex(ec.R1 + ec.R2 / s, ec.X1 + ec.X2)
        Z_shunt  = complex(ec.Rc * ec.Xm**2 / (ec.Rc**2 + ec.Xm**2),
                           ec.Rc**2 * ec.Xm / (ec.Rc**2 + ec.Xm**2))
        Z_total  = Z_shunt * Z_series / (Z_shunt + Z_series)

        I1 = V_phase / Z_total                    # Stator current [A]
        I2 = I1 * complex(0, ec.Xm) / (          # Rotor current (referred) [A]
             complex(ec.R2 / s, ec.X2) + complex(0, ec.Xm))

        P_air_gap = 3 * abs(I2)**2 * ec.R2 / s   # Air-gap power [W]
        T_em = P_air_gap / omega_s                # Electromagnetic torque [N·m]
        torques.append(T_em)

    torques = np.array(torques)
    speeds  = (1 - slips) * omega_s              # Rotor angular speed [rad/s]

    # Plot torque-speed curve
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(speeds, torques, linewidth=2, color="steelblue")
    ax.set_xlabel("Rotor Speed [rad/s]")
    ax.set_ylabel("Electromagnetic Torque [N·m]")
    ax.set_title("Torque-Speed Curve — Equivalent Circuit")
    ax.grid(True, linestyle="--", alpha=0.6)
    ax.axvline(omega_s, color="gray", linestyle=":", linewidth=1, label="Synchronous speed")
    ax.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()