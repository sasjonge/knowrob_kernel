echo_kernel
===========

``knowrob_kernel`` is a Jupyter kernel for using KnowRob, providing magic commands for querying and loading settings. 

Installation
------------

From PyPI
~~~~~~~~~

To install ``echo_kernel`` from PyPI::

    pip install echo_kernel
    
From Git using Conda
~~~~~~~~~~~~~~~~~~~~

To install ``echo_kernel`` from git into a Conda environment::

    git clone https://github.com/jupyter/echo_kernel
    cd echo_kernel
    conda create -n ker jupyter
    conda activate ker
    pip install .


Using the Echo kernel
---------------------
**Notebook**: The *New* menu in the notebook should show an option for an Echo notebook.

**Console frontends**: To use it with the console frontends, add ``--kernel echo`` to
their command line arguments.
