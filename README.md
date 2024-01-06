# small-ass-cache

![Icon](icon.png)

## What is it?

The "SMALL ASSet Cache" is a single file asset management system that lets you declare your assets once and load them when you need them. It is really intended to be used for games, but can be used for any project that needs to load assets from a file system.

## Why was it made?

I got tired of writing the same shit over and over. This enables my future self be lazy.

## But why should I use it?

Has the following advantages:

- Lets you declare your assets in the same place as the paths (no more dictionary of mappings).
- Uses an enum as the base type for your assets (instead of strings). This means your editor will autocomplete your asset names for you.
- Your editor will autocomplete your asset names for you.
- Your editor will autocomplete your asset names for you.
- Your editor will autocomplete your asset names for you.
- Your editor may also detect asset name typos. (thank you)
- Has a preload feature to warm the cache.
- Is already written.
- Is only like 100 lines of code. (Hackable, Grokkable.)

## How do?

### Installation

1. Install

   ```bash
   pip install small-ass-cache
   ```

2. Import

   ```python
   from small_ass_cache import {
       AssetCache,
       loader
   }
   ```

### 1. Define Loading Functions

First, define some functions for loading each type of asset.
Here are some example load functions for loading images and audio files:

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

### 2. Define Your Assets

Next, define your assets.

The @loader decorator is how you make define assets. The assets are paired with your load function.
If you have assets that need different load functions because they are different file types, define them seperately.
Your assets are Enums so you can match on them and such, so you have to derive from Enum.

```python
from small_ass_cache import loader

@loader(load_image, path="assets/images/")
class Images(Enum):
    CHIPS = "chips.png"
    FOOD = "food.png"
    GEAR = "gear.png"

@loader(load_audio, path="assets/audio/")
class Audio(Enum):
    GO = "go.wav"
    AWAY = "away.wav"

```

If you want you can just put full paths in your assets. It's optional in the @loader, but you are weird.
```python
@loader(load_txt)
class Audio(Enum):
    A_THING = "moms_files/credit_card.txt"
    A_TOTALLY_DIFFERENT_THING = "users/you/home/documents/social_security.txt"

```

### 3. Use Your Asset Cache

Make an instance of the AssetCache class.
When you need an asset, get it from the cache.
If the asset is not in the cache, it will be loaded from "disk" and added to the cache.
The second time you request the asset, it will already be in the cache and gets returned immediately.

```python
from small_ass_cache import AssetCache

assets = AssetCache()
image_asset = assets.get(Images.FOOD) # a cold load
fat_audio_asset = assets.get(Audio.GO) # also a cold load
the_same_image_asset = assets.get(Images.FOOD) # a warm load


#now go do something with your sorry asset
the_same_image_asset.show()
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

### 5. Call The Cops

```python
def load_remote(url):
    # convert URL to safe local filename
    local_filename = safe_filename(url)
    local_path = os.path.join('assets/remote/', local_filename)

    # check if local file exists
    if not os.path.exists(local_path):
        # If not, download it
        print(f"Downloading: {url}")
        download_file(url, local_path)
    else:
        print(f"Using cached file: {local_path}")

    return load_audio(local_path)

@loader(load_remote, path="assets/remote/")
class Audio(Enum):
    BEEP_SOUND = "https://www.soundjay.com/button/beep-07.wav"
```

### 6. Get Creative

```python
def load_hf_model(model_name):
    return AutoModel.from_pretrained(model_name)

@loader(load_hf_model)
class HuggingFace(Enum):
    BERT_BASE_UNCASED = "bert-base-uncased"
    GPT2 = "gpt2"

loader = AssetCache()
bert_model = loader.get(HuggingFaceModels.BERT_BASE_UNCASED)
```

I know AutoModel already caches, but you get the idea.
