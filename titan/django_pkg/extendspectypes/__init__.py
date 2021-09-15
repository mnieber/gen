from moonleap import Prop, extend
from moonleap.resources.type_spec_store import FieldSpec, TypeSpec

from . import props


@extend(FieldSpec)
class ExtendFieldSpec:
    fk_type_spec = Prop(props.fk_type_spec)


@extend(TypeSpec)
class ExtendTypeSpec:
    tn_graphene = Prop(props.tn_graphene)
    tn_django_model = Prop(props.tn_django_model)
