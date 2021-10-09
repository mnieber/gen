from moonleap import Prop, extend
from moonleap.typespec.field_spec import FieldSpec

from . import props


@extend(FieldSpec)
class ExtendFieldSpec:
    target_type_spec = Prop(props.target_type_spec)
