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