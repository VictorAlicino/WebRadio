Client Controls
================

The client provided in this repository can only be controlled via MQTT.
All commands can be send to an unique topic, but this topic must be exclusive for the client.

The topic is defined in the configuration file and can be changed to whatever you want.

.. note::

    The configuration file is loaded when the client starts. If you change the configuration file, you must restart
    the client service.

The client can be controlled via the following commands:

- ``play``: Alters the player state to play the stream.
- ``pause``: Alters the player state to paused.
- ``stop``: Stop the stream.
- ``mute``: Mute the stream.
- ``unmute``: Unmute the stream.
- ``volume+``: Increases the volume in 20.
- ``volume-``: Decreases the volume in 20.
- ``volume=``: Alters the volume of the stream. The volume must be between 0 and 100.
- ``source=``: Changes the stream source. The source must be one of the sources defined in the configuration file.
- ``add_source=``: Adds a new source to the stream. The source will also be added to the configuration file.
- ``remove_source=``: Removes a source from the stream. The source will also be removed from the configuration file.


.. describe:: Examples:

    .. describe:: play

        ..code-block:: bash

            mosquitto_pub -h localhost -t ``SPEAKER TOPIC` -m "play"


