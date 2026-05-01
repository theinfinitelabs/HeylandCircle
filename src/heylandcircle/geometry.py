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