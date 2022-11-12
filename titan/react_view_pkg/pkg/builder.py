import os

from moonleap.utils.fp import append_uniq
from titan.react_view_pkg.pkg.get_margins import get_margins


class Builder:
    def __init__(self, widget_spec, parent_builder, level):
        self.widget_spec = widget_spec
        self.parent_builder = parent_builder
        self.level = level
        self.widget_name = self._create_widget_name()
        self.result = []
        self.components = []
        self.css_classes = []
        self._get_components()

    def __add__(self, lines):
        self.result += [" " * self.level + x for x in lines]
        return self

    def _get_components(self):
        if self.widget_spec.is_component:
            self.components.append(self.widget_spec.component)

    def _create_widget_name(self):
        widget_name = _to_widget_name(self.widget_spec) or self.widget_spec.place
        if self.widget_spec.is_component:
            return widget_name

        if self.parent_builder and widget_name:
            parent_widget_spec = self.parent_builder.widget_spec
            infix = "__" if parent_widget_spec.is_component else ""
            return self.parent_builder.widget_name + infix + widget_name

        return widget_name

    def _add_div_open(self, classes=None):
        class_names = (
            [f'"{self.widget_name}"']
            + (classes or [])
            + (self.widget_spec.styles)
            + (["props.className"] if self.widget_spec.is_component else [])
        )

        for css_class in ("card",):
            if css_class in (classes or []):
                append_uniq(self.css_classes, css_class)

        self += [f'<div className={{cn({", ".join(class_names)})}}>']

    def _add_child_widgets(self):
        from titan.react_view_pkg.pkg.get_builder import get_builder

        self.level += 1
        prev_widget_spec = None

        for child_widget_spec in self.widget_spec.child_widget_specs:
            builder = get_builder(child_widget_spec, self, self.level + 1)
            margins = get_margins(prev_widget_spec, child_widget_spec)
            child_div, child_components, child_css_classes = builder.get_div(margins)
            self.components += child_components
            for css_class in child_css_classes:
                append_uniq(self.css_classes, css_class)
            self += [child_div]
            prev_widget_spec = child_widget_spec

        self.level -= 1

    def _add_div_close(self):
        self += [f"</div>"]
        return self._output()

    def _output(self):
        return os.linesep.join(self.result), self.components, self.css_classes

    def get_div(self, classes=None):
        return "", [], []


def _to_widget_name(widget_spec):
    if not widget_spec.is_component:
        return widget_spec.widget_type
    return widget_spec.component.name
