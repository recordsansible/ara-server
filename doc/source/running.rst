Running and hosting ara-server
==============================

You don't need to run and host an instance of the ara-server API if you don't
need to expose your data to other people or systems.

If you do need to let people or systems leverage the API, it is a good practice
to avoid using the built-in development server (``ara-manage runserver``).

This documentation outlines the basics of hosting a public ara-server instance.

An Ansible role supporting the following deployment scenarios will eventually
be available.

With nginx, gunicorn and sqlite
-------------------------------

Create a user for ARA::

    # adduser ara --shell /sbin/nologin --home-dir /var/lib/ara

Install ara-server and gunicorn in a virtualenv::

    # sudo -u ara python3 -m venv /var/lib/ara/venv
    # sudo -u ara /var/lib/ara/venv/bin/pip install ara-server gunicorn

Initialize the database:

    # ARA_BASE_DIR=/var/lib/ara sudo -E -u ara /var/lib/ara/venv/bin/ara-manage migrate

Copy the static files (such as css or js) for the API frontend to ``/var/www/ara``:

    # mkdir -p /var/www/ara/static
    # ARA_STATIC_ROOT=/var/www/ara/static /var/lib/ara/venv/bin/ara-manage collectstatic

Set up a systemd unit file for guicorn to listen on ``127.0.0.1:8000`` in
``/etc/systemd/system/ara-server.service``::

    [Unit]
    Description=ARA Records Ansible API server
    After=network.target

    [Service]
    PIDFile=/run/ara-server/pid
    User=ara
    Group=ara
    RuntimeDirectory=ara-server
    WorkingDirectory=/var/lib/ara
    EnvironmentFile=/etc/default/ara-server
    ExecStart=/var/lib/ara/venv/bin/gunicorn --pid /run/ara-server/pid \
        --workers=4 --bind 127.0.0.1:8000 ara.server.wsgi
    ExecReload=/bin/kill -s HUP $MAINPID
    ExecStop=/bin/kill -s TERM $MAINPID
    PrivateTmp=true

    [Install]
    WantedBy=multi-user.target

Set up an EnvironmentFile in ``/etc/default/ara-server`` for the systemd service::

    # Put your settings here or, alternatively, set an ARA_SETTINGS variable to
    # point to a configuration file -- for example /var/lib/ara/server/default_config.yaml
    ARA_SETTINGS=/var/lib/ara/server/default_config.yaml
    # ARA_BASE_DIR=/var/lib/ara
    # ARA_ALLOWED_HOSTS="['127.0.0.1', 'localhost', 'api.ara.example.org']"

Enable and start the service::

    # systemctl enable ara-server --now

You should now have the gunicorn process running and listening on 127.0.0.1::

    # ps faux |grep ara
    ara      28925  0.1  1.1 101128 22788 ?        Ss   20:12   0:00 /var/lib/ara/venv/bin/python3 /var/lib/ara/venv/bin/gunicorn --pid /run/ara-server/pid --workers=4 --bind 127.0.0.1:8000 ara.server.wsgi
    ara      28928  0.1  1.6 139684 34300 ?        S    20:12   0:00  \_ /var/lib/ara/venv/bin/python3 /var/lib/ara/venv/bin/gunicorn --pid /run/ara-server/pid --workers=4 --bind 127.0.0.1:8000 ara.server.wsgi
    ara      28930  0.1  1.6 139684 34372 ?        S    20:12   0:00  \_ /var/lib/ara/venv/bin/python3 /var/lib/ara/venv/bin/gunicorn --pid /run/ara-server/pid --workers=4 --bind 127.0.0.1:8000 ara.server.wsgi
    ara      28931  0.1  1.6 139684 34296 ?        S    20:12   0:00  \_ /var/lib/ara/venv/bin/python3 /var/lib/ara/venv/bin/gunicorn --pid /run/ara-server/pid --workers=4 --bind 127.0.0.1:8000 ara.server.wsgi
    ara      28933  0.1  1.6 139688 34372 ?        S    20:12   0:00  \_ /var/lib/ara/venv/bin/python3 /var/lib/ara/venv/bin/gunicorn --pid /run/ara-server/pid --workers=4 --bind 127.0.0.1:8000 ara.server.wsgi

    # netstat -ntlp
    Active Internet connections (only servers)
    Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
    tcp        0      0 127.0.0.1:8000          0.0.0.0:*               LISTEN      28925/python3

The next step is to set up nginx as a reverse proxy to the gunicorn service we
just started.

The procedure to install nginx and the location of the configuration files are
slightly different depending on your Linux distribution packages.

The important part is the server configuration that you'll need to add to either
``/etc/nginx/conf.d/ara-server.conf`` or ``/etc/nginx/sites-enabled/ara-server.conf``::

    upstream ara_server {
        # fail_timeout=0 means we always retry an upstream even if it failed
        # to return a good HTTP response
        server 127.0.0.1:8000 fail_timeout=0;
    }

    server {
        listen 80;
        keepalive_timeout 5;
        server_name api.ara.example.org;
        root /var/www/ara;

        access_log /var/log/nginx/api.demo.recordsansible.org_access.log;
        error_log  /var/log/nginx/api.demo.recordsansible.org_error.log;

        location / {
            # checks for static file, if not found proxy to app
            try_files $uri @proxy_to_app;
        }

        location @proxy_to_app {
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_set_header Host $http_host;

            proxy_redirect off;
            proxy_pass http://ara_server;
        }
    }
