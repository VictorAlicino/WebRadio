import rich
import vlc
import time

media_path = "http://alicinotestserver:8000/labiot-radio.ogg"

if __name__ == "__main__":
    media = vlc.MediaPlayer(media_path)
    media.play()
    time.sleep(1)
    while media.is_playing():
        pass

