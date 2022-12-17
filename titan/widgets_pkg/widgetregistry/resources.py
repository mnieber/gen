import typing as T
from dataclasses import dataclass
from pprint import pprint

from moonleap import Resource
from titan.widgets_pkg.pkg.widget_spec import WidgetSpec


@dataclass
class WidgetRegistry(Resource):
    def __post_init__(self):
        self._widget_spec_by_widget_name = {}
        self.states_by_module_name = {}

    def setdefault(self, widget_name, default_value):
        if not self.has(widget_name):
            self._widget_spec_by_widget_name[widget_name] = default_value

    def has(self, widget_name):
        return widget_name in self._widget_spec_by_widget_name

    def get(self, widget_name, default: T.Optional[str] = "__not_set__") -> WidgetSpec:
        widget_spec = self._widget_spec_by_widget_name.get(widget_name, None)
        if widget_spec is not None:
            return widget_spec

        if default == "__not_set__":
            raise Exception(f"Widget {widget_name} not found")

        return default

    def widget_specs(self) -> T.List[WidgetSpec]:
        return self._widget_spec_by_widget_name.values()

    def pprint(self):
        def convert(widget_spec):
            prefix = widget_spec.widget_name if widget_spec.widget_name else ""
            suffix = ", ".join(widget_spec.widget_base_types)
            infix = " as " if prefix and suffix else ""
            key = prefix + infix + suffix

            value = {}
            for child_key, child_value in [
                convert(x) for x in widget_spec.child_widget_specs
            ]:
                while child_key in value:
                    child_key += "~"
                value[child_key] = child_value

            return key, value

        root = WidgetSpec(
            widget_name="Root",
            widget_base_types=["Root"],
            child_widget_specs=self.widget_specs(),
        )
        data = convert(root)
        pprint(data)
