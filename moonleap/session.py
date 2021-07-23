import re
from importlib import import_module
from pathlib import Path

from moonleap.builder.install import install_package
from moonleap.settings import load_settings
from moonleap.utils.merge_into_config import merge_into_config

_session = None


class Session:
    def __init__(self, spec_dir, settings_fn, output_root_dir):
        self.spec_dir = spec_dir
        self.settings_fn = settings_fn
        self.settings = None
        self.output_root_dir = output_root_dir
        self.contexts = []
        self.uninstall_functions = []

    def _load_root_settings(self):
        settings_fn = Path(self.spec_dir) / self.settings_fn
        if not settings_fn.exists():
            raise Exception(f"Settings file not found: {settings_fn}")
        root_settings = load_settings(settings_fn)
        root_settings["spec_dir"] = self.spec_dir
        return root_settings

    def load_settings(self):
        self.settings = self._load_root_settings()
        for context in self.contexts:
            context_settings_fn = Path(self.spec_dir) / f"{context}.yml"
            if context_settings_fn.exists:
                merge_into_config(self.settings, load_settings(context_settings_fn))

        self._install_packages()

    def _install_packages(self):
        if self.uninstall_functions:
            raise Exception("Cannot install when there are uninstall functions pending")

        for package_name in (self.settings or {}).get("moonleap_packages", []):
            try:
                package = import_module(package_name)
            except ImportError:
                raise
            install_package(package, self.uninstall_functions)

    def _uninstall_packages(self):
        while self.uninstall_functions:
            uninstall = self.uninstall_functions.pop()
            uninstall()

    def set_contexts(self, contexts):
        if (self.contexts) == (contexts):
            return

        self._uninstall_packages()
        self.contexts = contexts
        self.load_settings()

    def report(self, x):
        print(x)

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


def get_local_contexts(text):
    contexts_pattern = r"(\{(((\s)*[_\w\-]+(\,)?)+)\})"
    matches = re.findall(contexts_pattern, text, re.MULTILINE)
    return matches[0] if matches else None
