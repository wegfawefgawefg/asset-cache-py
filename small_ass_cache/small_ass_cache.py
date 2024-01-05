from enum import Enum
import os


################    SETTING THE STAGE   ################
class AssetPath:
    def __init__(self, base_path):
        self.base_path = base_path

    def full_path(self, filename):
        return os.path.join(
            self.base_path, filename
        )  # Using os.path.join for compatibility


def loader(load_func, path: str | None = None):
    def decorator(cls):
        cls.load = staticmethod(load_func)
        if path:
            cls.get_base_path = classmethod(lambda c: AssetPath(path))
        return cls

    return decorator


class AssetMapping(Enum):
    @classmethod
    def get_base_path(cls):
        return AssetPath("")

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
        asset_type = type(asset_enum)
        try:
            return self.load_and_cache_asset(asset_type, asset_enum)
        except AttributeError as e:
            # Handle the case where the necessary methods aren't found.
            raise TypeError(f"No load function defined for asset {asset_enum}") from e

    def load_and_cache_asset(self, asset_type, asset_enum):
        # Attempt to retrieve the loader and base path.
        loader = asset_type.load
        base_path = asset_type.get_base_path()

        # Construct the full path and load the asset.
        full_path = base_path.full_path(asset_enum.value)
        if not os.path.exists(full_path):
            raise ValueError(f"File not found: {full_path}")
        self.cache[asset_enum] = loader(full_path)
        return self.cache[asset_enum]

    def remove(self, asset_enum):
        if asset_enum in self.cache:
            del self.cache[asset_enum]

    def preload(self, assets):
        for asset in assets:
            self.get(asset)

    def clear_cache(self):
        self.cache.clear()
