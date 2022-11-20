# Add a stream
# 
# Input:
#   uuid -> UUID of the stream which will be added
#   playlist_dir -> Path for playlist
# Returns:
#   Tuple containg a list with the source output, the dynamic source, and pause control, the key is the uuid
def new_icecast_stream(uuid, playlist_dir)
    log.important("Adding radio #{uuid} playing -> #{playlist}.")
    dynamic_source = source.dynamic() # Defining a dynamic source
    dynamic_source = amplify(general_volume, dynamic_source) # Set the source volume to the general volume
    stream_output = output.icecast(%vorbis,
        host = streamer_host, 
        port = streamer_port,
        password = streamer_pass, 
        mount = "{uuid}.ogg",
        dynamic_source
    )
    # The following lines add the play/pause functionality
    is_paused = ref(false)
    audio_files = mksafe(playlist(playlist_dir, reload_mode="watch"))
    source = switch( [ (is_paused, blank()), (!=is_paused, audio_files) ] )
    
    dynamic_source.set(source) # Set the dynamic source to the playlist given
    (uuid, [stream_output, dynamic_source, is_paused]) # Creates a tuple with a list, the key is the uuid
end

# Removes a stream
# 
# Input:
#   uuid -> UUID of the stream to be removed
# Returns:
#   Unit
def change_stream_playlist_dir(uuid, new_dir)
    dynamic_source = list.nth(list.assoc(uuid, outputs), 1)
    audio_files = mksafe(playlist(new_dir, reload_mode="watch"))
    source = switch( [ (is_paused, blank()), (!=is_paused, audio_files) ] )
    dynamic_source.set(source)
    ()
end

# Removes a stream
# 
# Input:
#   uuid -> UUID of the stream to be removed
# Returns:
#   Unit
def remove_icecast_stream(uuid)
    stream_output = list.nth(list.assoc(uuid, outputs), 0)
    outputs := list.assoc.remove(uuid, outputs)
    stream_output.shutdown()
    "Stream #{uuid} was closed."
    ()
end

# Skip a track from a stream
# 
# Input:
#   uuid -> UUID of the stream which the skip will be performed
# Returns:
#   Unit
def skip_track(uuid)
    dynamic_source = list.nth(list.assoc(uuid, outputs), 1)
    dynamic_source.skip()
    ()
end



# Create a new output
# Please note that the output name (its UUID) also is the output mountpoint
# 
# Input:
#   uuid -> UUID of the new stream
#   playlist_dir -> Path for playlist
# Returns:
#   Unit
def new_radio(uuid, playlist_dir=="../Playlists")

end