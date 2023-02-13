from moonleap import MemFun
from moonleap.packages.extensions.extend import extend
from moonleap.packages.extensions.prop import Prop
from titan.widgetspec.widget_spec import WidgetSpec

from . import props
from .widget_spec_get_form_data import widget_spec_get_form_data


@extend(WidgetSpec)
class ExtendWidgetSpec:
    component = Prop(props.widget_spec_component)
    bvr_names = Prop(props.widget_spec_bvr_names)
    handler_term_strs = Prop(props.widget_spec_handler_term_strs)
    get_form_data = MemFun(widget_spec_get_form_data)
    get_bvr_names = MemFun(props.widget_spec_get_bvr_names)
