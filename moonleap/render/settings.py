import os

from moonleap.utils import yaml2dict

settings = None


def load_settings_file():
    global settings

    if settings is None:
        fn = "moonleap.yml"
        if not os.path.exists(fn):
            return dict()

        with open("moonleap.yml") as ifs:
            settings = yaml2dict(ifs.read())

    return settings
