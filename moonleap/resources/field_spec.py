import typing as T
from dataclasses import dataclass, field

from moonleap.utils.case import lower0, snake_to_camel
from moonleap.utils.chop import chop_postfix


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


fk_prefix = "/data_types/"


def _default_value(field_spec):
    return field_spec.get("default", None)


def _unique(field_spec):
    return field_spec.get("unique", False)


def _description(field_spec):
    return field_spec.get("description")


def _field_type_and_attrs(field_spec_dict):
    attrs = {}
    t = field_spec_dict.get("type")

    if t is None:
        ref = field_spec_dict.get("$ref", "")
        if ref.startswith(fk_prefix):
            t = "fk"
            attrs["target"] = ref[len(fk_prefix) :]  # noqa: E203
            attrs["has_related_set"] = field_spec_dict.get("hasRelatedSet", True)
    else:
        if "onDelete" in field_spec_dict:
            attrs["on_delete"] = field_spec_dict["onDelete"]

        if "maxLength" in field_spec_dict:
            attrs["max_length"] = field_spec_dict["maxLength"]

    return t, attrs


def type_name_to_item_name(type_name):
    return lower0(chop_postfix(type_name, "Form"))


def field_specs_from_type_spec_dict(type_spec_dict):
    required = type_spec_dict.get("required", [])
    private = type_spec_dict.get("private", [])
    result = []
    for field_name, field_spec_dict in type_spec_dict["properties"].items():
        t, attrs = _field_type_and_attrs(field_spec_dict)
        if t is None:
            raise Exception(f"Unknown field type for field: {field_name}")

        if t == "form":
            fk_item_name = type_name_to_item_name(attrs["target"])
            attrs.setdefault("item_name", fk_item_name)

        if t == "fk":
            fk_item_name = lower0(attrs["target"])
            attrs.setdefault("item_name", fk_item_name)

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
