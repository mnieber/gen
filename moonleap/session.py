import importlib
import re
from pathlib import Path

from moonleap.builder.config import Context
from moonleap.builder.install import install_package
from moonleap.settings import load_settings
from moonleap.utils import yaml2dict

_session = None


class Session:
    def __init__(self, spec_dir, settings_fn, output_root_dir):
        self.spec_dir = spec_dir
        self.settings_fn = settings_fn
        self.settings = None
        self.output_root_dir = output_root_dir
        self.context_by_name = {}
        self.package_by_name = {}

    def _load_root_settings(self):
        settings_fn = Path(self.spec_dir) / self.settings_fn
        if not settings_fn.exists():
            raise Exception(f"Settings file not found: {settings_fn}")
        root_settings = load_settings(settings_fn)
        root_settings["spec_dir"] = self.spec_dir
        return root_settings

    def load_settings(self):
        self.settings = self._load_root_settings()

    def import_packages(self):
        def _load_package_settings(packages_fn):
            if packages_fn.exists:
                with open(packages_fn) as ifs:
                    return yaml2dict(ifs.read())
            return {}

        for context_name, package_names in _load_package_settings(
            Path(self.spec_dir) / "packages.yml"
        ).items():
            self._register_context(context_name, package_names)

    def _install_package(self, package_name):
        if package_name in self.package_by_name:
            return

        def _import_package(package_name):
            try:
                return importlib.import_module(package_name)
            except ImportError:
                raise

        package = _import_package(package_name)
        self.package_by_name[package_name] = package
        install_package(package)

    def _register_context(self, context_name, package_names):
        for package_name in package_names:
            self._install_package(package_name)

        def _create_context(context_name, package_names):
            context = Context(context_name)
            for package_name in package_names:
                package = self.package_by_name[package_name]
                for module in getattr(package, "modules", []):
                    context.add_rules(module)
            return context

        context = _create_context(context_name, package_names)
        self.context_by_name[context_name] = context

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
