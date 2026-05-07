import pytest
import matplotlib

# Use non-interactive backend for testing
matplotlib.use("Agg")

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
        I0=3.85,
        phi0_deg=85.85,
        Isc=8.4,
        phi_sc_deg=66.18,
        V_rated=415,
        V_sc=80,
        P_rated_kw=5.5,
    )


@pytest.fixture
def diagram(sample_config, sample_data):
    return CircleDiagram(sample_config, sample_data)


# ------------------------------------------------------------------
# Geometry construction
# ------------------------------------------------------------------

def test_build_geometry_runs(diagram):
    diagram._build_geometry()

    assert diagram.circle is not None
    assert diagram.p0 is not None
    assert diagram.psn is not None
    assert diagram.pP is not None


def test_circle_radius_positive(diagram):
    diagram._build_geometry()

    assert diagram.circle.r > 0


def test_key_points_are_finite(diagram):
    diagram._build_geometry()

    points = [
        diagram.p0,
        diagram.psn,
        diagram.pP,
        diagram.pM_O,
        diagram.pM_T,
    ]

    for p in points:
        assert p is not None
        assert p.x == pytest.approx(p.x)
        assert p.y == pytest.approx(p.y)


# ------------------------------------------------------------------
# Results computation
# ------------------------------------------------------------------

def test_compute_results_runs(diagram):
    diagram._build_geometry()
    diagram._compute_results()

    assert diagram.results is not None


def test_efficiency_bounds(diagram):
    diagram._build_geometry()
    diagram._compute_results()

    assert 0.0 <= diagram.results.efficiency <= 100.0


def test_power_factor_bounds(diagram):
    diagram._build_geometry()
    diagram._compute_results()

    assert 0.0 <= diagram.results.power_factor <= 1.0


def test_slip_bounds(diagram):
    diagram._build_geometry()
    diagram._compute_results()

    assert 0.0 <= diagram.results.slip <= 100.0


def test_losses_positive(diagram):
    diagram._build_geometry()
    diagram._compute_results()

    assert diagram.results.total_loss >= 0.0
    assert diagram.results.copper_loss >= 0.0
    assert diagram.results.fixed_loss >= 0.0


def test_scaled_quantities_exist(diagram):
    diagram._build_geometry()
    diagram._compute_results()

    assert diagram.results.total_loss_kW is not None
    assert diagram.results.max_output_kW is not None


# ------------------------------------------------------------------
# Plotting
# ------------------------------------------------------------------

def test_plot_runs(diagram):
    fig, ax = diagram.plot()

    assert fig is not None
    assert ax is not None


def test_plot_save(tmp_path, diagram):
    output_file = tmp_path / "circle_diagram.png"

    fig, ax = diagram.plot(save_path=str(output_file))

    assert output_file.exists()


# ------------------------------------------------------------------
# Configuration behavior
# ------------------------------------------------------------------

def test_plot_without_optional_scales(sample_data):
    config = CircleDiagramConfig(
        power_scale=1.0,
        current_scale=1.0,
        show_eff_scale=False,
        show_slip_scale=False,
        show_pf_curve=False,
        show_full_circle=False,
        show_grid=False,
    )

    diagram = CircleDiagram(config, sample_data)

    fig, ax = diagram.plot()

    assert fig is not None
    assert ax is not None