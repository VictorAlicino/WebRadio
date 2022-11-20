# Allowing commands from outside using telnet
server.telnet()

def telnet_skip_track(x)
    uuid = string.split(separator=" ", x)
    skip_track(uuid)
    "Skipped one track for stream #{uuid}"
end

server.register(usage="skip <stream_uuid>",
                description="Skip to the next track on the queue",
                "skip", telnet_skip_track)


# //TODO: ADD THE PAUSE COMMAND