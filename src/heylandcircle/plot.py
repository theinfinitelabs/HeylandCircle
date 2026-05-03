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