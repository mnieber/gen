from moonleap import Prop, extend
from moonleap.typespec.field_spec import FkFieldSpec, FormFieldSpec

from . import props


@extend(FkFieldSpec)
class ExtendFkFieldSpec:
    target_type_spec = Prop(props.field_spec_target_type_spec)


@extend(FormFieldSpec)
class ExtendFormFieldSpec:
    target_type_spec = Prop(props.field_spec_target_type_spec)
