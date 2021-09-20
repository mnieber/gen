import os
import typing as T
from dataclasses import dataclass, field, replace
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
    field_specs: T.List[FieldSpec]


_default_type_spec_placeholder = TypeSpec(type_name="placeholder", field_specs=[])
_default_field_specs = [
    FieldSpec(
        name_snake="id",
        name="id",
        required=True,
        private=False,
        field_type="uuid",
    ),
    FieldSpec(
        name_snake="name",
        name="name",
        required=True,
        private=False,
        field_type="string",
    ),
]


def _field_type_and_attrs(field_spec_dict):
    attrs = {}
    t = field_spec_dict.get("type")

    if t is None:
        ref = field_spec_dict.get("$ref", "")
        if ref.startswith(fk_prefix):
            t = "fk"
            attrs["target"] = ref[len(fk_prefix) :]  # noqa: E203
            attrs["inline"] = field_spec_dict.get("inline", False)
            if attrs["inline"] and field_spec_dict.get("hasRelatedSet"):
                raise Exception(
                    "Field cannot be inline and have a "
                    + f"related set: {field_spec_dict.name}"
                )
            attrs["has_related_set"] = (
                False if attrs["inline"] else field_spec_dict.get("hasRelatedSet", True)
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


def _load_type_spec_dict(type_specs_dir, type_name):
    spec_fn = os.path.join(type_specs_dir, type_name + ".json")
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


def _form_type_spec_from_data_type_spec(data_type_spec):
    def _convert(field_spec):
        changes = {}
        if field_spec.field_type in ("fk",):
            changes = dict(
                field_type="uuid",
                field_type_attrs={},
            )

        return replace(field_spec, **changes)

    return TypeSpec(
        type_name=data_type_spec.type_name + "Form",
        field_specs=R.pipe(
            R.always(data_type_spec.field_specs),
            R.filter(lambda x: x.field_type != "related_set"),
            R.map(_convert),
        )(None),
    )


def flattened_spec_field_by_name(type_spec, skip=None):
    if skip is None:
        skip = [type_spec.type_name]

    result = {}
    spec_fields = [x for x in type_spec.field_specs if not x.private]
    while spec_fields:
        spec_field = spec_fields.pop(0)
        if spec_field.field_type in ("fk", "related_set"):
            fk_type_name = spec_field.field_type_attrs["target"]
            if fk_type_name not in skip:
                inline = spec_field.field_type_attrs.get("inline", [])
                if inline:
                    fk_type_spec = type_spec_store().get(fk_type_name)
                    fk_field_specs = R.pick(
                        inline,
                        flattened_spec_field_by_name(
                            fk_type_spec, skip + [fk_type_name]
                        ),
                    )
                    spec_fields.extend(fk_field_specs)
                else:
                    result[spec_field.name] = spec_field
        else:
            result[spec_field.name] = spec_field

    return result


class TypeSpecStore:
    def __init__(self):
        self._type_spec_by_type_name = {}

    def load_specs(self, type_specs_dir):
        for spec_fn in Path(type_specs_dir).glob("*.json"):
            type_name = spec_fn.stem
            type_spec_dict = _load_type_spec_dict(type_specs_dir, type_name)

            type_spec = TypeSpec(
                type_name=type_name,
                field_specs=_get_field_specs(type_spec_dict),
            )
            self.setdefault(type_name, type_spec)

    def _on_add_type_spec(self, type_spec):
        for field_spec in type_spec.field_specs:
            if field_spec.field_type == "fk" and field_spec.field_type_attrs.get(
                "has_related_set"
            ):
                fk_type_spec = self.get(field_spec.field_type_attrs["target"])
                name = lower0(type_spec.type_name + "Set")
                if [x for x in fk_type_spec.field_specs if x.name == name]:
                    raise Exception("Field spec with name {name} already exists")

                fk_type_spec.field_specs.append(
                    FieldSpec(
                        name=name,
                        name_snake=camel_to_snake(name),
                        required=False,
                        private=field_spec.private,
                        field_type="related_set",
                        field_type_attrs=dict(target=type_spec.type_name),
                    )
                )

    def setdefault(self, type_name, default_value):
        assert type_name and type_name[0] == type_name[0].upper()

        if not self.has(type_name):
            self._type_spec_by_type_name[type_name] = default_value
            self._on_add_type_spec(default_value)

    def has(self, type_name):
        assert type_name and type_name[0] == type_name[0].upper()

        return type_name in self._type_spec_by_type_name

    def get(self, type_name, default=_default_type_spec_placeholder):
        type_name = upper0(type_name)  # HACK
        assert type_name and type_name[0] == type_name[0].upper()

        type_spec = self._type_spec_by_type_name.get(type_name, None)

        return (
            type_spec
            if type_spec is not None
            else (
                TypeSpec(type_name=type_name, field_specs=_default_field_specs)
                if default is _default_type_spec_placeholder
                else default
            )
        )

    def get_form(self, type_name, default=_default_type_spec_placeholder):
        data_type_name = upper0(type_name)  # HACK
        data_type_spec = self.get(data_type_name)

        form_type_name = upper0(type_name + "Form")  # HACK
        form_type_spec = self._type_spec_by_type_name.get(form_type_name, None)

        return (
            form_type_spec
            if form_type_spec is not None
            else _form_type_spec_from_data_type_spec(data_type_spec)
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
