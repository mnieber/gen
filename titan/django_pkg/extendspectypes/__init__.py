from moonleap import Prop, extend
from moonleap.resources.type_spec_store import TypeSpec

from . import props


@extend(TypeSpec)
class ExtendTypeSpec:
    tn_graphene = Prop(props.tn_graphene)
    tn_django_model = Prop(props.tn_django_model)
