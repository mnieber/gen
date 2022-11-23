import os

from moonleap import u0
from moonleap.utils.fp import append_uniq
from titan.react_view_pkg.pkg.builder_output import BuilderOutput
from titan.react_view_pkg.pkg.get_capture_elements import get_capture_elements
from titan.react_view_pkg.pkg.get_margins import get_margins


class Builder:
    def __init__(self, widget_spec, parent_builder, level):
        self.builder_lut = dict()
        self.widget_spec = widget_spec
        self.parent_builder = parent_builder
        self.level = level
        self.output = BuilderOutput(
            widget_class_name=self._create_widget_class_name(),
        )
        self._get_components()

        self.is_captured, const_name, prefix, suffix = get_capture_elements(self)
        if self.is_captured and self.is_captured is self:
            if prefix:
                self.output.preamble_lines.append(prefix)
                self.output.lines.append(f"{{{const_name}}}")
            if suffix:
                self.output.postamble_lines.append(suffix)

    def register_builder_type(self, widget_type, builder_type):
        self.builder_lut[widget_type] = builder_type

    def add_lines(self, lines):
        indented_lines = [" " * self.level + x for x in lines]
        if self.is_captured:
            self.output.preamble_lines.extend(indented_lines)
        else:
            self.output.lines.extend(indented_lines)

    def _get_components(self):
        if self.widget_spec.is_component and self.level > 0:
            self.output.components.append(self.widget_spec.component)

    def _create_widget_class_name(self):
        widget_class_name = (
            _to_widget_class_name(self.widget_spec)
            or self.widget_spec.place
            or self.widget_spec.widget_base_type
        )
        if self.widget_spec.is_component:
            return widget_class_name

        if self.parent_builder and widget_class_name:
            parent_widget_spec = self.parent_builder.widget_spec
            infix = "__" if parent_widget_spec.is_component else ""
            return (
                self.parent_builder.output.widget_class_name + infix + widget_class_name
            )

        return widget_class_name

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
            builder = self._get_builder(child_widget_spec, self.level)
            margins = get_margins(prev_widget_spec, child_widget_spec)
            builder.build(margins)
            self.output.add(builder.output)
            prev_widget_spec = child_widget_spec

        self.level -= 1

    def _get_builder(self, child_widget_spec, level):
        from titan.react_view_pkg.pkg.get_builder import get_builder

        # Look up builder in luts
        b = self
        while b:
            builder = b.builder_lut.get(child_widget_spec.widget_base_type, None)
            if builder:
                return builder(child_widget_spec, self, level)
            b = b.parent_builder

        return get_builder(child_widget_spec, self, level)

    def _add_div_close(self):
        self.add_lines([f"</div>"])

    def build(self, classes=None, handlers=None):
        pass


def _to_widget_class_name(widget_spec):
    if not widget_spec.is_component:
        return u0(widget_spec.widget_type)
    return widget_spec.component.name
