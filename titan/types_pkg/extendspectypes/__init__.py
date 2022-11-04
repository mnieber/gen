from moonleap import MemFun, Prop, extend
from titan.types_pkg.pkg.field_spec import FieldSpec, FkFieldSpec, FormFieldSpec

from . import props


@extend(FkFieldSpec)
class ExtendFkFieldSpec:
    target_type_spec = Prop(props.fk_field_spec_target_type_spec)


@extend(FormFieldSpec)
class ExtendFormFieldSpec:
    target_type_spec = Prop(props.form_field_spec_target_type_spec)


@extend(FieldSpec)
class ExtendFieldSpec:
    graphql_type = MemFun(props.field_spec_graphql_type)