import os
import typing as T
from dataclasses import dataclass, field
from pathlib import Path

import ramda as R
import yaml
from moonleap.session import get_session
from moonleap.utils.case import camel_to_snake, lower0, snake_to_camel, upper0
from moonleap.utils.inflect import plural

fk_prefix = "/data_types/"


@dataclass
class FieldSpec:
    field_type: str
    name_snake: str
    name: str
    private: bool
    required: bool
    default_value: T.Any = None
    description: T.Optional[str] = None
    unique: bool = False
    field_type_attrs: dict = field(default_factory=dict)


@dataclass
class TypeSpec:
    type_name: str
    field_spec_by_name: T.Dict[str, FieldSpec]


_default_type_spec_placeholder = TypeSpec(
    type_name="placeholder", field_spec_by_name={}
)
_default_field_spec_by_name = R.index_by(
    R.prop("name"),
    [
        FieldSpec(
            name_snake="id",
            name="id",
            required=True,
            private=False,
            field_type="string",
        ),
        FieldSpec(
            name_snake="name",
            name="name",
            required=True,
            private=False,
            field_type="string",
        ),
    ],
)


def _field_type_and_attrs(field_spec_dict):
    attrs = {}
    t = field_spec_dict.get("type")

    if t is None:
        ref = field_spec_dict.get("$ref", "")
        if ref.startswith(fk_prefix):
            t = "fk"
            attrs["target"] = ref[len(fk_prefix) :]  # noqa: E203
            attrs["inline"] = field_spec_dict.get("inline", False)
            if attrs["inline"] and field_spec_dict.get("has_related_set"):
                raise Exception(
                    f"Field cannot be inline and have a related set: {field_spec_dict.name}"
                )
            attrs["has_related_set"] = (
                False
                if attrs["inline"]
                else field_spec_dict.get("has_related_set", True)
            )
    else:
        if "onDelete" in field_spec_dict:
            attrs["on_delete"] = field_spec_dict["onDelete"]

        if "maxLength" in field_spec_dict:
            attrs["max_length"] = field_spec_dict["maxLength"]

    return t, attrs


def _default_value(field_spec):
    return field_spec.get("default", None)


def _unique(field_spec):
    return field_spec.get("unique", False)


def _description(field_spec):
    return field_spec.get("description")


def _load_type_spec_dict(type_spec_dir, type_name):
    spec_fn = os.path.join(type_spec_dir, type_name + ".json")
    if not os.path.exists(spec_fn):
        raise Exception(f"File not found: {spec_fn}")

    with open(spec_fn) as f:
        type_spec_dict = yaml.load(f, Loader=yaml.SafeLoader)
        if "properties" not in type_spec_dict:
            raise Exception(f"Field 'properties' not found in {type_spec_dict}")
        return type_spec_dict


def _get_field_specs(type_spec_dict):
    required = type_spec_dict.get("required", [])
    private = type_spec_dict.get("private", [])
    result = []
    for field_name, field_spec_dict in type_spec_dict["properties"].items():
        t, attrs = _field_type_and_attrs(field_spec_dict)
        if t is None:
            raise Exception(f"Unknown field type for field: {field_name}")

        result.append(
            FieldSpec(
                default_value=_default_value(field_spec_dict),
                description=_description(field_spec_dict),
                field_type=t,
                field_type_attrs=attrs,
                name_snake=field_name,
                name=snake_to_camel(field_name),
                private=field_name in private,
                required=field_name in required,
                unique=_unique(field_spec_dict),
            )
        )
    return result


class TypeSpecStore:
    def __init__(self):
        self._type_spec_by_type_name = {}

    def _load_specs(self, data_types_dir):
        for spec_fn in Path(data_types_dir).glob("*.json"):
            type_name = spec_fn.stem
            type_spec_dict = _load_type_spec_dict(data_types_dir, type_name)

            spec = TypeSpec(
                type_name=type_name,
                field_spec_by_name=R.index_by(
                    R.prop("name"), _get_field_specs(type_spec_dict)
                ),
            )
            self._type_spec_by_type_name[type_name] = spec

        for type_name, spec in list(self._type_spec_by_type_name.items()):
            for _, field in spec.field_spec_by_name.items():
                if field.field_type == "fk" and field.field_type_attrs.get(
                    "has_related_set"
                ):
                    fk_type_spec = self.get(field.field_type_attrs["target"])
                    name = lower0(plural(spec.type_name))
                    fk_type_spec.field_spec_by_name[name] = FieldSpec(
                        name=name,
                        name_snake=camel_to_snake(name),
                        required=False,
                        private=field.private,
                        field_type="related_set",
                        field_type_attrs=dict(target=spec.type_name),
                    )

    def get(self, type_name, default=_default_type_spec_placeholder):
        if not self._type_spec_by_type_name:
            self._load_specs(
                os.path.join(get_session().settings["spec_dir"], "data_types")
            )

        type_name = upper0(type_name)
        if type_name not in self._type_spec_by_type_name:
            self._type_spec_by_type_name[type_name] = (
                TypeSpec(
                    type_name=type_name, field_spec_by_name=_default_field_spec_by_name
                )
                if default is _default_type_spec_placeholder
                else default
            )

        return self._type_spec_by_type_name[type_name]


type_spec_store = TypeSpecStore()
