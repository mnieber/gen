import typing as T
from dataclasses import dataclass

from moonleap import Resource
from titan.api_pkg.pkg.api_spec import ApiSpec


@dataclass
class ApiRegistry(Resource):
    def __post_init__(self):
        self._api_spec_by_name = {}

    def setdefault(self, name, default_value):
        if not self.has(name):
            self._api_spec_by_name[name] = default_value

    def has(self, name):
        return bool(self._api_spec_by_name.get(name, None))

    def get(self, name, default="__not_set__") -> ApiSpec:
        result = self._api_spec_by_name.get(name, None)
        if result is None:
            if default == "__not_set__":
                raise Exception(f"Missing api spec: {name}")
            return T.cast(ApiSpec, default)
        return result

    def api_specs(self):
        return self._api_spec_by_name.values()
