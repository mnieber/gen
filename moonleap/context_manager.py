import importlib
import re

from moonleap.builder.config import Context
from moonleap.builder.install import install_package


def _import_package(package_name):
    try:
        return importlib.import_module(package_name)
    except ImportError:
        raise


class ContextManager:
    def __init__(self):
        self._context_by_name = {}
        self._package_by_name = {}

    def get_context(self, context_name):
        context = self._context_by_name.get(context_name)
        if not context:
            raise Exception(f"Context not specified in packages.yml: {context_name}")
        return context

    def import_packages(self, packages_by_context_name):
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


def get_local_context_names(text):
    context_names_pattern = r"(\{(((\s)*[_\w\-]+(\,)?)+)\})"
    matches = re.findall(context_names_pattern, text, re.MULTILINE)
    return matches[0] if matches else None
