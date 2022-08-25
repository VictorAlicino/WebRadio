import rich
import vlc
import time
import json
import paho.mqtt.client as mqtt


class Source:
    name = ""
    source_type = ""
    path = ""

    def __init__(self, name, source_type, path):
        self.name = name
        self.source_type = source_type
        self.path = path


class Speaker:
    name = ""
    _volume = None
    _mute = False
    _source = None


class Player:
    sources: list[Source] = []
    _vlc_wrapper = None
    _current_source = None

    def begin(self, sources):
        list_of_sources = sources

        for source in list_of_sources:
            self.sources.append(Source(source["name"], source["type"], source["path"]))

        self._vlc_wrapper = vlc.MediaPlayer(player.sources[0].path)
        self._vlc_wrapper.play()
        time.sleep(1)
        while self._vlc_wrapper.is_playing():
            pass

    # Play, Pause, Stop, Volume, Mute, Change Source
    def play(self):
        self._vlc_wrapper.play()

    def pause(self):
        self._vlc_wrapper.pause()

    def stop(self):
        self._vlc_wrapper.stop()

    def set_volume(self, volume: int):
        self._vlc_wrapper.audio_set_volume(volume)

    def inc_volume(self):
        self._vlc_wrapper.audio_set_volume(self._vlc_wrapper.audio_get_volume() + 25)

    def dec_volume(self):
        self._vlc_wrapper.audio_set_volume(self._vlc_wrapper.audio_get_volume() - 25)

    def mute(self, mute=False):
        self._vlc_wrapper.audio_set_mute(mute)


# MQTT Message handler
def on_mqtt_message(client, userdata, msg):
    # TODO: Change source, Add source, Remove source
    decoded_msg: str = msg.payload.decode("utf-8")
    print("Received message:", decoded_msg)
    if decoded_msg == "play":
        print("Playing")
        player.play()
    elif decoded_msg == "pause":
        print("Pausing")
        player.pause()
    elif decoded_msg == "volume+":
        print("Volume up")
        player.inc_volume()
    elif decoded_msg == "volume-":
        print("Volume down")
        player.dec_volume()
    elif decoded_msg.startswith("volume="):
        print("Setting volume to", decoded_msg.split("=")[1])
        player.set_volume(int(decoded_msg.split("=")[1]))
    elif decoded_msg == "mute":
        print("Mute enabled")
        player.mute(True)
    elif decoded_msg == "unmute":
        print("Mute disabled")
        player.mute(False)
    pass


player = Player()

if __name__ == "__main__":
    # Configuration
    # Loading configuration file
    with open("config.json", "r") as f:
        config = json.load(f)

    speaker = Speaker()
    player.begin(config["speaker_config"]["sources"])

    # Setting speaker
    speaker.name = config["name"]
    player.set_volume(config["volume"])
    player.mute(config["mute"])

    # MQTT
    mqtt_client = mqtt.Client(config["speaker"]["name"])
    # If you want to use a specific username and password:
    if config["mqtt"]["username"] and config["mqtt"]["password"]:
        mqtt_client.username_pw_set(config["mqtt"]["username"], config["mqtt"]["password"])
    # Connecting to the server
    mqtt_client.connect(config["mqtt"]["server"], config["mqtt"]["port"], 60)
    # Subscribing to the topic
    mqtt_client.subscribe(config["mqtt"]["topic"])
    # Setting callbacks
    mqtt_client.on_message = on_mqtt_message

    mqtt_client.loop_forever()
