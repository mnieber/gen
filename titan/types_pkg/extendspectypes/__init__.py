from moonleap import Prop, extend
from titan.typespec.field_spec import FieldSpec, FormFieldSpec

from . import props


@extend(FieldSpec)
class ExtendFkFieldSpec:
    target_type_spec = Prop(props.fk_field_spec_target_type_spec)


@extend(FormFieldSpec)
class ExtendFormFieldSpec:
    target_type_spec = Prop(props.form_field_spec_target_type_spec)
