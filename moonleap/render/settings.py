import os

from moonleap.utils import yaml2dict

_settings = None


def get_settings():
    global _settings

    if _settings is None:
        fn = "moonleap.yml"
        if not os.path.exists(fn):
            return dict()

        with open("moonleap.yml") as ifs:
            _settings = yaml2dict(ifs.read())

    return _settings


def get_tweaks():
    return _settings.get("tweaks", {})
