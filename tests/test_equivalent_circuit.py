# ---------------------------------------------------------------------
# tests/test_equivalent_circuit.py
#
# Pytest suite for equivalent circuit parameter calculations.
# Test result based on paper "Induction Motor Parameters Extraction"
#   by Sinisa Jurkovic
#   https://web.mit.edu/kirtley/binlustuff/literature/electric%20machine/motor-parameters.pdf
# ---------------------------------------------------------------------

import numpy as np
import pytest

from heylandcircle.data_structures import EquivalentCircuit, MachineTestData
from heylandcircle.equivalent_circuit import calculate_equivalent_circuit


# ------------------------------------------------------------------
# Fixtures — mirrors conftest.py style
# ------------------------------------------------------------------

@pytest.fixture
def sample_data():
    """Real-world 5.5 kW motor test data (same machine as circle diagram tests)."""
    return MachineTestData(
        I_0=1.5,
        phi_0_deg=84.8,
        I_sc=6.1,
        phi_sc_deg=64,
        V_rated=208,
        V_sc=90,
        P_rated_kw=0.724,
        R1_dc=None
    )


@pytest.fixture
def ec(sample_data):
    return calculate_equivalent_circuit(sample_data)


# ------------------------------------------------------------------
# Return type
# ------------------------------------------------------------------

def test_returns_equivalent_circuit(ec):
    assert isinstance(ec, EquivalentCircuit)


def test_all_fields_are_floats(ec):
    for field in ("R1", "X1", "Rc", "Xm", "R2", "X2"):
        assert isinstance(getattr(ec, field), float), f"{field} is not float"


# ------------------------------------------------------------------
# No-load branch: Rc and Xm
# ------------------------------------------------------------------

def test_Rc_expected_value(sample_data, ec):
    V0 = sample_data.V_rated / np.sqrt(3)
    phi = np.deg2rad(sample_data.phi_0_deg)
    expected = V0 / (sample_data.I_0 * np.cos(phi))
    assert ec.Rc == pytest.approx(expected, rel=1e-6)


def test_Xm_expected_value(sample_data, ec):
    V0 = sample_data.V_rated / np.sqrt(3)
    phi = np.deg2rad(sample_data.phi_0_deg)
    expected = V0 / (sample_data.I_0 * np.sin(phi))
    assert ec.Xm == pytest.approx(expected, rel=1e-6)


# ------------------------------------------------------------------
# Blocked-rotor branch: R1, X1, R2, X2
# ------------------------------------------------------------------

def test_equal_split_R1_eq_R2(ec):
    assert ec.R1 == pytest.approx(ec.R2, rel=1e-9)


def test_equal_split_X1_eq_X2(ec):
    assert ec.X1 == pytest.approx(ec.X2, rel=1e-9)


def test_series_resistance_sum(sample_data, ec):
    V_sc = sample_data.V_sc / np.sqrt(3)
    Z_sc = V_sc / sample_data.I_sc
    R_sc = Z_sc * np.cos(np.deg2rad(sample_data.phi_sc_deg))
    assert ec.R1 + ec.R2 == pytest.approx(R_sc, rel=1e-6)


def test_series_reactance_sum(sample_data, ec):
    V_sc = sample_data.V_sc / np.sqrt(3)
    Z_sc = V_sc / sample_data.I_sc
    X_sc = Z_sc * np.sin(np.deg2rad(sample_data.phi_sc_deg))
    assert ec.X1 + ec.X2 == pytest.approx(X_sc, rel=1e-6)


# ------------------------------------------------------------------
# Physical invariants
# ------------------------------------------------------------------

def test_Xm_greater_than_X1(ec):
    """Magnetizing reactance must dominate leakage reactance."""
    assert ec.Xm > ec.X1


def test_Rc_greater_than_R1(ec):
    """Core loss resistance must dominate stator resistance."""
    assert ec.Rc > ec.R1


def test_no_load_angle_reconstructs(sample_data, ec):
    """Rc and Xm must reproduce the original phi_0."""
    V0 = sample_data.V_rated / np.sqrt(3)
    Ic = V0 / ec.Rc   # active component → cos branch
    Im = V0 / ec.Xm   # reactive component → sin branch
    phi_reconstructed = np.rad2deg(np.arctan2(Im, Ic))  # angle from active axis = phi_0
    assert phi_reconstructed == pytest.approx(sample_data.phi_0_deg, rel=1e-5)


def test_blocked_rotor_angle_reconstructs(sample_data, ec):
    """R_sc and X_sc must reproduce the original phi_sc."""
    R_sc = ec.R1 + ec.R2
    X_sc = ec.X1 + ec.X2
    phi_reconstructed = np.rad2deg(np.arctan2(X_sc, R_sc))
    assert phi_reconstructed == pytest.approx(sample_data.phi_sc_deg, rel=1e-5)


# ------------------------------------------------------------------
# I_start property
# ------------------------------------------------------------------

def test_I_start_scales_correctly(sample_data):
    expected = sample_data.I_sc * (sample_data.V_rated / sample_data.V_sc)
    assert sample_data.I_start == pytest.approx(expected, rel=1e-9)


def test_I_start_greater_than_I_sc(sample_data):
    """V_rated > V_sc → starting current must exceed blocked-rotor test current."""
    assert sample_data.I_start > sample_data.I_sc


# ------------------------------------------------------------------
# Edge cases
# ------------------------------------------------------------------

def test_unity_pf_blocked_rotor_gives_zero_reactance():
    """phi_sc = 0 → purely resistive series branch → X1 = X2 = 0."""
    data = MachineTestData(
        I_0=3.85, phi_0_deg=85.85,
        I_sc=8.4, phi_sc_deg=0.0,
        V_rated=415, V_sc=80, P_rated_kw=5.5,
        R1_dc=None
    )
    ec = calculate_equivalent_circuit(data)
    assert ec.X1 == pytest.approx(0.0, abs=1e-10)
    assert ec.X2 == pytest.approx(0.0, abs=1e-10)


def test_voltage_scaling_doubles_impedance():
    """Doubling both voltages at same currents → 4x all impedances (Z ∝ V²/P ∝ V)."""
    base = MachineTestData(
        I_0=3.85, phi_0_deg=85.85,
        I_sc=8.4, phi_sc_deg=66.18,
        V_rated=415, V_sc=80, P_rated_kw=5.5,
        R1_dc=None
    )
    scaled = MachineTestData(
        I_0=3.85, phi_0_deg=85.85,
        I_sc=8.4, phi_sc_deg=66.18,
        V_rated=830, V_sc=160, P_rated_kw=5.5,
        R1_dc=None
    )
    ec_base = calculate_equivalent_circuit(base)
    ec_scaled = calculate_equivalent_circuit(scaled)

    for field in ("R1", "X1", "Rc", "Xm", "R2", "X2"):
        assert getattr(ec_scaled, field) == pytest.approx(
            2 * getattr(ec_base, field), rel=1e-6
        ), f"{field} did not scale 2x with 2x voltage"