# ---------------------------------------------------------------------
# src/heylandcircle/geometry.py
#
# Geometric primitives and plotting utilities for the Heyland circle
# diagram. Provides point/line/circle operations, phasor conversion,
# arc rendering, and annotation helpers.
#
# Author:       Anubhav Gupta
# Affiliation:  University of Colorado Boulder
#               In Orbit Aerospace
# Organization: Infinite Labs
# License:      MIT
# ---------------------------------------------------------------------


import numpy as np

# ------------------------------------------------------------------
# Point / scalar utilities
# ------------------------------------------------------------------

def distance(p1: Point, p2: Point) -> float:
    """Euclidean distance between two points."""
    return np.hypot(p2.x - p1.x, p2.y - p1.y)


def slope_from_points(p1: Point, p2: Point) -> float:
    """Slope of the line through p1 and p2. Raises ValueError for vertical lines."""
    if np.isclose(p1.x, p2.x):
        raise ValueError("Vertical line: slope undefined.")
    return (p2.y - p1.y) / (p2.x - p1.x)


def y_intercept(x: float, y: float, m: float) -> float:
    """Y-intercept of the line through (x, y) with slope m."""
    return y - m * x


def phasor_to_point(
    length: float,
    angle_deg: float,
    direction: Literal["cw", "ccw"] = "cw",
) -> Point:
    """Cartesian endpoint of a phasor with given magnitude and angle from vertical.

    Args:
        length:     Phasor magnitude.
        angle_deg:  Angle measured from the vertical axis.
        direction:  'cw' (clockwise, default) or 'ccw' (counter-clockwise).
    """
    offset = 90.0 - angle_deg if direction == "cw" else 90.0 + angle_deg
    theta = np.deg2rad(offset)
    return Point(length * np.cos(theta), length * np.sin(theta))


# ------------------------------------------------------------------
# Intersection solvers
# ------------------------------------------------------------------

def line_line_intersection(l1: Line, l2: Line) -> Point | None:
    """Intersection of two lines. Returns None for parallel or degenerate cases.

    Each Line encodes one of: normal (m, c), vertical (x_vert), horizontal (y_horz).
    """
    # Both lines are vertical
    if l1.x_vert is not None and l2.x_vert is not None:
        return None

    # Both lines are horizontal
    if l1.y_horz is not None and l2.y_horz is not None:
        return None

    # One line is vertical and other is horizontal
    if l1.x_vert is not None and l2.y_horz is not None:
        return Point(l1.x_vert, l2.y_horz)
    if l2.x_vert is not None and l1.y_horz is not None:
        return Point(l2.x_vert, l1.y_horz)

    # One line is vertical and other is normal
    if l1.x_vert is not None:
        if l2.m is None or l2.c is None:
            return None
        return Point(l1.x_vert, l2.m * l1.x_vert + l2.c)
    if l2.x_vert is not None:
        if l1.m is None or l1.c is None:
            return None
        return Point(l2.x_vert, l1.m * l2.x_vert + l1.c)

    # One line is horizontal and other is normal
    if l1.y_horz is not None:
        if l2.m is None or l2.c is None:
            return None
        return Point((l1.y_horz - l2.c) / l2.m, l1.y_horz)
    if l2.y_horz is not None:
        if l1.m is None or l1.c is None:
            return None
        return Point((l2.y_horz - l1.c) / l1.m, l2.y_horz)

    # Both lines are normal
    if any(v is None for v in (l1.m, l1.c, l2.m, l2.c)):
        return None
    if np.isclose(l1.m, l2.m):
        return None
    x = (l2.c - l1.c) / (l1.m - l2.m)
    return Point(x, l1.m * x + l1.c)


def line_circle_intersection(line: Line, circle: Circle) -> Point | None:
    """Leftmost intersection of a normal line with a circle.

    Args:
        line:   A Line with m and c defined (y = mx + c).
        circle: Target circle.

    Returns:
        The leftmost intersection Point, or None if the line does not intersect.
    """
    if line.m is None or line.c is None:
        raise ValueError("line_circle_intersection requires a normal line (m and c).")

    m, c = line.m, line.c
    h, k, r = circle.center.x, circle.center.y, circle.r

    A = 1 + m**2
    B = 2 * m * (c - k) - 2 * h
    C = h**2 + (c - k)**2 - r**2

    discriminant = B**2 - 4 * A * C
    if discriminant < 0:
        return None

    x1 = (-B + np.sqrt(discriminant)) / (2 * A)
    x2 = (-B - np.sqrt(discriminant)) / (2 * A)
    x = min(x1, x2)
    return Point(x, m * x + c)