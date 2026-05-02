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
sys.path.append("../src/heylandcircle/")
import numpy as np
import matplotlib.pyplot as plt

from heylandcircle.data_structures import MachineTestData, CircleResults, Point, Line, Circle
from heylandcircle.geometry import phasor_to_point, slope_from_points, y_intercept, line_circle_intersection, line_line_intersection, distance


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
        pass


    def plot(self, save_path: str | None = None):
        pass