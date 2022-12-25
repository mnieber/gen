import os
from pathlib import Path

import ramda as R

from moonleap.packages.scope_manager import ScopeManager
from moonleap.settings import load_settings
from moonleap.utils.inflect import install_plural

_session = None


class Session:
    def __init__(self, spec_dir, settings_fn, output_root_dir):
        self.spec_dir = spec_dir
        self.settings_fn = settings_fn
        self.settings = None
        self.scope_manager = ScopeManager()
        self.output_root_dir = output_root_dir
        self.output_dir = f"{output_root_dir}/output"
        self.expected_dir = f"{output_root_dir}/expected"
        self.snapshot_fn = f"{output_root_dir}/snapshot.json"
        self.type_specs_dir = os.path.join(self.spec_dir, "type_specs")

    @property
    def spec_fn(self):
        spec_fn = Path(self.spec_dir) / "spec.md"
        if not spec_fn.exists():
            raise Exception(f"Spec file not found: {spec_fn}")
        return spec_fn

    def load_settings(self):
        settings_fn = Path(self.spec_dir) / self.settings_fn
        if not settings_fn.exists():
            raise Exception(f"Settings file not found: {settings_fn}")
        self.settings = load_settings(settings_fn)
        self.settings["spec_dir"] = self.spec_dir
        self.scope_manager.import_packages(self.settings.get("packages_by_scope", {}))

        for one, many in self.settings.get("plurals", {}).items():
            install_plural(one, many)

    def get_post_process_settings(self):
        return self.settings.get("post_process", {})

    def get_bin_settings(self):
        return self.settings.get("bin", {})

    def report(self, x, end=os.linesep):
        print(x, end=end)

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
