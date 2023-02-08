from moonleap import MemFun
from moonleap.packages.extensions.extend import extend
from moonleap.packages.extensions.prop import Prop
from titan.widgetspec.widget_spec import WidgetSpec

from . import props


@extend(WidgetSpec)
class ExtendWidgetSpec:
    component = Prop(props.widget_spec_component)
    bvr_names = Prop(props.widget_spec_bvr_names)
    handler_terms = Prop(props.widget_spec_handler_terms)
    field_names = Prop(props.widget_spec_field_names)
    get_field_names = MemFun(props.widget_spec_get_field_names)
    get_bvr_names = MemFun(props.widget_spec_get_bvr_names)
