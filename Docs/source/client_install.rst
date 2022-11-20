Client Installation
===================

The WebRadio is a HTTP stream, so it can be played with any web browser or player that supports this format.

Bundled with this project is a client script written in Python that can listen to the stream and play it on the
local machine, it also can be controlled via MQTT. It is located in the `Client` directory.

Python dependencies
-------------------

The client script requires the following Python modules:

#. Eclipse Paho MQTT Client
    Get it by running `pip install paho-mqtt`

    .. code-block:: bash

        pip install paho-mqtt

#. Python VLC bindings
    Get it by running `pip install python-vlc`

    .. code-block:: bash

        pip install python-vlc

    .. note::

        You will need the LibVLC for this to work, you can get it from the Advanced Packaging Tool (APT)
        by running ``sudo apt-get install vlc`` or from the official website.


Configuration file
------------------

The client script requires a configuration file to be able to connect to the MQTT broker and the WebRadio stream.
The configuration file is located in the `Client` directory and is called `config.json`.

The configuration file is a JSON file with the following structure:

//TODO: Add configuration file structure


Systemd service
---------------

The client script can be run as a systemd service, to do so, copy the ``WebRadioClient.service`` file to
``/etc/systemd/system/``

.. code-block:: bash

    sudo cp WebRadio/Client/WebRadioClient.service /etc/systemd/system/

Then, edit the file and change the ``ExecStart`` line to point to the script location.

.. code-block:: bash

    sudo nano /etc/systemd/system/WebRadioClient.service

.. code-block:: ini

        [Unit]
        Description=Web Radio Player by LabIoT
        After=multi-user.target

        [Service]
        Type=simple
        User=YOUR_USERNAME
        Restart=always
        ExecStart=/usr/bin/python3 ~/WebRadio/Client/main.py

        [Install]
        WantedBy=multi-user.target

Then, enable and start the service.