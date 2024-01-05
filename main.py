from enum import Enum
import os

import simpleaudio as sa
import wave
import numpy as np
from PIL import Image  # Corrected import for PIL


################    SETTING THE STAGE   ################
class AssetPath:
    def __init__(self, base_path):
        self.base_path = base_path

    def full_path(self, filename):
        return os.path.join(
            self.base_path, filename
        )  # Using os.path.join for compatibility


def base_path(path):
    def decorator(cls):
        cls.get_base_path = classmethod(lambda c: AssetPath(path))
        return cls

    return decorator


def loader(load_func):
    def decorator(cls):
        cls.load = staticmethod(load_func)
        return cls

    return decorator


class AssetMapping(Enum):
    @classmethod
    def paths(cls):
        base = cls.get_base_path()
        return {member: base.full_path(member.value) for member in cls}


################    THE CACHE    ################
class AssetCache:
    def __init__(self):
        self.cache = {}

    def get(self, asset_enum):
        if asset_enum in self.cache:
            return self.cache[asset_enum]
        else:
            asset_type = type(asset_enum)
            try:
                # Attempt to retrieve the loader and base path.
                loader = asset_type.load
                base_path = asset_type.get_base_path()

                # Construct the full path and load the asset.
                full_path = base_path.full_path(asset_enum.value)
                if os.path.exists(full_path):
                    self.cache[asset_enum] = loader(full_path)
                    return self.cache[asset_enum]
                else:
                    raise ValueError(f"File not found: {full_path}")
            except AttributeError:
                # Handle the case where the necessary methods aren't found.
                raise TypeError(f"No load function defined for asset {asset_enum}")

    def remove(self, asset_enum):
        if asset_enum in self.cache:
            del self.cache[asset_enum]

    def preload(self, assets):
        for asset in assets:
            self.get(asset)

    def clear_cache(self):
        self.cache.clear()


################    USER DEFINED    ################
def play_audio(audio_data, params):
    # Convert the buffer to a NumPy array appropriate for playback
    audio_array = np.frombuffer(audio_data, dtype=np.int16)
    # Play the audio
    play_obj = sa.play_buffer(audio_array, **params)
    play_obj.wait_done()  # Wait until sound has finished playing


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


################    USAGE    ################

assets = AssetCache()
assets.preload([Images.CHIPS, Audio.AWAY])

image_asset = assets.get(Images.FOOD)
image_asset.show()

sound_asset, sound_params = assets.get(Audio.GO)
play_audio(sound_asset, sound_params)


print("clearing cache...")
assets.clear_cache()
