#%%
# ./examples/motor_circle_diagram.py
#
# Sample script to demonstrate the Heyland circle diagram using test data.
#
# Author:       Anubhav Gupta
# Organization: Abruan Aerospace
# License:      MIT
# 

r"""

This example demonstrates the construction and visualization of a Heyland circle diagram using induction-machine test data.

The script defines the no-load and blocked-rotor test conditions, configures the graphical scales and display options, constructs the circle diagram, and reports the principal operating quantities obtained from the geometric construction.

The corresponding example script is located at::

  examples/motor_circle_diagram.py

Overview
--------

The example follows four main steps:

#. Define the induction-machine test data.
#. Configure the graphical representation of the circle diagram.
#. Construct and plot the Heyland circle.
#. Extract and display the calculated operating quantities.

The circle diagram is generated using the
:class:`heylandcircle.circle_diagram.CircleDiagram` class.

Machine Test Data
-----------------

The example uses representative no-load and blocked-rotor test data for an induction machine.

.. code-block:: python

  test_data = MachineTestData(
    I_0=6,
    phi_0_deg=85,
    I_sc=12.0,
    phi_sc_deg=69.0667,
    V_rated=400,
    V_sc=100,
    P_rated_kw=5.6,
    R1_dc=None
    )

The parameters represent:

.. list-table::
   :header-rows: 1
   :widths: 25 20 55

   * - Parameter
     - Value
     - Description

   * - ``I_0``
     - 6 A
     - No-load current.

   * - ``phi_0_deg``
     - 85 deg
     - Phase angle of the no-load current.

   * - ``I_sc``
     - 12 A
     - Blocked-rotor current measured during the short-circuit test.

   * - ``phi_sc_deg``
     - 69.0667 deg
     - Phase angle of the blocked-rotor current.

   * - ``V_rated``
     - 400 V
     - Rated machine voltage.

   * - ``V_sc``
     - 100 V
     - Voltage applied during the blocked-rotor test.

   * - ``P_rated_kw``
     - 5.6 kW
     - Rated output power of the machine.

   * - ``R1_dc``
     - ``None``
     - Optional measured stator resistance. In this example, no explicit value is supplied.

Circle Diagram Configuration
------------------------------

The graphical construction is controlled through
:class:`heylandcircle.data_structures.CircleDiagramConfig`.

.. code-block:: python

  config = CircleDiagramConfig(
    power_scale=1.4,
    current_scale=1 / 2,
    show_eff_scale=True,
    show_slip_scale=True,
    show_pf_curve=True,
    show_full_circle=False,
    show_grid=True
    )

The configuration used in this example enables the efficiency, slip, and power-factor scales while displaying only the portion of the circle relevant to normal machine operation.

The current scale is specified as

.. math::

  S_I = \frac{1}{2},

such that one unit of geometric length corresponds to

.. math::

  \frac{1}{S_I} = 2~\mathrm{A}.

Similarly, the power scale establishes the conversion between geometric distances on the diagram and machine power.

Constructing the Circle Diagram
--------------------------------

The circle diagram is constructed by passing the configuration and machine test data to
:class:`heylandcircle.circle_diagram.CircleDiagram`.

.. code-block:: python

  cd = CircleDiagram(config, test_data)

  fig, ax = cd.plot()
  plt.show()

The :meth:`heylandcircle.circle_diagram.CircleDiagram.plot` method performs the geometric construction and returns the Matplotlib figure and axes objects.

The resulting plot contains the Heyland circle together with the enabled graphical scales and characteristic operating points.

Calculated Results
------------------

After the circle has been constructed, the calculated operating quantities are available through

.. code-block:: python

  r = cd.results

The example reports the following quantities:

* input power,
* total loss,
* copper loss,
* rotor copper loss,
* fixed loss,
* maximum output,
* maximum torque,
* efficiency,
* slip,
* line current, and
* power factor.

For several quantities, HeylandCircle retains both the geometric value measured from the circle construction and the corresponding calibrated engineering value.

For example,

.. code-block:: python

  r.power_input
  r.power_input_kW

represent the geometric input-power quantity and its calibrated value in kilowatts, respectively.

Running the Example
-------------------

From the root directory of the HeylandCircle repository, activate the project environment and run:

.. code-block:: bash

  python examples/motor_circle_diagram.py

The generated circle diagram is displayed using Matplotlib. After the plotting window is closed, a summary table is printed to the terminal.

A typical table has the form:

.. code-block:: text

  ======================== RESULTS SUMMARY ========================
  Parameter              Geometric Value      Calibrated Value
  ------------------------------------------------------------

  Input Power            ...
  Total Loss             ...
  Copper Loss            ...
  Rotor Cu Loss          ...
  Fixed Loss             ...
  Max Output             ...
  Max Torque             ...
  Efficiency             ...
  Slip (power-based)     ...
  Line Current           ...
  Power Factor           ...
  ==========================

Complete Example
-----------------

The complete source code is reproduced below.

.. literalinclude:: ../../../examples/motor_circle_diagram.py
:language: python
:linenos:
:caption: motor_circle_diagram.py
"""

