import typing as T
from dataclasses import dataclass, field

from moonleap.utils.case import l0, u0
from moonleap.utils.chop import chop_prefix


@dataclass
class FieldSpec:
    field_type: str
    name: str
    private: bool
    required: bool
    default_value: T.Any = None
    description: T.Optional[str] = None
    unique: bool = False
    field_type_attrs: dict = field(default_factory=dict)

    @property
    def target(self):
        return self.field_type_attrs.get("target")

    @property
    def index(self):
        return self.field_type_attrs.get("index", False)

    @property
    def related_output(self):
        return self.field_type_attrs.get("relatedOutput")

    @property
    def short_name(self):
        return l0(chop_prefix(self.name, self.related_output or ""))


@dataclass
class SlugFieldSpec(FieldSpec):
    @property
    def slug_src(self):
        return self.field_type_attrs.get("slugSrc")


@dataclass
class FormFieldSpec(FieldSpec):
    pass


@dataclass
class FkFieldSpec(FieldSpec):
    @property
    def through(self):
        return self.field_type_attrs.get("through")

    @property
    def admin_inline(self):
        return self.field_type_attrs.get("adminInline")

    @property
    def has_related_set(self):
        return self.field_type_attrs.get("hasRelatedSet")

    @property
    def add_id_field(self):
        return self.field_type_attrs.get("addIdField")


def _default_value(field_spec):
    return field_spec.get("default", None)


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
        attrs["addIdField"] = field_spec_dict.get("addIdField", False)
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


def input_is_used_for_output(input_field_spec, output_field_spec):
    related_output = input_field_spec.related_output
    return not related_output or output_field_spec.name == related_output
