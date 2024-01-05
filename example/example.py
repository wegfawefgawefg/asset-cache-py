import simpleaudio as sa
import wave
import numpy as np
from PIL import Image
from small_ass_cache import AssetCache, AssetMapping, base_path, loader

################    DEFINE YOUR LOADERS    ################


def load_image(path):
    return Image.open(path)


def load_audio(path):
    with wave.open(path, "rb") as wav_file:
        # Extract Audio Frames and parameters
        audio_data = wav_file.readframes(wav_file.getnframes())
        params = {
            "num_channels": wav_file.getnchannels(),
            "bytes_per_sample": wav_file.getsampwidth(),
            "sample_rate": wav_file.getframerate(),
        }
        return (audio_data, params)


################    DEFINE YOUR ASSETS    ################


@base_path("assets/images/")
@loader(load_image)
class Images(AssetMapping):
    CHIPS = "chips.png"
    FOOD = "food.png"
    GEAR = "gear.png"


@base_path("assets/audio/")
@loader(load_audio)
class Audio(AssetMapping):
    GO = "go.wav"
    AWAY = "away.wav"


################    USE IT    ################


# little utility function to play a sound
def play_audio(audio_data, params):
    audio_array = np.frombuffer(audio_data, dtype=np.int16)
    play_obj = sa.play_buffer(audio_array, **params)
    play_obj.wait_done()


assets = AssetCache()
assets.preload([Images.CHIPS, Audio.AWAY])

image_asset = assets.get(Images.FOOD)
image_asset.show()

sound_asset, sound_params = assets.get(Audio.GO)
play_audio(sound_asset, sound_params)


print("clearing cache...")
assets.clear_cache()
