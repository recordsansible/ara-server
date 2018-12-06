Running and hosting ara-server
==============================

You don't need to run and host an instance of the ara-server API if you don't
need to expose your data to other people or systems.

If you do need to let people or systems leverage the API, it is a good practice
to avoid using the built-in development server (``ara-manage runserver``).

This documentation outlines the basics of hosting a public ara-server instance.

With nginx, gunicorn and sqlite
-------------------------------

WIP