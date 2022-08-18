import typing as T
from collections import defaultdict

from moonleap.session import get_session
from moonleap.typespec.default_field_specs_store import DefaultFieldSpecsStore
from moonleap.typespec.load_type_specs import load_type_specs
from moonleap.typespec.type_spec import TypeSpec

_default_type_spec_placeholder = TypeSpec(type_name="placeholder", field_specs=[])


class TypeSpecStore:
    def __init__(self):
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

    def register_parent_child(self, parent_type_name, child_type_name, is_sure_parent):
        self.parents_by_type_name[child_type_name].append(
            (parent_type_name, is_sure_parent)
        )


_type_spec_store = None


def type_spec_store():
    global _type_spec_store
    if _type_spec_store is None:
        _type_spec_store = TypeSpecStore()
        load_type_specs(_type_spec_store, get_session().spec_dir)
    return _type_spec_store
