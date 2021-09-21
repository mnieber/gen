from moonleap import Prop, extend
from moonleap.resources.type_spec_store import FieldSpec

from . import props


@extend(FieldSpec)
class ExtendFieldSpec:
    fk_type_spec = Prop(props.fk_type_spec)
