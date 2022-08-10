import typing as T
from dataclasses import dataclass, field

from moonleap.utils.case import l0
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


def input_is_used_for_output(input_field_spec, output_field_spec):
    related_output = input_field_spec.related_output
    return not related_output or output_field_spec.name == related_output
