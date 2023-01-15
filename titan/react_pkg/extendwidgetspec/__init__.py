from moonleap import MemFun
from moonleap.packages.extensions.extend import extend
from moonleap.packages.extensions.memfield import MemField
from moonleap.packages.extensions.prop import Prop
from titan.widgetspec.widget_spec import WidgetSpec

from . import props


@extend(WidgetSpec)
class ExtendWidgetSpec:
    component = Prop(props.widget_spec_component)
    pipelines = MemField(lambda: list())
    get_pipeline_by_name = MemFun(props.widget_spec_get_pipeline_by_name)
    get_data_path = MemFun(props.widget_spec_get_data_path)
    maybe_expression = MemFun(props.widget_spec_maybe_expression)
    handler_terms = Prop(props.widget_spec_handler_terms)
    bvr_names = Prop(props.widget_spec_bvr_names)
    field_names = Prop(props.widget_spec_field_names)
    queries = Prop(props.widget_spec_queries)
    mutations = Prop(props.widget_spec_mutations)
    named_props = MemField(lambda: list())
    named_default_props = MemField(lambda: list())
