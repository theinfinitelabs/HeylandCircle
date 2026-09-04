.. HeylandCircle documentation master file, created by
   sphinx-quickstart on Fri Aug  7 00:49:21 2026.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

HeylandCircle
=============

HeylandCircle is a lightweight, modular Python package for constructing
and analyzing the Heyland circle diagram of three-phase induction
machines. It brings the classical graphical method into a programmable
workflow, connecting machine parameters and test data with geometric
construction and performance visualization.

The Heyland circle diagram represents the locus of the stator-current
phasor as the operating condition of an induction machine changes.
Within the assumptions of the underlying equivalent-circuit model,
this geometric representation provides insight into relationships
among current, power factor, torque, and efficiency.

HeylandCircle makes this construction reproducible and accessible
through Python. Users can generate circle diagrams, inspect
characteristic operating points, and incorporate the analysis into
scripts, notebooks, and teaching examples.

Capabilities
------------

HeylandCircle provides tools to:

* Construct the current locus from machine parameters or test data.
* Estimate characteristic operating points, including no-load,
  full-load, and maximum-torque conditions.
* Visualize the circle diagram using reusable plotting utilities.
* Work with equivalent-circuit calculations, parameter transformations,
  and geometric constructions through separate modules.

The package separates machine data, electrical calculations, geometry,
and plotting so that individual components can be inspected, tested,
and extended independently.

Intended use
------------

HeylandCircle is intended for students, educators, and researchers
interested in induction-machine analysis and the connection between
equivalent-circuit models and graphical methods. It supports classroom
demonstrations, reproducible computational examples, and exploration
of machine performance through the circle diagram.

The resulting diagrams and performance estimates should be interpreted
in the context of the selected machine model and the quality of its
input parameters or test data.


.. toctree::
   :hidden:
   :maxdepth: 2
   :caption: HeylandCircle:

   rst/install
   rst/examples

