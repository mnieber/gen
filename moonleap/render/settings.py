import os

from moonleap.utils import yaml2dict

_settings = None


def load_settings(fn):
    global _settings

    if _settings is None:
        if not os.path.exists(fn):
            raise Exception(f"Settings file not found: {fn}")

        with open(fn) as ifs:
            _settings = yaml2dict(ifs.read())

    return _settings


def get_settings():
    global _settings

    if _settings is None:
        raise Exception(f"No settings file has been loaded")

    return _settings


def get_tweaks():
    return get_settings().get("tweaks", {})
