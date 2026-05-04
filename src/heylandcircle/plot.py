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
    center: Point,
    radius: float,
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
        center:           Center point of the arc.
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
        (center.x, center.y),
        2 * radius, 2 * radius,
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


def annotate_point(
    ax: Axes,
    p: Point,
    text: str,
    x_offset: float = 0.03,
    y_offset: float = 0.03,
    fontsize: int = 9,
    ha: str = "center",
    va: str = "center",
) -> None:
    """Annotate a point with a text label offset by a fraction of the axis span.

    Args:
        ax:       Target Matplotlib axes.
        p:        Point to annotate.
        text:     Label text.
        x_offset: Horizontal offset as a fraction of the x-axis span.
        y_offset: Vertical offset as a fraction of the y-axis span.
        fontsize: Font size of the label.
        ha:       Horizontal alignment ('left', 'center', 'right').
        va:       Vertical alignment ('top', 'center', 'bottom').
    """
    xspan = ax.get_xlim()[1] - ax.get_xlim()[0]
    yspan = ax.get_ylim()[1] - ax.get_ylim()[0]

    ax.text(
        p.x + x_offset * xspan,
        p.y + y_offset * yspan,
        text,
        fontsize=fontsize,
        ha=ha,
        va=va,
        bbox=dict(facecolor="white", alpha=0.7, edgecolor="none", pad=0.5),
        zorder=10,
    )
    ax.scatter(p.x, p.y, s=10, color="black", zorder=11)