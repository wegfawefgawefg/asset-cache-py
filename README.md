# asset-cache-py
an okay asset cache that is very python 

## What is it?

Its an asset management system that lets you declare your assets once and load them when you need them. 

## Why use it?
Has the following advantages:
- Lets you declare your assets in the same place as the paths (no more dictionary of mappings)
- Uses an enum as the base type for your assets (instead of strings)
- This means your editor will autocomplete your asset names for you.
- Has a preload feature to warm the cache

## How do?
### 1. Define Loading Functions

First, define some functions for loading each type of asset. 
Here is an example for loading images and audio files:

```python
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
```

### 2. Define Your Asset Enums

Next, define your asset enums.


```python
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

```

- The base_path decorator lets you specify a base path so you dont have to type it over and over again. (optional)
- The loader decorator is how you specify a load function for the assets in that enum. (not optional) ((how do expect the library to account for any possible file type, including user defined ones?)) 


### 3. Use Your Asset Cache

Make an instance of the AssetCache class.
When you need an asset, get it from the cache.
If the asset is not in the cache, it will be loaded and added to the cache.
The second time you request the asset, it will already be in the cache and gets returned immediately.


```python
assets = AssetCache()
image_asset = assets.get(Images.FOOD) # a cold load
audio_asset = assets.get(Audio.GO)    # a cold load

#do somthing with your asset
image_asset.show()
play_audio(audio_asset)
```

### 4. Preloading and Managing Cached Assets

If you expect the next scene to use a lot of assets, you can preload them.

```python
assets = AssetCache()
assets.preload([Images.CHIPS, Audio.AWAY]) # this will be slow
image_asset = assets.get(Images.Chips) # this will be fast
```

Can also remove all or just one asset from the cache.

```python
assets.remove(Images.CHIPS) # no longer cached
assets.clear_cache() # remove all
```
