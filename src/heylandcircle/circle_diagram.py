# ---------------------------------------------------------------------
# src/heylandcircle/circle_diagram.py
#
# Core engine for the Heyland circle diagram construction and analysis.
# Encapsulates geometry building, performance computation, and plotting
# for induction machines using classical circle diagram methods.
#
# Author:       Anubhav Gupta
# Affiliation:  University of Colorado Boulder
#               In Orbit Aerospace
# Organization: Infinite Labs
# License:      MIT
# ---------------------------------------------------------------------

from __future__ import annotations
import sys
sys.path.append("../src/heylandcircle/")                # TODO: Should be handled through pyproject.toml or setup.py
import numpy as np
import matplotlib.pyplot as plt

from heylandcircle.data_structures import MachineTestData, CircleResults, Point, Line, Circle
from heylandcircle.geometry import phasor_to_point, slope_from_points, y_intercept, line_circle_intersection, line_line_intersection, distance
from heylandcircle.plot import plot_phasor, draw_arc, annotate_point


COLORS = {
    "accent": "#1f4e79",      # deep elegant blue
    "max_output": "#222222",  # black
    "max_torque": "#8b0000",  # dark muted red
    "mono": "#444444",        # main gray
    "light": "#aaaaaa",       # auxiliary construction
}


