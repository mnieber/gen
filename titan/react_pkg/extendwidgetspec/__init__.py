from moonleap.packages.extensions.extend import extend
from moonleap.packages.extensions.memfield import MemField
from moonleap.packages.extensions.prop import Prop
from titan.react_pkg.component.resources import Component
from widgetspec.widget_spec import WidgetSpec

from . import props


@extend(WidgetSpec)
class ExtendWidgetSpec:
    component = Prop(props.widget_spec_component)
    pipelines = MemField(lambda: list())
    handler_terms = Prop(props.widget_spec_handler_terms)
    named_prop_terms = Prop(props.widget_spec_named_prop_terms)
    named_default_prop_terms = Prop(props.widget_spec_named_default_prop_terms)


@extend(Component)
class ExtendComponent:
    widget_spec = Prop(props.component_widget_spec)
