import vlc
import time
import json
import os
import paho.mqtt.client as mqtt

config_path = f"/home/{os.getlogin()}/config.json"  # Path to config file


class Source:
    """
    Class to represent the data structure of an audio source

    ...

    Attributes
    ----------
    name : str
        The name of the source
    source_type : str
        The type of the source (file, url, etc.)
    path : str
        The path to the source
    """

    name = ""
    source_type = ""
    path = ""

    def __init__(self, name, source_type, path):
        self.name = name
        self.source_type = source_type
        self.path = path


def add_source(source: Source):
    """
    Add a new source to the config file

    Parameters
    ----------
    source : Source
        The source to add
    """

    temp_config: json = None # Temporary config file
    with open(config_path, "r") as f_temp: # Open config file
        temp_config = json.load(f_temp)

    temp_config["speaker_config"]["sources"].append(
        {"name": source.name, "type": source.source_type, "path": source.path}
    ) # Add source to config file

    with open(config_path, "w") as f_temp: # Write config file
        json.dump(temp_config, f_temp)


def remove_source(source_name: str):
    """
    Remove a source from the config file

    Parameters
    ----------
    source_name : str
        The name of the source to remove
    """
    
    temp_config: json = None # Temporary config file
    with open(config_path, "r") as f_temp: # Open config file
        temp_config = json.load(f_temp)

    for i in range(len(temp_config["speaker_config"]["sources"])): # Loop through sources
        if temp_config["speaker_config"]["sources"][i]["name"] == source_name:
            temp_config["speaker_config"]["sources"].pop(i) # Remove source from config file
            break

    with open(config_path, "w") as f_temp: # Write config file
        json.dump(temp_config, f_temp)


class Speaker:
    """
    Class to control the speaker
    ...

    Attributes
    ----------
    _volume : int
        Speaker volume
    _mute : bool
        Whether the speaker is muted or not
    _source : str
        The source active on the speaker

    Methods
    -------
    set_volume(volume)
        Set the volume of the speaker
    set_mute(mute)
        Set whether the speaker is muted or not
    set_source(source)
        Set the source of the speaker
    get_volume()
        Get the volume of the speaker
    is_muted()
        Get whether the speaker is muted or not
    get_source()
        Get the source of the speaker

    """

    name = ""
    _volume = None
    _mute = False
    _source: Source = None

    def set_volume(self, volume):
        self._volume = volume
        temp_config: json = None
        with open(config_path, "r") as f_temp:
            temp_config = json.load(f_temp)

        temp_config["speaker_config"]["volume"] = self._volume

        with open(config_path, "w") as f_temp:
            json.dump(temp_config, f_temp)

    def set_mute(self, mute):
        self._mute = mute
        temp_config: json = None
        with open(config_path, "r") as f_temp:
            temp_config = json.load(f_temp)

        temp_config["speaker_config"]["mute"] = self._mute

        with open(config_path, "w") as f_temp:
            json.dump(temp_config, f_temp)

    def set_source(self, source):
        self._source = source

    def get_volume(self):
        return self._volume

    def is_muted(self):
        return self._mute

    def get_source(self):
        return self._source