class CircleDiagram:
    """Encapsulates geometry, analysis, and plotting of the Heyland circle."""

    def __init__(self, config: CircleDiagramConfig, data: MachineTestData):
        self.config = config
        self.data = data
        self.results: CircleResults = CircleResults()
        self.circle: Circle | None = None

    def _build_geometry(self):
        """Compute all geometric points needed for the classical construction."""
        
        # ------------------------------------------------
        # Phase 1: Get Output line and circle center 
        # ------------------------------------------------
        # Scale the currents
        self.data.I0 *= self.config.current_scale
        self.data.Isc *= self.config.current_scale
        
        # Compute endpoints of the no-load (point O') and starting-current (point A) phasors
        self.p0 = phasor_to_point(self.data.I0, self.data.phi0_deg)
        self.psn = phasor_to_point(self.data.I_start, self.data.phi_sc_deg)
        
        # Compute slope and y-intercept of the Output line (between O' and A)
        self.m_output = slope_from_points(self.p0, self.psn)
        self.c_output = y_intercept(self.p0.x, self.p0.y, self.m_output)

        # Compute midpoint (C') of the Output line (O'A) for the perpendicular bisector construction
        self.pCprime = Point( x=(self.p0.x + self.psn.x) / 2.0,
                              y=(self.p0.y + self.psn.y) / 2.0 )
        # Compute slope of the perpendicular bisector of Output line passing through C'
        self.m_perp = -1.0 / self.m_output

        # Compute intersection point of the Output line bisector with x-axis (y=0) and O'B line (y = p0.y)
        self.x_at_xaxis = self.pCprime.x - self.pCprime.y / self.m_perp
        self.x_at_OB = self.pCprime.x + (self.p0.y - self.pCprime.y) / self.m_perp

        # Determine main circle center and radius
        r = self.x_at_OB - self.p0.x
        self.circle = Circle(center=Point(self.x_at_OB, self.p0.y), r=r)

        # ------------------------------------------------
        # Phase 2: Locate load point P on the circle
        # and auxiliary points E, Q, Q', R'
        # ------------------------------------------------
        # Assuming equal losses, determine the midpoint E of total loss (AF)
        self.pE = Point( self.psn.x, (self.p0.y + self.psn.y) / 2.0)
        
        # Locate point P on the circle: intersection of line parallel to output line through A with circle
        c1 = self.c_output + self.pCprime.y
        self.pP = line_circle_intersection(Line(m=self.m_output, c=c1), self.circle)

        # Locate point Q: vertical through P intersects output line
        self.pQprime = line_line_intersection( Line(m=self.m_output, c=self.c_output), Line(x_vert=self.pP.x) )
        
        # Locate point R: vertical through P intersects torque line
        self.m_torque = slope_from_points(self.p0, self.pE)
        self.c_torque = y_intercept(self.p0.x, self.p0.y, self.m_torque)
        self.pRprime = line_line_intersection( Line(m=self.m_torque, c=self.c_torque), Line(x_vert=self.pP.x) )
        
        # ------------------------------------------------
        # Phase 3: Determine max output point M_O and 
        # max torque point M_T using classical constructions
        # ------------------------------------------------
        # Determine point of maximum output M_O: intersection of perpendicular bisector of Output line with circle
        c_perp = self.pCprime.y - self.m_perp * self.pCprime.x
        self.pM_O = line_circle_intersection(Line(m=self.m_perp, c=c_perp), self.circle)
        
        # Determine point N_O: projection of M_O onto Output line
        self.pN_O = line_line_intersection( Line(m=self.m_output, c=self.c_output), Line(x_vert=self.pM_O.x) )
        
        # Determine point of maximum torque M_T: intersection of perpendicular (NOT bisector) of Torque line (O'E) with circle
        # Perpendicular to the torque line passing through the circle center C
        m_perp_torque = -1.0 / self.m_torque
        c_perp_center = self.circle.center.y - m_perp_torque * self.circle.center.x
        self.pM_T = line_circle_intersection( Line(m=m_perp_torque, c=c_perp_center), self.circle )
        
        # Determine point N_T: projection of M_T onto Torque line
        self.pN_T = line_line_intersection( Line(m=self.m_torque, c=self.c_torque), Line(x_vert=self.pM_T.x) )
        
        # ------------------------------------------------
        # Phase 4: Determine points for efficiency and 
        # slip scales
        # ------------------------------------------------
        # Locate point T' on x-axis: intersection of Output line with x-axis (y=0)
        self.pTprime = line_line_intersection( Line(m=self.m_output, c=self.c_output), Line(y_horz=0.0) )
        
        # Determine point T: vertical extension from point T'
        # The length TT' is set to the radius of the circle plus no-load current y-coordinate (O'B line) to give a meaningful efficiency scale
        self.y_T = self.circle.r + self.p0.y
        self.pT = Point(self.pTprime.x, self.y_T)

        # Compute point Q: extend Output line until it meets the horizontal through T parallel to x-axis(y = y_T)
        self.pQ = line_line_intersection(
            Line(m=self.m_output, c=self.c_output),     # Output line
            Line(y_horz=self.y_T)                # Vertical through T
        )

        # Compute efficiency for load point P: line from origin (O), passing through point P, to Efficiency scale intersecting at point T_eff
        m_OP = slope_from_points(Point(0, 0), self.pP)
        c_OP = y_intercept(self.pP.x, self.pP.y, m_OP)
        self.pTeff = line_line_intersection( Line(m=m_OP, c=c_OP), Line(y_horz=self.y_T) )

        # Slip Scale: line from point Q, parallel to Torque line, intersecting vertical extension from point T' at point X.
        m_QX = self.m_torque
        c_QX = self.pQ.y - m_QX * self.pQ.x
        self.pX = line_line_intersection( Line(m=m_QX, c=c_QX), Line(x_vert=self.p0.x) )

        # Compute slip point X_slip: intersection of O'P with QX
        m_O2P = slope_from_points(self.p0, self.pP)
        c_O2P = y_intercept(self.pP.x, self.pP.y, m_O2P)
        self.pXslip = line_line_intersection( Line(m=m_O2P, c=c_O2P), Line(m=m_QX, c=c_QX) )

        # Point X': projection of X_slip onto the QT base line (y = y_T)
        self.pXprime = line_line_intersection(
            Line(y_horz=self.y_T),        # Horizontal QT
            Line(x_vert=self.pXslip.x)    # Vertical through X_slip
        )

    def _compute_results(self):
        """Populate CircleResults from the geometry."""
        
        self.results.total_loss = self.psn.y                            # Vertical distance from A to x-axis
        self.results.copper_loss = self.psn.y - self.p0.y               # Vertical distance from A to O'B line (y = p0.y)
        self.results.rotor_copper_loss = self.psn.y - self.pE.y         # Vertical distance from A to E (half of total loss)
        self.results.fixed_loss = self.p0.y                             # Vertical distance from F to x-axis
        self.results.max_output = self.pM_O.y - self.pN_O.y             # Vertical distance from M_O to N_O
        self.results.power_input = self.psn.y                           # Vertical distance from A to x-axis (same as total loss + max output)
        self.results.max_torque = self.pM_T.y - self.pN_T.y             # Vertical distance from M_T to N_T
        
        # Efficiency: horizontal distance from T to Q divided by horizontal distance from T_eff to Q
        QT     = self.pT.x - self.pQ.x
        QT_eff = self.pTeff.x - self.pQ.x
        self.results.efficiency = ( (self.pP.y - self.pQprime.y) / self.pP.y ) * 100
        
        # Power factor: angle of load current phasor P with respect to horizontal axis (real axis)
        I_mag = np.hypot(self.pP.x, self.pP.y)
        self.results.power_factor = self.pP.y / I_mag
        self.results.line_current = np.linalg.norm([self.pP.x, self.pP.y])
        
        # Slip: ratio of vertical distance from Q' to R' (slip component) to vertical distance from P to R' (total current component)
        self.results.slip = (self.pQprime.y - self.pRprime.y) / (self.pP.y - self.pRprime.y) * 100
        
        # Geometric Slip: from QT using X_slip projection
        QT = self.pT.x - self.pQ.x                      # Full slip scale length
        TXprime = self.pT.x - self.pXprime.x            # Position of S on QT
        s_geom = (TXprime) / QT
        self.results.slip_geom = s_geom * 100

        # ==========================
        # Apply scaling if provided
        # ==========================
        if self.config.power_scale is not None:
            self.results.total_loss_kW = self.results.total_loss * self.config.power_scale
            self.results.copper_loss_kW = self.results.copper_loss * self.config.power_scale
            self.results.rotor_copper_loss_kW = self.results.rotor_copper_loss * self.config.power_scale
            self.results.fixed_loss_kW = self.results.fixed_loss * self.config.power_scale
            self.results.max_output_kW = self.results.max_output * self.config.power_scale
            self.results.power_input_kW = self.results.power_input * self.config.power_scale
            self.results.max_torque_kW = self.results.max_torque * self.config.power_scale
        else:
            # Scaling disabled → keep None
            self.results.total_loss_kW = None
            self.results.copper_loss_kW = None
            self.results.rotor_copper_loss_kW = None
            self.results.fixed_loss_kW = None
            self.results.max_output_kW = None
            self.results.power_input_kW = None


    def plot(self, save_path: str | None = None):
        """Build geometry, compute results, and generate the circle diagram plot."""
        self._build_geometry()
        self._compute_results()

        plt.rcParams["figure.dpi"] = 200
        plt.rcParams["font.family"] = "DejaVu Sans"  # or 'Times New Roman' for IEEE
        plt.rcParams["mathtext.fontset"] = "cm"       # LaTeX-like math

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.set_aspect("equal", "box")
        ax.set_xlabel("Reactive Current (A)")
        ax.set_ylabel("Active Current (A)")
        for spine in ax.spines.values():
            spine.set_visible(False)

        if not self.config.show_full_circle:
            xmin = 0
            xmax = max(self.pT.x, self.psn.x, self.pQ.x) * 1.1
            ymin = 0
            ymax = max(self.pT.y, self.pM_O.y) * 1.25

            ax.set_xlim(xmin, xmax)
            ax.set_ylim(ymin, ymax)
        
        ax.axhline(0, color="#222222", linewidth=1.5)
        ax.axvline(0, color="#222222", linewidth=1.5)

        # Phasors
        plot_phasor(ax, self.p0, label="$I_0$", color=COLORS["mono"])
        plot_phasor(ax, self.psn, label="$I_{SN}$", color=COLORS["mono"])

        # Horizontal line from O'
        xmax = ax.get_xlim()[1]
        ax.hlines(y=self.p0.y, xmin=self.p0.x, xmax=xmax*1.1,
                  colors=COLORS["light"], linestyles="--", linewidth=1)

        # Output line
        ax.plot([self.p0.x, self.psn.x], [self.p0.y, self.psn.y],
                color=COLORS["mono"], linestyle="--", linewidth=1.6, label="Output Line")

        # Main circle
        if self.config.show_full_circle:
            theta = np.linspace(0, 2 * np.pi, 600)
        else:
            theta = np.linspace(0, np.pi, 600)
        self.x_circle = self.circle.center.x + self.circle.r * np.cos(theta)
        self.y_circle = self.circle.center.y + self.circle.r * np.sin(theta)
        ax.plot(self.x_circle, self.y_circle, color=COLORS["accent"], linewidth=2.0)

        # Vertical from A
        ax.plot([self.psn.x, self.psn.x], [self.psn.y, 0],
                color=COLORS["light"], linestyle="--", linewidth=1)

        # Torque line
        ax.plot([self.p0.x, self.psn.x], [self.p0.y, self.pE.y],
                color=COLORS["mono"], linestyle="-.", linewidth=1.6, label="Torque Chord")

        # Vertical through A
        ax.plot([self.psn.x, self.psn.x],
                [self.psn.y, self.psn.y + self.pE.y],
                color=COLORS["light"], linestyle="--", linewidth=1)

        # Line from A parallel to output -> P
        ax.plot([self.psn.x, self.pP.x],
                [self.psn.y + self.pE.y, self.pP.y],
                color=COLORS["light"], linestyle="--", linewidth=1)

        # Vertical through P
        ax.plot([self.pP.x, self.pP.x],
                [self.pP.y, 0],
                color=COLORS["light"], linestyle="--", linewidth=1)
        
        # Perpendicular bisector to C' and circle
        ax.plot([self.pCprime.x, self.circle.center.x], [self.pCprime.y, self.circle.center.y],
                color=COLORS["light"], linestyle="--", linewidth=1)
        ax.plot([self.pCprime.x, self.pM_O.x], [self.pCprime.y, self.pM_O.y],
                color=COLORS["light"], linestyle="--", linewidth=1)
        
        # Line from M_O down to N_O (max output)
        ax.plot([self.pM_O.x, self.pM_O.x],
                [self.pM_O.y, self.pN_O.y],
                color=COLORS["max_output"], linewidth=1, label="Max Output")

        # Perpendicular to torque line and circle
        ax.plot([self.pM_T.x, self.circle.center.x], [self.pM_T.y, self.circle.center.y],
                color=COLORS["light"], linestyle="--", linewidth=1)

        # Line from M_T down to N_T (max torque)
        ax.plot([self.pM_T.x, self.pM_T.x],
                [self.pM_T.y, self.pN_T.y],
                color=COLORS["max_torque"], linestyle=":", linewidth=2.0, label="Max Torque")

        if self.config.show_eff_scale:
            # Output line extended to meet x-axis at point T'
            ax.plot([self.p0.x, self.pTprime.x],
                    [self.p0.y, self.pTprime.y],
                    color=COLORS["light"], linestyle="--", linewidth=1)

            # Vertical from T' to T, parallel to y-axis
            ax.plot([self.pT.x, self.pT.x], [0, self.pT.y],
                    color=COLORS["light"], linestyle="--", linewidth=1)

            # Extend the output line to Q
            ax.plot([self.psn.x, self.pQ.x],
                    [self.psn.y, self.pQ.y],
                    color="k", linewidth=1)

            # Efficiency line QT parallel to x-axis
            ax.plot([self.pQ.x, self.pTprime.x],
                    [self.pQ.y, self.pQ.y],
                    color=COLORS["mono"], linestyle="dashdot", linewidth=1.2, label="Efficiency Line")

            # Line OP intersecting QT at T_eff
            ax.plot([0, self.pP.x], [0, self.pP.y],
                    color=COLORS["light"], linestyle="--", linewidth=1)
            ax.plot([self.pP.x, self.pTeff.x],
                    [self.pP.y, self.pTeff.y],
                    color=COLORS["light"], linestyle="--", linewidth=1)

        if self.config.show_slip_scale:
            # O'X parallel to y-axis
            ax.plot([self.p0.x, self.p0.x], [0, self.pX.y],
                    color="gray", linestyle="--", linewidth=1)

            # Slip line QX and X_slip
            ax.plot(
                [self.pQ.x, self.pX.x],
                [self.pQ.y, self.pX.y],
                color="tab:green",
                linestyle="-",
                linewidth=1.2,
                label="Slip Calibration Line (QR)"
            )

            ax.plot([self.p0.x, self.pXslip.x],
                    [self.p0.y, self.pXslip.y],
                    color="gray", linestyle="--", linewidth=1)
            ax.plot([self.pXprime.x, self.pXslip.x],
                    [self.pXprime.y, self.pXslip.y],
                    color="gray", linestyle="--", linewidth=1)

        # Power factor arc
        if self.config.show_pf_curve:
            draw_arc(ax, center=Point(0, 0), radius=self.pT.y * 0.9,
                    start_angle_deg=40, end_angle_deg=90,
                    color="tab:purple", linestyle="--",
                    label="Power Factor curve")

        annotate_point(ax, Point(0,0), "O")
        annotate_point(ax, self.p0, "O'")
        annotate_point(ax, self.psn, "A")
        # annotate_point(ax, Point(self.psn.x, 0), "B")
        annotate_point(ax, self.pCprime, "C'")
        annotate_point(ax, Point(self.circle.center.x, self.circle.center.y), "C")
        annotate_point(ax, Point(self.x_circle[0], self.y_circle[0]), "D")
        annotate_point(ax, self.pE, "E")
        annotate_point(ax, Point(self.psn.x, self.p0.y), "F")
        annotate_point(ax, Point(self.psn.x, self.psn.y + self.pE.y), "S")
        annotate_point(ax, self.pP, "P")
        annotate_point(ax, self.pQprime, "Q'")
        annotate_point(ax, self.pRprime, "R'", x_offset=-0.05, y_offset=0.3)
        annotate_point(ax, self.pM_O, r"M$_O$", x_offset=-0.03, y_offset=0.03)
        annotate_point(ax, self.pN_O, r"N$_O$", x_offset=-0.03, y_offset=0.03)
        annotate_point(ax, self.pM_T, r"M$_T$", x_offset=0.03, y_offset=0.03)
        annotate_point(ax, self.pN_T, r"N$_T$", x_offset=0.03, y_offset=0.03)
        if self.config.show_eff_scale:
            annotate_point(ax, self.pTprime, "T'")
            annotate_point(ax, self.pT, "T")
            annotate_point(ax, self.pQ, "Q")
            annotate_point(ax, self.pTeff, "T_eff")
        if self.config.show_slip_scale:
            annotate_point(ax, self.pX, "X")
            annotate_point(ax, self.pXslip, "X_slip")
            annotate_point(ax, self.pXprime, "X'")
            
        ax.legend(ncols=3, loc="upper center",
                  bbox_to_anchor=(0.5, -0.1), frameon=False)
        plt.tight_layout()

        if save_path:
            fig.savefig(save_path, dpi=300, bbox_inches="tight")

        return fig, ax