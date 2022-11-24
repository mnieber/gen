import os

from moonleap.utils.fp import append_uniq
from titan.react_view_pkg.pkg.builder_output import BuilderOutput
from titan.react_view_pkg.pkg.create_widget_class_name import create_widget_class_name
from titan.react_view_pkg.pkg.get_margins import get_margins
from titan.react_view_pkg.pkg.update_captured_builder import update_captured_builder


class Builder:
    def __init__(self, widget_spec, parent_builder, level):
        self.builder_type_lut = dict()
        self.widget_spec = widget_spec
        self.parent_builder = parent_builder
        self.level = level
        self.output = BuilderOutput(
            widget_class_name=create_widget_class_name(widget_spec, parent_builder),
        )
        self._get_components()
        self.captured_builder = update_captured_builder(self)

    def register_builder_type(self, widget_base_type, builder_type):
        self.builder_type_lut[widget_base_type] = builder_type

    def add_lines(self, lines):
        indented_lines = [" " * self.level + x for x in lines]
        if self.captured_builder:
            id = self.captured_builder.widget_spec.id
            preamble_lines = self.output.preamble_lines_by_id.setdefault(id, [])
            self.output.postamble_lines_by_id.setdefault(id, [])
            preamble_lines.extend(indented_lines)
        else:
            self.output.lines.extend(indented_lines)

    def _get_components(self):
        if self.widget_spec.is_component and self.level > 0:
            self.output.components.append(self.widget_spec.component)

    def _add_div_open(self, classes=None, handlers=None):
        class_names = (
            [f'"{self.output.widget_class_name}"']
            + (classes or [])
            + (self.widget_spec.styles)
            + (["props.className"] if self.widget_spec.is_component_def else [])
        )

        for external_css_class in ("card",):
            if external_css_class in (classes or []):
                append_uniq(self.output.external_css_classes, external_css_class)

        self.add_lines(
            [
                f'<div className={{cn({", ".join(class_names)})}} {os.linesep.join(handlers or [])}>'
            ]
        )

    def _add_child_widgets(self, child_widget_specs=None):
        if child_widget_specs is None:
            child_widget_specs = self.widget_spec.child_widget_specs

        self.level += 1
        prev_widget_spec = None

        for child_widget_spec in child_widget_specs:
            if child_widget_spec.widget_base_type == "Children":
                self.output.has_children = True

        for child_widget_spec in child_widget_specs:
            builder = self._get_child_widget_builder(child_widget_spec, self.level)
            margins = get_margins(prev_widget_spec, child_widget_spec)
            builder.build(margins)
            self.output.add(builder.output)
            prev_widget_spec = child_widget_spec

        self.level -= 1

    def _get_child_widget_builder(self, child_widget_spec, level):
        from titan.react_view_pkg.pkg.get_builder import get_builder

        # Look up builder_type in luts
        b = self
        while b:
            builder_type = b.builder_type_lut.get(
                child_widget_spec.widget_base_type, None
            )
            if builder_type:
                return builder_type(child_widget_spec, self, level)
            b = b.parent_builder

        return get_builder(child_widget_spec, self, level)

    def _add_div_close(self):
        self.add_lines([f"</div>"])

    def build(self, classes=None, handlers=None):
        pass
