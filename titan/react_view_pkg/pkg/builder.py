import os

from titan.react_view_pkg.pkg.add_child_widgets import add_child_widgets
from titan.react_view_pkg.pkg.add_div import add_div_close, add_div_open
from titan.react_view_pkg.pkg.update_captured_builder import (
    create_builder_output,
    get_root_builder,
)


class Builder:
    def __init__(self, widget_spec, parent_builder, level):
        self.builder_type_lut = dict()
        self.widget_spec = widget_spec
        self.parent_builder = parent_builder
        self.level = level
        self.root_builder = get_root_builder(self)
        self.output = create_builder_output(self)

    @property
    def is_captured(self):
        if self.widget_spec.values.get("array", False):
            return "array"
        if self.widget_spec.values.get("capture", False):
            return "capture"
        return False

    def register_builder_type(self, widget_base_type, builder_type):
        self.builder_type_lut[widget_base_type] = builder_type

    def add_lines(self, lines):
        indented_lines = ["  " * self.level + x for x in lines]
        self.output.lines.extend(indented_lines)

    def _add_div_open(self, classes=None, handlers=None):
        add_div_open(self, classes, handlers)

    def _add_child_widgets(self, child_widget_specs=None):
        add_child_widgets(
            self, child_widget_specs or self.widget_spec.child_widget_specs
        )

    def _add_div_close(self):
        add_div_close(self)

    def build(self, classes=None, handlers=None):
        pass
