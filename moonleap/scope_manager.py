import importlib
import re

from moonleap.builder.config import Scope
from moonleap.builder.install import install_package


def _import_package(package_name):
    try:
        return importlib.import_module(package_name)
    except ImportError:
        raise


class ScopeManager:
    def __init__(self):
        self._scope_by_name = {}
        self._package_by_name = {}

    def get_scope(self, scope_name):
        scope = self._scope_by_name.get(scope_name)
        if not scope:
            raise Exception(f"Scope not specified in packages.yml: {scope_name}")
        return scope

    def import_packages(self, packages_by_scope):
        for scope_name, package_names in packages_by_scope.items():
            scope = self._scope_by_name[scope_name] = Scope(scope_name)

            for package_name in package_names:
                package = self._install_package(package_name)
                for module in getattr(package, "modules", []):
                    scope.add_rules(module)

    def _install_package(self, package_name):
        package = self._package_by_name.get(package_name)
        if package:
            return package

        self._package_by_name[package_name] = package = _import_package(package_name)
        install_package(package)
        return package


def get_local_scope_names(text):
    scope_names_pattern = r"(\{(((\s)*[_\w\-]+(\,)?)+)\})"
    matches = re.findall(scope_names_pattern, text, re.MULTILINE)
    return matches[0] if matches else None
