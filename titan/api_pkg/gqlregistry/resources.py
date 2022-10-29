import typing as T
from dataclasses import dataclass

from moonleap import Resource
from titan.api_pkg.pkg.gql_spec import GqlSpec


@dataclass
class GqlRegistry(Resource):
    def __post_init__(self):
        self._gql_spec_by_name = {}

    def setdefault(self, name, default_value):
        if not self.has(name):
            self._gql_spec_by_name[name] = default_value

    def has(self, name):
        return bool(self._gql_spec_by_name.get(name, None))

    def get(self, name, default="__not_set__") -> GqlSpec:
        result = self._gql_spec_by_name.get(name, None)
        if result is None:
            if default == "__not_set__":
                raise Exception(f"Missing gql spec: {name}")
            return T.cast(GqlSpec, default)
        return result

    def gql_specs(self):
        return self._gql_spec_by_name.values()
