import typing as T

from moonleap.gqlspec.gql_spec import GqlSpec
from moonleap.gqlspec.load_gql_specs import load_gql_specs
from moonleap.session import get_session


class GqlSpecStore:
    def __init__(self):
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


_gql_spec_store = None


def gql_spec_store():
    global _gql_spec_store
    if _gql_spec_store is None:
        _gql_spec_store = GqlSpecStore()
        load_gql_specs(_gql_spec_store, get_session().spec_dir)
    return _gql_spec_store
