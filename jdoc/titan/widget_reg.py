from jdoc.moonleap.resource import *
from jdoc.scenario import *


class WidgetSpec(Entity):
    module_name: str
    component_term: str
    widget_base_types: list[str] = []
    child_widget_specs: list["WidgetSpec"] = []


class WidgetReg(Entity):
    widget_specs: list[WidgetSpec] = []

    def load_widget_specs(self):
        pass


class WidgetSpecParserRes(Entity):
    widget_spec_yaml: str


global_widget_reg = WidgetReg()
