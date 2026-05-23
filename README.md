# HeylandCircle
HeylandCircle is a lightweight, modular Python tool for constructing and analyzing the circle diagram of three-phase induction machines, enabling rapid visualization of performance characteristics such as power factor, torque, current, and efficiency.

[![Tests](https://github.com/theinfinitelabs/HeylandCircle/actions/workflows/ci.yml/badge.svg)](https://github.com/theinfinitelabs/HeylandCircle/actions)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/theinfinitelabs/HeylandCircle/main)

![Heyland Circle Diagram](docs/images/circle_diagram.png)

## 🔬 Features
- Compute current locus from machine parameters or test data
- Estimate key points (no-load, full-load, max torque)
- Simple plotting utilities

## ⚡ Quick Start
```
pip install -e .
pytest
python examples/motor_circle_diagram.py
```

## 🏗️ Structure
```
heylandcircle/
  circle_diagram.py/
  data_structures.py/
  geometry.py/
  plot.py/
  tests/
```

## 🧪 Testing
HeylandCircle uses pytest for validation.

Run all tests:
```
pytest
```
Tests cover:
- circle construction consistency
- parameter transformations
- basic analytical checks

## 🔄 Status
In development

## 📜 License
MIT

## References (Select)
1. Heyland. A.; "**A Graphical Treatment of the Induction Motor.**" New York, NY: McGraw Publishing Company, 1906
1. Langsdorf. A.; "**Theory of Alternating Current Machines.**" New York, NY: McGraw-Hill Book Company, 1937
1. Gupta, A.; and Gupta, A.; "**Testing of Transformers and Induction Machines.**" Charleston, SC: CreateSpace, 2012
1. Gupta, A.; "**Möbius Transformations and the Analytic-Geometric Reconstruction of the Induction-Machine Circle Diagram.**" In arXiv:2512.08302, 2025 [math.DS]
1. Gupta, A.; and Gupta, A.; "**HeylandCircle: A Computational Framework for the Geometric Reconstruction of the Heyland Circle Diagram.**" In arXiv:2512.20015, 2025 [eess.SY]