class Player:
    """
    VLC player wrapper
    ...

    Attributes
    ----------
    _vlc_wrapper : vlc.MediaPlayer
        The VLC player wrapper
    sources : list
        The list of sources

    Methods
    -------
    begin(sources)
        Begin the player
    play()
        Play the current source
    pause()
        Pause the current source
    stop()
        Stop the current source
    set_volume(volume)
        Set the volume of the current source
    """
    sources: list[Source] = []
    _vlc_wrapper: vlc.MediaPlayer = None

    def __init__(self):
        self._vlc_wrapper = vlc.MediaPlayer()

    def begin(self, sources):
        list_of_sources = sources

        for source in list_of_sources:
            self.sources.append(Source(source["name"], source["type"], source["path"]))

        self._vlc_wrapper.set_media(vlc.Media(self.sources[0].path))
        speaker.set_source(player.sources[0])
        self._vlc_wrapper.play()
        time.sleep(1)

    def play(self):
        self._vlc_wrapper.play()
        print("▶️ Playing")

    def pause(self):
        self._vlc_wrapper.pause()
        print("⏸️ Paused")

    def stop(self):
        self._vlc_wrapper.stop()
        print("⏹️ Stopped")

    def set_volume(self, volume: int):
        self._vlc_wrapper.audio_set_volume(volume)
        speaker.set_volume(volume)
        print("🎚️ Volume set to", volume)

    def inc_volume(self):
        self._vlc_wrapper.audio_set_volume(self._vlc_wrapper.audio_get_volume() + 20)
        speaker.set_volume(self._vlc_wrapper.audio_get_volume())
        print("🔊︎ Volume increased in 20, now's at ", self._vlc_wrapper.audio_get_volume())

    def dec_volume(self):
        self._vlc_wrapper.audio_set_volume(self._vlc_wrapper.audio_get_volume() - 20)
        speaker.set_volume(self._vlc_wrapper.audio_get_volume())
        print("🔉 Volume decreased in 20, now's at ", self._vlc_wrapper.audio_get_volume())

    def mute(self, mute=False):
        self._vlc_wrapper.audio_set_mute(mute)
        speaker.set_mute(mute)
        if speaker.is_muted():
            print("🔇 Mute enabled")
        else:
            print("🔈 Mute disabled")

    def change_source(self, source: Source):
        self._vlc_wrapper.set_media(vlc.Media(source.path))
        speaker.set_source(source)
        self._vlc_wrapper.play()
        time.sleep(1)
        print("🔄 Source changed to", source.name)


# MQTT Message handler
def on_mqtt_message(client, userdata, msg):
    decoded_msg: str = msg.payload.decode("utf-8")

    if decoded_msg == "play":
        player.play()

    elif decoded_msg == "pause":
        player.pause()

    elif decoded_msg == "volume+":
        player.inc_volume()

    elif decoded_msg == "volume-":
        player.dec_volume()

    elif decoded_msg.startswith("volume="):
        player.set_volume(int(decoded_msg.split("=")[1]))

    elif decoded_msg == "mute":
        player.mute(True)

    elif decoded_msg == "unmute":
        player.mute(False)

    elif decoded_msg == "stop":
        player.stop()

    elif decoded_msg.startswith("source="):
        for source in player.sources:
            if source.name == decoded_msg.split("=")[1]:
                player.change_source(source)
                break

    elif decoded_msg.startswith("add_source="):
        source_data = decoded_msg.split("=")[1].split(";")
        player.sources.append(Source(source_data[0], source_data[1], source_data[2]))
        add_source(Source(source_data[0], source_data[1], source_data[2]))
        print(f"🔄 Added source {source_data[0]} ({source_data[2]})")

    elif decoded_msg.startswith("remove_source="):
        for source in player.sources:
            if source.name == decoded_msg.split("=")[1]:
                player.sources.remove(source)
                print("⏏️ Removed source", source.name)
                break

        remove_source(decoded_msg.split("=")[1])


# Global variables
player = Player()
speaker = Speaker()

if __name__ == "__main__":
    # Configuration
    # Loading configuration file
    print("---Loading configuration file---\n")
    with open(config_path, "r") as f:
        config = json.load(f)

    # Setting speaker
    speaker.name = config["speaker_config"]["name"]
    player.begin(config["speaker_config"]["sources"])
    player.mute(config["speaker_config"]["mute"])
    player.set_volume(config["speaker_config"]["volume"])

    # MQTT
    mqtt_client = mqtt.Client(speaker.name)
    # If you want to use a specific username and password:
    if config["mqtt_config"]["user"] and config["mqtt_config"]["password"]:
        mqtt_client.username_pw_set(config["mqtt_config"]["user"], config["mqtt_config"]["password"])
    # Setting callbacks
    mqtt_client.on_message = on_mqtt_message
    # Connecting to the server
    mqtt_client.connect(config["mqtt_config"]["server"], config["mqtt_config"]["port"], 60)
    # Subscribing to the topic
    mqtt_client.subscribe(config["mqtt_config"]["topic"])

    # Cleaning the variables
    del config

    print("\n-----Configurations loaded------\n")
    print("--------------LOGS--------------\n")
    mqtt_client.loop_forever()
