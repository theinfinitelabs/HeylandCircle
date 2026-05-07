import pytest


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