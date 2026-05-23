import pytest

from heylandcircle.data_structures import (
    MachineTestData,
    Point,
    Circle,
    Line,
    CircleResults,
)


# ------------------------------------------------------------------
# MachineTestData
# ------------------------------------------------------------------

def test_machine_test_data_starting_current():
    data = MachineTestData(
        I_0=5.0,
        phi_0_deg=80.0,
        I_sc=20.0,
        phi_sc_deg=45.0,
        V_rated=400.0,
        V_sc=100.0,
        P_rated_kw=15.0,
    )

    assert data.I_start == pytest.approx(80.0)


# ------------------------------------------------------------------
# Point
# ------------------------------------------------------------------

def test_point_creation():
    p = Point(1.5, -2.0)

    assert p.x == 1.5
    assert p.y == -2.0


# ------------------------------------------------------------------
# Circle
# ------------------------------------------------------------------

def test_circle_creation():
    circle = Circle(
        center=Point(0.0, 0.0),
        r=5.0,
    )

    assert circle.center.x == 0.0
    assert circle.center.y == 0.0
    assert circle.r == 5.0


# ------------------------------------------------------------------
# Line
# ------------------------------------------------------------------

def test_line_normal_form():
    line = Line(m=2.0, c=1.0)

    assert line.m == 2.0
    assert line.c == 1.0


def test_line_vertical_form():
    line = Line(x_vert=3.0)

    assert line.x_vert == 3.0


def test_line_horizontal_form():
    line = Line(y_horz=-1.0)

    assert line.y_horz == -1.0


def test_line_invalid_multiple_forms():
    with pytest.raises(ValueError):
        Line(
            m=1.0,
            c=2.0,
            x_vert=5.0,
        )


def test_line_invalid_missing_c():
    with pytest.raises(ValueError):
        Line(m=1.0)


def test_line_invalid_missing_m():
    with pytest.raises(ValueError):
        Line(c=2.0)


def test_line_invalid_empty_definition():
    with pytest.raises(ValueError):
        Line()


# ------------------------------------------------------------------
# CircleResults
# ------------------------------------------------------------------

def test_circle_results_defaults():
    results = CircleResults()

    assert results.total_loss == 0.0
    assert results.efficiency == 0.0
    assert results.power_factor == 0.0
    assert results.total_loss_kW is None
    assert results.max_output_kW is None