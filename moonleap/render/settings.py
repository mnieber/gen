import os

from moonleap.utils import yaml2dict


def load_settings_file():
    fn = "moonleap.yml"
    if not os.path.exists(fn):
        return dict()

    with open("moonleap.yml") as ifs:
        return yaml2dict(ifs.read())
