from moonleap import MemFun, Prop, extend
from titan.types_pkg.pkg.field_spec import FieldSpec
from titan.types_pkg.pkg.type_spec import TypeSpec

from . import props


@extend(TypeSpec)
class ExtendTypeSpec:
    tn_graphene = Prop(props.tn_graphene)


@extend(FieldSpec)
class ExtendFieldSpec:
    graphene_type = MemFun(props.graphene_type)
    target_item = Prop(props.target_item)
    graphql_type = MemFun(props.field_spec_graphql_type)
