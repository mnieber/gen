from moonleap import Prop, extend
from moonleap.resources.field_spec import FieldSpec

from . import props


@extend(FieldSpec)
class ExtendFieldSpec:
    fk_type_spec = Prop(props.fk_type_spec)
