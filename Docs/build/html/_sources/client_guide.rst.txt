Client Controls
================

The client provided in this repository can only be controlled via MQTT.
All commands can be send to an unique topic, but this topic must be exclusive for the client.

The topic is defined in the configuration file and can be changed to whatever you want.

.. note::

    The configuration file is loaded when the client starts.
    If you change the configuration file, you must restart
    the client service.

The client can be controlled via the following commands:

.. describe:: MQTT Commands

    .. describe:: play

            Alters the player state to play the stream.

            .. code-block:: bash

                mosquitto_pub -h localhost -t %SPEAKER_TOPIC -m "play"

    .. describe:: pause

                Alters the player state to paused.

                .. code-block:: bash

                    mosquitto_pub -h localhost -t %SPEAKER_TOPIC -m "pause"

    .. describe:: stop

                Stop the stream.

                .. code-block:: bash

                    mosquitto_pub -h localhost -t %SPEAKER_TOPIC -m "stop"

    .. describe:: mute

                Mute the stream.

                .. code-block:: bash

                    mosquitto_pub -h localhost -t %SPEAKER_TOPIC -m "mute"

    .. describe:: unmute

                Unmute the stream.

                .. code-block:: bash

                    mosquitto_pub -h localhost -t %SPEAKER_TOPIC -m "unmute"

    .. describe:: volume+

                Increases the volume in 20.

                .. code-block:: bash

                    mosquitto_pub -h localhost -t %SPEAKER_TOPIC -m "volume+"

    .. describe:: volume-

                Decreases the volume in 20.

                .. code-block:: bash

                    mosquitto_pub -h localhost -t %SPEAKER_TOPIC -m "volume-"

    .. describe:: volume=

                Set the stream volume to a specific value.

                .. note::

                    The volume must be between 0 and 100 (VLC actually supports up to 200, but please don't do that).

                .. code-block:: bash

                    mosquitto_pub -h localhost -t %SPEAKER_TOPIC -m "volume=50"

    .. describe:: source=

                Changes the stream source.
                The source must be one of the sources defined in the configuration file.

                .. code-block:: bash

                    mosquitto_pub -h localhost -t %SPEAKER_TOPIC -m "source=LabIoT Radio"

                .. note::

                    Use only the source ``name`` to change sources.

    .. describe:: add_source=

                Adds a new source to the stream.

                .. note::

                    The source will also be added to the configuration file.

                Send a single string containing the source ``name``, stream ``type`` and the source ``path``
                separated by a semicolon ``;``.

                .. code-block:: bash

                    mosquitto_pub -h localhost -t %SPEAKER_TOPIC -m \
                    "add_source=NewRadio;WebRadio;http://streaming.radionomy.com/80s-Remix"


    .. describe:: remove_source=

                Removes a source from the stream.

                Send a single string containing the source ``name``.

                .. code-block:: bash

                    mosquitto_pub -h localhost -t %SPEAKER_TOPIC -m "remove_source=NewRadio"

                .. warning::

                    The source will also be removed from the configuration file.