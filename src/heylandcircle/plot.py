# ---------------------------------------------------------------------
# src/heylandcircle/plot.py
#
# Plotting and annotation utilities for the Heyland circle diagram.
# Handles phasor rendering, arc drawing, point annotation, and other
# Matplotlib-based visual helpers.
#
# Author:       Anubhav Gupta
# Affiliation:  University of Colorado Boulder
#               In Orbit Aerospace
# Organization: Infinite Labs
# License:      MIT
# ---------------------------------------------------------------------


from __future__ import annotations
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.patches import Arc

from heylandcircle.geometry import Point, Line, Circle

def plot_phasor(
    ax: Axes,
    p: Point,
    label: str | None = None,
    color: str = "gray",
    linewidth: float = 1.0,
) -> None:
    """Draw a phasor from the origin to point p."""
    ax.plot([0, p.x], [0, p.y], color=color, linewidth=linewidth, label=label)


def draw_arc(
    ax: Axes,
    circle: Circle,
    start_angle_deg: float,
    end_angle_deg: float,
    color: str = "blue",
    linestyle: str = "-",
    linewidth: float = 1.5,
    label: str | None = None,
) -> Arc:
    """Draw a circular arc defined by a Circle and an angular extent.

    Args:
        ax:               Target Matplotlib axes.
        circle:           Circle whose center and radius define the arc.
        start_angle_deg:  Start angle in degrees (Matplotlib convention: CCW from +x).
        end_angle_deg:    End angle in degrees.
        color:            Line color.
        linestyle:        Line style (e.g. '-', '--').
        linewidth:        Line width.
        label:            Optional legend label.

    Returns:
        The Arc patch added to ax.
    """
    arc = Arc(
        (circle.center.x, circle.center.y),
        2 * circle.r, 2 * circle.r,
        angle=0,
        theta1=start_angle_deg,
        theta2=end_angle_deg,
        color=color,
        linestyle=linestyle,
        linewidth=linewidth,
        label=label,
    )
    ax.add_patch(arc)
    return arc