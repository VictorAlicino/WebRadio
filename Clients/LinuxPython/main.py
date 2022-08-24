import rich
import vlc
import time
import json
import paho.mqtt.client as mqtt


class Source:
    name = ""
    type = ""
    path = ""


class Speaker:
    name = ""
    sources = []
    _volume = None
    _mute = False
    _source = None

    def set_volume(self, volume):
        self._volume = volume
        print("Setting volume to", volume)

    def set_mute(self, mute):
        self._mute = mute
        print("Setting mute to", mute)


if __name__ == "__main__":
    speaker = Speaker()

    # Configuration
    # Loading configuration file
    with open("config.json", "r") as f:
        config = json.load(f)

    # Setting speaker
    speaker.name = config["name"]
    speaker.set_volume(config["volume"])
    speaker.set_mute(config["mute"])

    # MQTT
    # Connecting to MQTT server
    client = mqtt.Client()
    client.connect(config["mqtt"]["server"], config["mqtt"]["port"], 60)

    #TODO: COMANDOS MQTT = play, pause, volume+, volume-, next, previous, mute, unmute, source

    # VLC
    media = vlc.MediaPlayer(speaker.sources[0])
    media.play()
    time.sleep(1)
    while media.is_playing():
        pass

    while True:
        pass
