import typing as T

from jdoc.moonleap.resource import *
from jdoc.scenario import *


class WidgetSpec(Entity):
    module_name: str
    component_term: str
    widget_base_types: T.List[str] = []
    child_widget_specs: T.List["WidgetSpec"] = []


class WidgetReg(Entity):
    widget_specs: T.List[WidgetSpec] = []

    def load_widget_specs(self):
        pass


class WidgetSpecParserRes(Entity):
    widget_spec_yaml: str


global_widget_reg = WidgetReg()
