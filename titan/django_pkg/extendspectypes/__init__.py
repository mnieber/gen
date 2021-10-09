from moonleap import MemFun, Prop, extend
from moonleap.typespec.field_spec import FieldSpec
from moonleap.typespec.type_spec_store import TypeSpec

from . import props


@extend(TypeSpec)
class ExtendTypeSpec:
    tn_graphene = Prop(props.tn_graphene)


@extend(FieldSpec)
class ExtendFieldSpec:
    graphene_input_type = Prop(props.graphene_input_type)
    graphene_output_type = MemFun(props.graphene_output_type)
    target_django_module = MemFun(props.target_django_module)
