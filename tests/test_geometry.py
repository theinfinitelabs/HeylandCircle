import numpy as np
import pytest

from heylandcircle.geometry import (
    distance,
    slope_from_points,
    y_intercept,
    phasor_to_point,
    line_line_intersection,
    line_circle_intersection,
)

from heylandcircle.data_structures import Point, Line, Circle


# ------------------------------------------------------------------
# distance
# ------------------------------------------------------------------

def test_distance_basic():
    p1 = Point(0, 0)
    p2 = Point(3, 4)

    assert distance(p1, p2) == pytest.approx(5.0)


# ------------------------------------------------------------------
# slope_from_points
# ------------------------------------------------------------------

def test_slope_from_points():
    p1 = Point(0, 0)
    p2 = Point(2, 4)

    assert slope_from_points(p1, p2) == pytest.approx(2.0)


def test_slope_vertical_line():
    p1 = Point(1, 0)
    p2 = Point(1, 5)

    with pytest.raises(ValueError):
        slope_from_points(p1, p2)


# ------------------------------------------------------------------
# y_intercept
# ------------------------------------------------------------------

def test_y_intercept():
    assert y_intercept(2, 5, 1.5) == pytest.approx(2.0)


# ------------------------------------------------------------------
# phasor_to_point
# ------------------------------------------------------------------

def test_phasor_to_point_cw():
    p = phasor_to_point(1.0, 0.0, direction="cw")

    assert p.x == pytest.approx(0.0, abs=1e-10)
    assert p.y == pytest.approx(1.0, abs=1e-10)


def test_phasor_to_point_ccw():
    p = phasor_to_point(1.0, 90.0, direction="ccw")

    assert p.x == pytest.approx(-1.0, abs=1e-10)
    assert p.y == pytest.approx(0.0, abs=1e-10)


# ------------------------------------------------------------------
# line_line_intersection
# ------------------------------------------------------------------

def test_line_line_intersection_normal():
    l1 = Line(m=1.0, c=0.0)
    l2 = Line(m=-1.0, c=2.0)

    p = line_line_intersection(l1, l2)

    assert p is not None
    assert p.x == pytest.approx(1.0)
    assert p.y == pytest.approx(1.0)


def test_line_line_intersection_parallel():
    l1 = Line(m=1.0, c=0.0)
    l2 = Line(m=1.0, c=2.0)

    assert line_line_intersection(l1, l2) is None


def test_line_line_vertical_horizontal():
    l1 = Line(x_vert=2.0)
    l2 = Line(y_horz=3.0)

    p = line_line_intersection(l1, l2)

    assert p is not None
    assert p.x == pytest.approx(2.0)
    assert p.y == pytest.approx(3.0)


# ------------------------------------------------------------------
# line_circle_intersection
# ------------------------------------------------------------------

def test_line_circle_intersection():
    line = Line(m=0.0, c=0.0)

    circle = Circle(
        center=Point(0.0, 0.0),
        r=5.0,
    )

    p = line_circle_intersection(line, circle)

    assert p is not None
    assert p.x == pytest.approx(-5.0)
    assert p.y == pytest.approx(0.0)


def test_line_circle_no_intersection():
    line = Line(m=0.0, c=10.0)

    circle = Circle(
        center=Point(0.0, 0.0),
        r=5.0,
    )

    assert line_circle_intersection(line, circle) is None


def test_line_circle_requires_normal_line():
    line = Line(x_vert=2.0)

    circle = Circle(
        center=Point(0.0, 0.0),
        r=5.0,
    )

    with pytest.raises(ValueError):
        line_circle_intersection(line, circle)