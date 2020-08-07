import os
import json

import yaml

from inoft_vocal_framework.safe_dict import SafeDict


class CliCache:
    _cache = None

    @staticmethod
    def get_cli_cache_filepath() -> str:
        filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cli_cache.yaml")
        if not os.path.isfile(filepath):
            with open(filepath, "w+") as cache_file:
                cache_file.write(yaml.safe_dump({}))
        return filepath

    @staticmethod
    def cache() -> SafeDict:
        if CliCache._cache is None:
            CliCache.load_cache_from_yaml()
        return CliCache._cache

    @staticmethod
    def load_cache_from_json():
        expected_cli_cache_filepath = CliCache.get_cli_cache_filepath()
        if os.path.exists(expected_cli_cache_filepath):
            with open(expected_cli_cache_filepath) as cache_file:
                CliCache._cache = SafeDict(json.load(cache_file))

    @staticmethod
    def load_cache_from_yaml():
        expected_cli_cache_filepath = CliCache.get_cli_cache_filepath()
        if os.path.exists(expected_cli_cache_filepath):
            with open(expected_cli_cache_filepath) as cache_file:
                CliCache._cache = SafeDict(yaml.safe_load(cache_file))

    @staticmethod
    def save_cache_to_json():
        with open(CliCache.get_cli_cache_filepath(), "w+") as cache_file:
            cache_file.write(json.dumps(CliCache.cache().to_dict()))

    @staticmethod
    def save_cache_to_yaml():
        with open(CliCache.get_cli_cache_filepath(), "w+") as cache_file:
            cache_file.write(yaml.safe_dump(CliCache.cache().to_dict()))

    # todo: fix big issue in the situation that 2 project are done with the same framework,
    #  the cache of the first project will not allow the cache of the second to be create,
    #  and so, the user will get stuck getting proposed an app settings file that is not the write
    #  one for his project
