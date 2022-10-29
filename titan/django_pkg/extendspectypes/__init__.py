from moonleap import MemFun, Prop, extend
from titan.types_pkg.typeregistry.field_spec import FieldSpec
from titan.types_pkg.typeregistry.type_spec import TypeSpec

from . import props


@extend(TypeSpec)
class ExtendTypeSpec:
    tn_graphene = Prop(props.tn_graphene)


@extend(FieldSpec)
class ExtendFieldSpec:
    graphene_type = MemFun(props.graphene_type)
    target_item = Prop(props.target_item)
