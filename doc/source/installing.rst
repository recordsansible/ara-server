.. _installing:

Installing ara-server
=====================

``ara-server`` requires python 3 to run.

It is recommended to use a python `virtual environment <https://docs.python.org/3/tutorial/venv.html>`_
in order to avoid conflicts with your Linux distribution python packages::

    # Create virtual environment
    python3 -m venv ara

    # Activate the virtual environment
    source ara/bin/activate

Install ``ara-server``::

    # From source
    pip install git+https://git.openstack.org/openstack/ara-server

    # or from PyPi
    pip install ara-server
