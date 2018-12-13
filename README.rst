ara-server
==========

.. image:: doc/source/_static/ara-with-icon.png

ARA Records Ansible playbook runs and makes the recorded data available and
intuitive for users and systems.

ara-server is a modern python 3 application built with the latest releases of
`Django <https://www.djangoproject.com/>`_ and `django-rest-framework <https://www.django-rest-framework.org/>`_.

ara-server is the component from ARA that manages the REST API and the database.

.. image:: doc/source/_static/screenshot.png

- For the ARA Ansible callback plugin or the ``ara_record`` action module, look at `ara-plugins <https://github.com/openstack/ara-plugins>`_
- For the ARA REST API clients, look at `ara-clients <https://github.com/openstack/ara-clients>`_
- For the ARA web interface, look at `ara-web <https://github.com/openstack/ara-web>`_

Disclaimer
==========

``ara-server`` is not yet stable and will be shipped as part of a coordinated
ARA 1.0 release. It is not currently recommended for production use.

While most of the major work has landed, please keep in mind that we can still
introduce backwards incompatible changes until we ship the first release.

You are free to use this project and in fact, you are more than welcome to
contribute feedback, bug fixes or improvements !

If you are looking for a stable version of ARA, you can find the latest 0.x
version on PyPi_ and the source is available here_.

.. _PyPi: https://pypi.org/project/ara/
.. _here: https://github.com/openstack/ara

Documentation
=============

*Work in progress*

**TL;DR**: Using tox is convenient for the time being::

  # Retrieve the source
  git clone https://github.com/openstack/ara-server
  cd ara-server

  # Install tox from pip or from your distro packages
  pip install tox

  # Run an Ansible playbook integrated ara-server, ara-clients and ara-plugins
  # This will exercise all three components and record real data from Ansible
  tox -e ansible-integration

  # Run test server -> http://127.0.0.1:8000/api/v1/
  tox -e runserver

  # Run actual tests or get coverage
  tox -e linters
  tox -e py3
  tox -e cover

  # Build docs
  tox -e docs

Authors and contributors
========================

ARA was created by David Moreau Simard (@dmsimard) and contributors can be
found on GitHub_.

.. _GitHub: https://github.com/openstack/ara-server/graphs/contributors

Copyright
=========

::

    Copyright (c) 2018 Red Hat, Inc.

    ARA is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    ARA is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with ARA.  If not, see <http://www.gnu.org/licenses/>.
