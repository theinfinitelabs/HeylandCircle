# HeylandCircle

[![Tests](https://github.com/abruanspace/HeylandCircle/actions/workflows/ci.yml/badge.svg)](https://github.com/abruanspace/HeylandCircle/actions)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/abruanspace/HeylandCircle/main)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)](https://www.repostatus.org/#active)


[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![GitHub release](https://img.shields.io/github/v/release/abruanspace/HeylandCircle)](https://github.com/abruanspace/HeylandCircle/releases)
[![Docs](https://img.shields.io/badge/docs-latest-blue.svg)](https://abruan-documentation.readthedocs.io/en/develop/#)

[![arXiv](https://img.shields.io/badge/arXiv-2512.20015-b31b1b.svg)](https://arxiv.org/abs/2512.20015)
[![arXiv](https://img.shields.io/badge/arXiv-2512.08302-b31b1b.svg)](https://arxiv.org/abs/2512.08302)
<br></br>

HeylandCircle is a lightweight, modular Python tool for constructing and analyzing the circle diagram of three-phase induction machines, enabling rapid visualization of performance characteristics such as power factor, torque, current, and efficiency.
<br></br>

![Heyland Circle Diagram](docs/source/_images/circle_diagram.png)

## 🔬 Features

- Compute current locus from machine parameters or test data
- Estimate key points (no-load, full-load, max torque)
- Simple plotting utilities

## ⚡ Installation

Clone the repository:

```bash
git clone https://github.com/theinfinitelabs/HeylandCircle.git
cd HeylandCircle
```

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate the environment:

**macOS / Linux**
```bash
source .venv/bin/activate
```

**Windows (PowerShell)**
```powershell
.venv\Scripts\Activate.ps1
```

Install HeylandCircle in editable mode:

```bash
python -m pip install --upgrade pip
python -m pip install -e .
```

Verify the installation:

```bash
pytest
python examples/motor_circle_diagram.py
```

## 🏗️ Structure

```bash
heylandcircle/
  circle_diagram.py
  data_structures.py
  equivalent_circuit.py
  geometry.py
  plot.py
```

## 🧪 Testing

HeylandCircle uses pytest for validation.

Run all tests from the root of the repo using the following command:

```python
pytest
```

Tests cover:

- circle construction consistency
- parameter transformations
- basic analytical checks

## 📚 Citation

If you use HeylandCircle in academic work, please cite:

> Gupta, A., and Gupta, A., "HeylandCircle: A Computational Framework for the Geometric Reconstruction of the Heyland Circle Diagram," arXiv preprint, arXiv:2512.20015, 2025.

```bibtex
@article{gupta2025heylandcircle,
      title={HeylandCircle: A Computational Framework for the Geometric Reconstruction of the Heyland Circle Diagram}, 
      author={Anubhav Gupta and Abhinav Gupta},
      year={2025},
      eprint={2512.20015},
      archivePrefix={arXiv preprint, arXiv},
      primaryClass={eess.SY},
      url={https://arxiv.org/abs/2512.20015},
}
```

## References

1. Heyland, A.; "**[A Graphical Treatment of the Induction Motor](https://archive.org/details/graphicaltreatme00heylrich/page/n3/mode/2up)**," New York, NY: McGraw Publishing Company, 1906
1. Langsdorf, A.; "**[Theory of Alternating Current Machines](https://books.google.com/books?id=zKVd780XHGcC&newbks=0&hl=en&source=newbks_fb)**," New York, NY: McGraw-Hill Book Company, 1937
1. Thereja, B. L.; and Thereja, A.K.; "**[A Textbook of Electrical Technology](https://www.amazon.com/dp/8121924413)**," New Delhi, India: S. Chand Publishing, 2014
1. Fritzgerald, A.; Kingsley Jr., C.; and Umans, S.; "**[Electric Machinery](https://www.amazon.com/Electric-Machinery-Fitzgerald-Kingsley-Umans/dp/0070530394)**," 6th ed., New York, NY: McGraw-Hill, 2002
1. Carpaneto, E.; and Savio, S.; “**A Teaching Tool for the Heyland Circle Diagram using Numerical Simulation**,” IEEE Transactions on Education, vol. 45, no. 3, pp. 263–270, 2002.
1. Gupta, A.; and Gupta, A.; "**[Testing of Transformers and Induction Machines.](https://www.amazon.com/dp/B00A63NBTI)**" 1st ed., Charleston, SC: CreateSpace, 2012
1. Gupta, A.; "**[Möbius Transformations and the Analytic-Geometric Reconstruction of the Induction-Machine Circle Diagram.](https://arxiv.org/abs/2512.08302)**" In arXiv:2512.08302, 2025 [math.DS]
1. Gupta, A.; and Gupta, A.; "**[HeylandCircle: A Computational Framework for the Geometric Reconstruction of the Heyland Circle Diagram.](https://arxiv.org/abs/2512.20015)**" In arXiv:2512.20015, 2025 [eess.SY]
1. Jurkovic, S.; "**Induction Motor Parameters Extraction**", Educypedia-Electronics, 2014