#!/usr/bin/liquidsoap

# Log Directory
log.file.path.set("/log/radio.log")

# Variables 
outputs = ref[] # List with the all the Outputs
general_volume = interactive.float("general_volume", 1.) # Radio general volume (0.0 ~ 1.0)

# Includes
%include radio.liq
%include utils.liq
%include telnet.liq
%include icecast_config.liq