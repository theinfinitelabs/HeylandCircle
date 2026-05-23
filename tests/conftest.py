import pytest

from heylandcircle.circle_diagram import CircleDiagram
from heylandcircle.data_structures import (
    CircleDiagramConfig,
    MachineTestData,
)

# ------------------------------------------------------------------
# Fixtures
# ------------------------------------------------------------------

@pytest.fixture
def sample_config():
    return CircleDiagramConfig(
        power_scale=1.0,
        current_scale=1.0,
        show_eff_scale=True,
        show_slip_scale=True,
        show_pf_curve=True,
        show_full_circle=False,
        show_grid=False,
    )


@pytest.fixture
def sample_data():
    return MachineTestData(
        I_0=3.85,
        phi_0_deg=85.85,
        I_sc=8.4,
        phi_sc_deg=66.18,
        V_rated=415,
        V_sc=80,
        P_rated_kw=5.5,
    )


@pytest.fixture
def diagram(sample_config, sample_data):
    return CircleDiagram(sample_config, sample_data)