import matplotlib.pyplot as plt

from heylandcircle.circle_diagram import CircleDiagram
from heylandcircle.data_structures import CircleDiagramConfig, MachineTestData

def main():
    # Sample test data for a 10 kW induction machine
    test_data = MachineTestData(
        I_0=6,               # No-load current [A]
        phi_0_deg=85,        # No-load current angle [deg]
        I_sc=12.0,           # Blocked-rotor current [A]
        phi_sc_deg=69.0667,  # Blocked-rotor current angle [deg]
        V_rated=400,         # Rated voltage [V]
        V_sc=100,            # Blocked-rotor test voltage [V]
        P_rated_kw=5.6,      # Rated power [kW]
        R1_dc=None           # Stator resistance at operating temperature [Ω]
    )

    # Circle diagram configuration
    config = CircleDiagramConfig(
        power_scale=1.4,           # x kW/cm
        current_scale=1 / 2,       # 1/x implies 1 cm = x Amps
        show_eff_scale=True,       # whether to show slip scale on diagram
        show_slip_scale=True,      # whether to show slip scale on diagram
        show_pf_curve=True,        # whether to show power factor curve scale on diagram
        show_full_circle=False,    # whether to show full circle on diagram
        show_grid=True             # whether to show grid lines on diagram
    )

    cd = CircleDiagram(config, test_data)
    fig, ax = cd.plot()
    plt.show()
    
    # Build 3-column results table
    r = cd.results
    rows = [
        ["Input Power",         f"{r.power_input:.2f}",        f"{r.power_input_kW:.2f} kW"       if r.power_input_kW else "-"],
        ["Total Loss",          f"{r.total_loss:.2f}",         f"{r.total_loss_kW:.2f} kW"        if r.total_loss_kW else "-"],
        ["Copper Loss",         f"{r.copper_loss:.2f}",        f"{r.copper_loss_kW:.2f} kW"       if r.copper_loss_kW else "-"],
        ["Rotor Cu Loss",       f"{r.rotor_copper_loss:.2f}",  f"{r.rotor_copper_loss_kW:.2f} kW" if r.rotor_copper_loss_kW else "-"],
        ["Fixed Loss",          f"{r.fixed_loss:.2f}",         f"{r.fixed_loss_kW:.2f} kW"        if r.fixed_loss_kW else "-"],
        ["Max Output",          f"{r.max_output:.2f}",         f"{r.max_output_kW:.2f} kW"        if r.max_output_kW else "-"],
        ["Max Torque",          f"{r.max_torque:.2f}",         f"{r.max_torque_kW:.2f} Sync kW"        if r.max_output_kW else "-"],
        ["Efficiency",          f"{r.efficiency/100:.2f}",     f"{r.efficiency:.2f} %"],
        ["Slip (power-based)",  f"{r.slip/100:.2f}",           f"{r.slip:.2f} %"],
        ["Line Current",        f"{r.line_current:.2f}",       f"{r.line_current/config.current_scale:.2f} A"],
        ["Power Factor",        f"{r.power_factor:.2f}",       "-"],
    ]

    # Print the table to console
    print("======================== RESULTS SUMMARY ========================")
    print(f"{'Parameter':<22} {'Geometric Value':<20} {'Calibrated Value':<20}")
    print("-" * 65)

    for param, geom, calib in rows:
        print(f"{param:<22} {geom:<20} {calib:<20}")

    print("=" * 65)
    
if __name__ == "__main__":
    main()