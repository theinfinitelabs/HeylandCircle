# ---------------------------------------------------------------------
# src/heylandcircle/data_structures.py
#
# Data containers for HeylandCircle.
# Defines dataclasses for machine test inputs, geometric primitives,
# and computed performance results used throughout the package.
#
# Author:       Anubhav Gupta
# Affiliation:  University of Colorado Boulder
#               In Orbit Aerospace
# Organization: Infinite Labs
# License:      MIT
# ---------------------------------------------------------------------


from dataclasses import dataclass, field


@dataclass
class CircleDiagramConfig:
    """Configuration options for the Circle Diagram."""
    power_scale: float          # x kW/cm
    current_scale: float        # 1/x implies 1 cm = x Amps
    show_eff_scale: bool        # whether to show slip scale on diagram
    show_slip_scale: bool       # whether to show slip scale on diagram
    show_pf_curve: bool         # whether to show power factor curve scale on diagram
    show_full_circle: bool      # whether to show half-circle or full circle diagram
    show_grid: bool             # whether to show grid lines on diagram


@dataclass
class MachineTestData:
    """Raw test data for the induction machine."""
    I0: float           # No-load current magnitude [A]
    phi0_deg: float     # No-load current angle from vertical (clockwise) [deg]
    Isc: float          # Blocked-rotor current magnitude [A] at V_SC
    phi_sc_deg: float   # Blocked-rotor current angle from vertical (clockwise) [deg]
    V_rated: float      # Rated line-to-line voltage [V]
    V_sc: float         # Blocked-rotor test voltage [V]
    P_rated_kw: float   # Rated power [kW]

    @property
    def I_start(self) -> float:
        """Starting current at rated voltage (scaled from blocked-rotor test)."""
        return self.Isc * (self.V_rated / self.V_sc)


@dataclass
class Point:
    x: float
    y: float


@dataclass
class Circle:
    center: Point
    r: float

@dataclass
class Line:
    """Represents a line in one of three forms (set exactly one group):
        - Normal:     m and c   →  y = mx + c
        - Vertical:   x_vert   →  x = const
        - Horizontal: y_horz   →  y = const
    """
    m:      float | None = None
    c:      float | None = None
    x_vert: float | None = None
    y_horz: float | None = None
    
    def __post_init__(self):
        normal = (self.m is not None) or (self.c is not None)
        vertical = self.x_vert is not None
        horizontal = self.y_horz is not None

        forms_selected = sum([normal, vertical, horizontal])

        if forms_selected != 1:
            raise ValueError(
                "Line must define exactly one form: "
                "(m,c), x_vert, or y_horz."
            )

        # Require BOTH m and c for normal form
        if normal and (self.m is None or self.c is None):
            raise ValueError(
                "Normal line form requires both m and c."
            )
        
@dataclass
class CircleResults:
    # Geometric units
    total_loss: float = 0.0
    copper_loss: float = 0.0
    rotor_copper_loss: float = 0.0
    fixed_loss: float = 0.0
    max_torque: float = 0.0
    max_output: float = 0.0

    # Power input (geom)
    power_input: float = 0.0

    # Line current at operating point
    line_current: float = 0.0
    
    # SI units (optional)
    total_loss_kW: float | None = None
    copper_loss_kW: float | None = None
    rotor_copper_loss_kW: float | None = None
    fixed_loss_kW: float | None = None
    max_output_kW: float | None = None
    power_input_kW: float | None = None

    # Dimensionless
    efficiency: float = 0.0
    power_factor: float = 0.0
    slip: float = 0.0
    slip_geom: float = 0.0