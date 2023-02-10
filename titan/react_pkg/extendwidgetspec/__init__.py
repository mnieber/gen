import typing as T
from dataclasses import dataclass

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
    form_fields = Prop(props.widget_spec_form_fields)
    get_bvr_names = MemFun(props.widget_spec_get_bvr_names)


@dataclass
class FormField:
    name: str
    prefix: str = ""
    through: T.Optional[str] = None

    @property
    def as_str(self):
        return f"{self.prefix}{self.name}"
