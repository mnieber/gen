import os
from pathlib import Path

import yaml
from moonleap.session import get_session
from moonleap.typespec.default_field_specs_store import DefaultFieldSpecsStore
from moonleap.typespec.field_spec import field_specs_from_type_spec_dict
from moonleap.typespec.type_spec import TypeSpec, add_related_set_field_to_type_spec
from titan.api_pkg.pkg.ml_name import (
    ml_item_name_from_type_name,
    ml_type_name_from_item_name,
)

_default_type_spec_placeholder = TypeSpec(type_name="placeholder", field_specs=[])


def _load_type_spec_dict(type_specs_dir, type_name):
    spec_fn = os.path.join(type_specs_dir, type_name + ".json")
    if not os.path.exists(spec_fn):
        raise Exception(f"File not found: {spec_fn}")

    with open(spec_fn) as f:
        type_spec_dict = yaml.load(f, Loader=yaml.SafeLoader)
        if "properties" not in type_spec_dict:
            raise Exception(f"Field 'properties' not found in {type_spec_dict}")
        return type_spec_dict


class TypeSpecStore:
    def __init__(self):
        self._type_spec_by_type_name = {}
        self.default_field_specs_store = DefaultFieldSpecsStore()

    def load_specs(self, type_specs_dir):
        for spec_fn in Path(type_specs_dir).glob("*.json"):
            type_name = spec_fn.stem
            type_spec_dict = _load_type_spec_dict(type_specs_dir, type_name)

            type_spec = TypeSpec(
                type_name=type_name,
                field_specs=field_specs_from_type_spec_dict(type_spec_dict),
                select_item_by=type_spec_dict.get("selectItemBy", ["id"]),
                query_item_by=type_spec_dict.get("queryItemBy", ["id"]),
                display_item_by=type_spec_dict.get("displayItemBy", ["id"]),
                query_items_by=type_spec_dict.get("queryItemsBy", []),
            )
            self.setdefault(type_name, type_spec)

    def _on_add_type_spec(self, type_spec):
        for field_spec in type_spec.get_field_specs(["fk"]):
            if field_spec.field_type_attrs.get("hasRelatedSet"):
                fk_item_name = field_spec.target
                add_related_set_field_to_type_spec(
                    self.get(ml_type_name_from_item_name(fk_item_name)),
                    is_private=field_spec.private,
                    related_item_name=ml_item_name_from_type_name(type_spec.type_name),
                )

    def register_default_field_spec(self, type_name, field_spec):
        self.default_field_specs_store.register_field_spec(type_name, field_spec)

    def setdefault(self, type_name, default_value):
        assert type_name and type_name[0] == type_name[0].upper()

        if not self.has(type_name):
            self._type_spec_by_type_name[type_name] = default_value
            self._on_add_type_spec(default_value)

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


_type_spec_store = None


def type_spec_store():
    global _type_spec_store
    if _type_spec_store is None:
        _type_spec_store = TypeSpecStore()
        _type_spec_store.load_specs(get_session().type_specs_dir)
    return _type_spec_store
