#!/usr/bin/liquidsoap

# Log Directory
log.file.path.set("/home/pi/WebRadio/log/history.log")

# Variables 
#sources = ref([]) # List with the all the Sources
#general_volume = interactive.float("general_volume", 1.) # Radio general volume (0.0 ~ 1.0)
playlists = file.ls("/home/pi/WebRadio/Playlists")

# Includes
%include "streamer_config.liq"
%include "radio.liq"
%include "utils.liq"
%include "telnet.liq"

# Main
list.iter(generate_sources_by_playlists, playlists)