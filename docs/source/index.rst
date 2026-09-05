.. HeylandCircle documentation master file.

HeylandCircle
=============

HeylandCircle is a lightweight, modular Python package for constructing
and analyzing the Heyland circle diagram of three-phase induction
machines. It translates the classical graphical method into a
reproducible computational workflow connecting machine test data,
geometric construction, and performance analysis.

.. sidebar:: HeylandCircle Info

   .. image:: _static/heylandcircle_logo.svg
      :alt: HeylandCircle logo
      :align: center
      :width: 170px

   .. rubric:: HeylandCircle

   :Purpose:
      Computational construction and analysis of the Heyland circle
      diagram.

   :License:
      MIT License

   :Language:
      Python 3.10+

   :Platforms:
      macOS, Linux, and Windows

   :Initial release:
      May 2026

   :Status:
      Active development

   :Source:
      `GitHub repository
      <https://github.com/abruanspace/HeylandCircle>`_

   .. rubric:: Logo design

   The open circular locus forms a stylized **C** while representing
   the stator-current locus of an induction machine. The two colored
   phasors signify the no-load and blocked-rotor test measurements,
   and the central point represents the deterministic geometric
   construction underlying the framework.

The Heyland circle diagram represents the locus of the stator-current
phasor as the operating condition of an induction machine changes.
Within the assumptions of the underlying equivalent-circuit model,
the diagram reveals relationships among current, power factor, torque,
output power, slip, and efficiency.

HeylandCircle makes this construction reproducible and accessible
through Python. Users can generate circle diagrams, inspect
characteristic operating points, and incorporate the analysis into
scripts, notebooks, automated tests, and teaching examples.


Capabilities
------------

HeylandCircle provides tools to:

* Construct the current locus from no-load and blocked-rotor test data.
* Reproduce the geometric elements of the classical Heyland diagram.
* Estimate characteristic operating quantities, including power
  factor, slip, torque, output power, and efficiency.
* Visualize annotated circle diagrams using reusable plotting tools.
* Integrate circle-diagram analysis into Python scripts and notebooks.
* Inspect and test the electrical, geometric, and plotting operations
  independently.

The package separates machine test data, electrical calculations,
geometric construction, performance analysis, and plotting so that
individual components can be inspected, validated, and extended
independently.


Intended use
------------

HeylandCircle is intended for students, educators, engineers, and
researchers interested in induction-machine analysis and the
relationship between equivalent-circuit models and classical graphical
methods.

The framework supports:

* Classroom demonstrations of induction-machine behavior.
* Reproducible computational examples.
* Verification of hand-constructed circle diagrams.
* Parameter studies based on measured machine-test data.
* Exploration of extensions to the classical circular current locus.

The resulting diagrams and performance estimates should be interpreted
within the assumptions of the selected machine model and the quality of
the supplied test data.


References
----------

#. Gupta, A., “`Möbius Transformations and the Analytic-Geometric
   Reconstruction of the Induction-Machine Circle Diagram
   <https://arxiv.org/abs/2512.08302>`_,”
   arXiv:2512.08302 [math.DS], 2025.

#. Gupta, A., and Gupta, A., “`HeylandCircle: A Computational Framework
   for the Geometric Reconstruction of the Heyland Circle Diagram
   <https://arxiv.org/abs/2512.20015>`_,”
   arXiv:2512.20015 [eess.SY], 2025.

#. Gupta, A., and Gupta, A.,
   `Testing of Transformers and Induction Machines
   <https://www.amazon.com/dp/B00A63NBTI>`_,
   1st ed., CreateSpace, Charleston, South Carolina, 2012.


.. toctree::
   :hidden:
   :maxdepth: 2
   :caption: HeylandCircle

   rst/install
   rst/examples