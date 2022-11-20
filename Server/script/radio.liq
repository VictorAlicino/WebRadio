# Generate various sources from a playlist file
# 
# Input:
#   list -> List with path
# Returns:
#   Unit()
def generate_sources_by_playlists(list)
    log.important("Playing #{list}.")
    s = mksafe(playlist("PATH-TO-PLAYLISTS/#{list}"))
    ignore(
        output.icecast(
            %vorbis,
            host = streamer_host, 
            port = streamer_port,
            password = streamer_pass, 
            mount = "#{list}.ogg",
            s
        )
    )
    print("Created #{list}.ogg")
end