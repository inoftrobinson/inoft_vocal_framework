import os
import json

from inoft_vocal_framework.safe_dict import SafeDict


class CliCache:
    _cache = None

    @staticmethod
    def get_expected_cli_cache_filepath():
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), "cli_cache.json")

    @staticmethod
    def cache() -> SafeDict:
        if CliCache._cache is None:
            CliCache.load_cache_from_json()
        return CliCache._cache

    @staticmethod
    def load_cache_from_json():
        expected_cli_cache_filepath = CliCache.get_expected_cli_cache_filepath()
        if os.path.exists(expected_cli_cache_filepath):
            with open(expected_cli_cache_filepath) as cache_file:
                CliCache._cache = SafeDict(json.load(cache_file))
        else:
            print(f"No cache file has been found at the filepath {expected_cli_cache_filepath}")
            CliCache._cache = SafeDict()

    @staticmethod
    def save_cache_to_json():
        with open(CliCache.get_expected_cli_cache_filepath(), "w+") as cache_file:
            cache_file.write(json.dumps(CliCache.cache().to_dict()))
