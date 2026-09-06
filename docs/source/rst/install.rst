Installation
============

HeylandCircle requires Python 3.10 or newer and Git.

Clone the repository
--------------------

Clone HeylandCircle and navigate to the project directory:

.. code-block:: bash

   git clone https://github.com/abruanspace/HeylandCircle.git
   cd HeylandCircle

Create a virtual environment
----------------------------

Create a virtual environment to isolate the project's dependencies:

.. code-block:: bash

   python3 -m venv .venv

On Windows, use ``python`` instead of ``python3`` if needed.

Activate the environment using the command for your operating system.

**macOS / Linux**

.. code-block:: bash

   source .venv/bin/activate

**Windows (PowerShell)**

.. code-block:: powershell

   .venv\Scripts\Activate.ps1

Install the package
-------------------

Upgrade pip and install HeylandCircle in editable mode from the
repository root:

.. code-block:: bash

   python -m pip install --upgrade pip
   python -m pip install -e .

Editable mode makes changes to the package source available without
reinstalling it.

Verify the installation
-----------------------

Run the example script from the repository root:

.. code-block:: bash

   python examples/motor_circle_diagram.py

Run the tests
-------------

Install pytest if it is not already available, then run the test suite:

.. code-block:: bash

   python -m pip install pytest
   python -m pytest

Deactivate the environment
--------------------------

When you have finished, deactivate the virtual environment:

.. code-block:: bash

   deactivate