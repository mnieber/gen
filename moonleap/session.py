import importlib
import re
from pathlib import Path

from moonleap.builder.config import Context
from moonleap.builder.install import install_package
from moonleap.settings import load_settings

_session = None


def _import_package(package_name):
    try:
        return importlib.import_module(package_name)
    except ImportError:
        raise


class Session:
    def __init__(self, spec_dir, settings_fn, output_root_dir):
        self.spec_dir = spec_dir
        self.settings_fn = settings_fn
        self.settings = None
        self.output_root_dir = output_root_dir
        self._context_by_name = {}
        self._package_by_name = {}

    def get_context(self, context_name):
        context = self._context_by_name.get(context_name)
        if not context:
            raise Exception(f"Context not specified in packages.yml: {context_name}")
        return context

    def load_settings(self):
        settings_fn = Path(self.spec_dir) / self.settings_fn
        if not settings_fn.exists():
            raise Exception(f"Settings file not found: {settings_fn}")
        self.settings = load_settings(settings_fn)
        self.settings["spec_dir"] = self.spec_dir
        self._import_packages(self.settings.get("packages_by_context_name", {}))

    def _import_packages(self, packages_by_context_name):
        for context_name, package_names in packages_by_context_name.items():
            context = self._context_by_name[context_name] = Context(context_name)

            for package_name in package_names:
                package = self._install_package(package_name)
                for module in getattr(package, "modules", []):
                    context.add_rules(module)

    def _install_package(self, package_name):
        package = self._package_by_name.get(package_name)
        if package:
            return package

        self._package_by_name[package_name] = package = _import_package(package_name)
        install_package(package)
        return package

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


def get_local_context_names(text):
    context_names_pattern = r"(\{(((\s)*[_\w\-]+(\,)?)+)\})"
    matches = re.findall(context_names_pattern, text, re.MULTILINE)
    return matches[0] if matches else None
