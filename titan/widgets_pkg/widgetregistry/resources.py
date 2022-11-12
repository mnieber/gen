import typing as T
from dataclasses import dataclass
from pprint import pprint

from moonleap import Resource
from titan.widgets_pkg.pkg.widget_spec import WidgetSpec


@dataclass
class WidgetRegistry(Resource):
    def __post_init__(self):
        self._widget_spec_by_widget_type = {}

    def setdefault(self, widget_type, default_value):
        if not self.has(widget_type):
            self._widget_spec_by_widget_type[widget_type] = default_value

    def has(self, widget_type):
        return widget_type in self._widget_spec_by_widget_type

    def get(self, widget_type, default="__not_set__") -> WidgetSpec:
        widget_spec = self._widget_spec_by_widget_type.get(widget_type, None)
        if widget_spec is not None:
            return widget_spec

        if default == "__not_set__":
            raise Exception(f"Widget {widget_type} not found")

        return default

    def widget_specs(self) -> T.List[WidgetSpec]:
        return self._widget_spec_by_widget_type.values()

    def pprint(self):
        def convert(widget_spec):
            prefix = widget_spec.widget_type if widget_spec.widget_type else ""
            suffix = (
                widget_spec.widget_base_type if widget_spec.widget_base_type else ""
            )
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
            widget_type="Root",
            widget_base_type="Root",
            child_widget_specs=self.widget_specs(),
        )
        data = convert(root)
        pprint(data)
