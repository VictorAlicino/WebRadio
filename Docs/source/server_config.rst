Server Configuration
====================

Icecast2
--------

First we have to configure the Icecast.

Icecast configuration is done by a XML file located in ``/etc/icecast2/icecast.xml``.

Choose your editor of choice and open this file (you will need sudo).

.. code-block:: bash

    sudo nano /etc/icecast2/icecast.xml


Look for this line:

.. code-block:: xml

    <listen-socket>
        <port>8000</port>
        <!-- <bind-address>127.0.0.1</bind-address> -->
        <!-- <shoutcast-mount>/stream</shoutcast-mount> -->
    </listen-socket>

You can change the ``<port>`` parameter to any port you want to be the Icecast listening port, this will be
used by Liquidsoap for send the stream to Icecast.

To change the passwords you have to look for the authentication line, which look like this:

.. code-block:: xml

    <authentication>
        <source-password>hackme</source-password>
        <relay-password>hackme</relay-password>
        <admin-user>admin</admin-user>
        <admin-password>hackme</admin-password>
    </authentication>

After that you can restart Icecast to load de changes.

.. code-block:: bash

    sudo service icecast2 restart


NGINX
-----

If you want to use NGINX as a reverse proxy, you can create a new NGINX configuration file for Icecast.

.. code-block:: bash

    sudo nano /etc/nginx/conf.d/icecast.conf


And add this content:

.. code-block:: nginx

    server {
        listen 80;
        server_name YOUR_URL_HERE;

        location / {
            proxy_pass http://localhost:8000;
        }
    }

Save the file and run the following command to test the configuration:

.. code-block:: bash

    sudo nginx -t

If the configuration is correct, you can restart NGINX:

.. code-block:: bash

    sudo systemctl restart nginx


Liquidsoap
----------

For liquidsoap to work properly, you will have to modify some script lines.

#. Step 1: Connect to Icecast

    Inside the ``Server/scripts/`` folder, locate the ``streamer_config.liq`` file, this file contains the streamer
    information, in our case, the Icecast.

    In ``streamer_config.liq`` modify the following lines:

    .. code-block:: OCaml

        streamer_host = "localhost"
        streamer_port = 8000
        streamer_pass = "hackme"


    Change the ``streamer_host`` to the IP of your server, the ``streamer_port`` to the port you configured in Icecast
    and the ``streamer_pass`` to the password you configured in Icecast.

#. Step 2: Set the correct paths

    Inside the ``Server/scripts/`` folder, locate the ``main.liq`` file, this is the main file of the script.

    .. code:: OCaml

        log.file.path.set("PATH-TO-LOG/log/history.log")

    On line 4, change the ``PATH-TO-LOG`` string to the desired path of the log file.

    .. code:: OCaml

        playlists = file.ls("PATH-TO-PLAYLISTS")

    On line 9, change the ``PATH-TO-PLAYLITS`` string to the desired path of the playlists folders.

    Locate the file ``radio.liq``,

    .. code:: OCaml

        s = mksafe(playlist("PATH-TO-PLAYLISTS/#{list}"))
    
    on line 9, change the ``PATH-TO-PLAYLISTS`` with the same path to the playlists folder.

    .. note::

        Inside the playlists folders, every different folder will generate a different stream with the files of the folder.

#. Step 3: Make it a daemon

    Copy the ``script`` folder to ``liquidsoap-daemon`` directory.

    .. code-block:: bash

        cp -r PATH-TO-REPOSITORY/Server/script ~/liquidsoap-daemon/

    Run ``daemonize-liquidsoap.sh <script-name>``.

    .. code-block:: bash

        ~/liquidsoap-daemon/daemonize-liquidsoap.sh ~/liquidsoap-daemon/script/webradio.liq

    Start the Systemd service.

    .. code-block:: bash

        sudo systemctl start webradio-liquidsoap