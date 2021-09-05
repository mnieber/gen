import os
from pathlib import Path

from moonleap.scope_manager import ScopeManager
from moonleap.settings import load_settings

_session = None


class Session:
    def __init__(self, spec_dir, settings_fn, output_root_dir):
        self.spec_dir = spec_dir
        self.settings_fn = settings_fn
        self.settings = None
        self.scope_manager = ScopeManager()
        self.output_dir = f"{output_root_dir}/output"
        self.expected_dir = f"{output_root_dir}/expected"
        self.snapshot_fn = f"{output_root_dir}/snapshot.json"

    def load_settings(self):
        settings_fn = Path(self.spec_dir) / self.settings_fn
        if not settings_fn.exists():
            raise Exception(f"Settings file not found: {settings_fn}")
        self.settings = load_settings(settings_fn)
        self.settings["spec_dir"] = self.spec_dir
        self.scope_manager.import_packages(self.settings.get("packages_by_scope", {}))

    def report(self, x, end=os.linesep):
        print(x, end=end)

    def get_tweaks(self):
        if not self.settings:
            raise Exception("No settings loaded")
        return self.settings.get("tweaks", {})


def set_session(session):
    global _session

    if _session:
        raise Exception("There already is a session")
    _session = session


def get_session():
    if not _session:
        raise Exception("There is no session")
    return _session
