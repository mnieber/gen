import os

import ramda as R
from moonleap.session.settings import load_settings
from moonleap.utils.inflect import install_plural

_session = None


class Session:
    def __init__(self):
        self.settings = None
        self.trace_level = 1
        self.ws = None

    def load_settings(self, settings_fn):
        if not settings_fn.exists():
            raise Exception(f"Settings file not found: {settings_fn}")
        self.settings = load_settings(settings_fn)

        for one, many in self.settings.get("plurals", {}).items():
            install_plural(one, many)

    def init(self, workspace):
        self.ws = workspace

    def get_post_process_settings(self):
        return self.settings.get("post_process", {})

    def get_bin_settings(self):
        return self.settings.get("bin", {})

    def report(self, x, end=os.linesep):
        print(x, end=end)

    def warn(self, x, end=os.linesep):
        print(f"Warning: {x}", end=end)

    def get_setting_or(self, default_value, path):
        if not self.settings:
            raise Exception("No settings loaded")
        return R.path_or(default_value, path)(self.settings)


def set_session(session):
    global _session

    if _session:
        raise Exception("There already is a session")
    _session = session


def get_session():
    if not _session:
        raise Exception("There is no session")
    return _session


def trace(msg, level=0):
    session = get_session()
    if level <= session.trace_level:
        session.report(msg)
