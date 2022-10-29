import typing as T
from collections import defaultdict
from dataclasses import dataclass

from moonleap import Resource
from titan.types_pkg.typeregistry.type_spec import TypeSpec

from .default_field_specs_store import DefaultFieldSpecsStore

_default_type_spec_placeholder = TypeSpec(type_name="placeholder", field_specs=[])


@dataclass
class TypeRegistry(Resource):
    def __post_init__(self):
        self._type_spec_by_type_name = {}
        self.default_field_specs_store = DefaultFieldSpecsStore()
        self.parents_by_type_name = defaultdict(list)

    def setdefault(self, type_name, default_value):
        assert type_name and type_name[0] == type_name[0].upper()

        if not self.has(type_name):
            self._type_spec_by_type_name[type_name] = default_value

    def has(self, type_name):
        assert type_name and type_name[0] == type_name[0].upper()

        return type_name in self._type_spec_by_type_name

    def get(self, type_name, default=_default_type_spec_placeholder) -> TypeSpec:
        assert type_name and type_name[0] == type_name[0].upper()

        type_spec = self._type_spec_by_type_name.get(type_name, None)
        if type_spec is not None:
            return type_spec

        return (
            TypeSpec(
                type_name=type_name,
                field_specs=self.default_field_specs_store.get_field_specs(type_name),
            )
            if default is _default_type_spec_placeholder
            else default
        )

    def type_specs(self) -> T.List[TypeSpec]:
        return self._type_spec_by_type_name.values()

    def register_parent_child(self, parent_type_name, child_type_name):
        self.parents_by_type_name[child_type_name].append(parent_type_name)
