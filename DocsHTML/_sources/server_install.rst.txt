Server Installation
===================

This document describes how to install the Web Radio application on any computer running Linux
(preferably Debian based distros).

For the server, we are going to need Icecast and Liquidsoap, and optionally we can also use Nginx as a reverse proxy.

Icecast 2
---------

The official documentation for Icecast can be found on https://icecast.org/docs/icecast-trunk/

For Linux users with Debian based distros, I highly recommend using the Advanced Package Tool.

.. code-block:: bash

    sudo apt-get install icecast2

.. note::

    Make sure to use icecast2 version 2.4.4 or higher

Liquidsoap
----------

The official documentation for Liquidsoap can be found on https://www.liquidsoap.info/doc-2.1.2/

.. note::

    This documentation version can only be trusted for Liquidsoap version 2.1.2 or above

Liquidsoap can also be installed via Advanced Package Tool, but the official documentation
recommends installing it using the OCaml Package Manager (OPAM), so, let's install it.

.. note::

    Liquidsoap official documentation also provides a docker container, see more at
    https://www.liquidsoap.info/doc-2.1.2/install.html#docker

.. code-block:: bash

    sudo apt-get install opam

.. note::

    Make sure your OPAM is at least version 2.0.

    Make sure your OCaml is at least version 4.12.0

For Liquidsoap to work properly you will need some dependencies, you can install all of them
in a single command, but make sure to get yourself some coffee, this is going to take a while.

.. note::

    For a list of all the dependencies available, run ``opam info liquidsoap``

First, make sure you have all the external dependencies needed in order to correct install the 
dependencies you want, this can be accomplished by running the ``opam depext command``.

.. code-block:: bash

    opam depext taglib mad lame vorbis cry samplerate liquidsoap

After that you can install,

.. code-block:: bash

    opam install taglib mad lame vorbis cry samplerate liquidsoap

For Liquidsoap to be able to run as daemon, we need the liquidsoap-daemon package.
Clone the liquidsoap-daemon repository in a convenient path.

.. code-block:: bash

    git clone https://github.com/savonet/liquidsoap-daemon.git

    