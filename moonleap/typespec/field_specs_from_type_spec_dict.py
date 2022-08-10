from moonleap.typespec.field_spec import (
    FieldSpec,
    FkFieldSpec,
    FormFieldSpec,
    SlugFieldSpec,
)
from moonleap.utils.case import u0


def field_specs_from_type_spec_dict(type_spec_dict, type_name):
    required = type_spec_dict.get("required", [])
    private = type_spec_dict.get("private", [])
    result = []
    for field_name, field_spec_dict in type_spec_dict["properties"].items():
        t, attrs = _field_type_and_attrs(field_spec_dict)
        if t is None:
            raise Exception(f"Unknown field type for field: {field_name}")

        if "_" in field_name:
            raise Exception(
                f"Field names should not have underscores. For field: {field_name}"
                + f" in type: {type_name}"
            )

        constructor = get_field_spec_constructor(t)
        result.append(
            constructor(
                default_value=_default_value(field_spec_dict),
                description=_description(field_spec_dict),
                field_type=t,
                field_type_attrs=attrs,
                name=field_name,
                private=field_name in private,
                required=field_name in required,
                unique=_unique(field_spec_dict),
            )
        )
    return result


def _unique(field_spec):
    return field_spec.get("unique", False)


def _description(field_spec):
    return field_spec.get("description")


def _field_type_and_attrs(field_spec_dict):
    attrs = {}
    t = field_spec_dict.get("type")

    if t == "fk":
        target = attrs["target"] = field_spec_dict["target"]
        _check_target(target)
        attrs["hasRelatedSet"] = field_spec_dict.get("hasRelatedSet", True)
        if "onDelete" in field_spec_dict:
            attrs["onDelete"] = field_spec_dict["onDelete"]
    elif t == "relatedSet":
        target = attrs["target"] = field_spec_dict["target"]
        _check_target(target)
        attrs["adminInline"] = field_spec_dict.get("adminInline", True)
        if "through" in field_spec_dict:
            attrs["through"] = field_spec_dict["through"]
    elif t == "form":
        target = attrs["target"] = field_spec_dict["target"]
        _check_target(target)
    elif t == "uuid" and field_spec_dict.get("target"):
        target = attrs["target"] = field_spec_dict.get("target")
        _check_target(target)
    else:
        attrs["index"] = field_spec_dict.get("index", False)
        if "maxLength" in field_spec_dict:
            attrs["maxLength"] = field_spec_dict["maxLength"]
        if "choices" in field_spec_dict:
            attrs["choices"] = field_spec_dict["choices"]
        if "slugSrc" in field_spec_dict:
            attrs["slugSrc"] = field_spec_dict.get("slugSrc")

    return t, attrs


def _check_target(target):
    if target != u0(target):
        raise Exception(f"Target should be capitalized: {target}")


def _default_value(field_spec):
    return field_spec.get("default", None)


def get_field_spec_constructor(t):
    return (
        FkFieldSpec
        if t in ("fk", "relatedSet")
        else SlugFieldSpec
        if t in ("slug")
        else FormFieldSpec
        if t in ("form")
        else FieldSpec
    )
