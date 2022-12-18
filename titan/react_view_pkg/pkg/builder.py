from titan.react_view_pkg.pkg.add_child_widgets import add_child_widgets
from titan.react_view_pkg.pkg.add_div import get_div_close, get_div_open
from titan.react_view_pkg.pkg.builder_output import BuilderOutput
from titan.react_view_pkg.pkg.builders.item_helper import ItemHelper
from titan.react_view_pkg.pkg.builders.item_list_helper import ItemListHelper


class Builder:
    def __init__(self, widget_spec):
        self.widget_spec = widget_spec
        self.output = BuilderOutput()
        self.ilh = ItemListHelper(widget_spec)
        self.ih = ItemHelper(widget_spec)
        if "Children" in widget_spec.widget_base_types:
            self.output.has_children = True
        self.__post_init__()

    def __post_init__(self):
        pass

    def add(
        self,
        lines=None,
        props=None,
        add_props=None,
        default_props=None,
        imports=None,
        scss=None,
        preamble=None,
        preamble_hooks=None,
    ):
        level = self.widget_spec.level
        if lines:
            indented_lines = ["  " * level + x for x in lines]
            self.output.lines.extend(indented_lines)
        if props:
            self.output.props_lines.extend(_trim(props))
        if add_props:
            self.output.add_props_lines.extend(_trim(add_props))
        if default_props:
            self.output.default_props.extend(default_props)
        if imports:
            self.output.imports_lines.extend(imports)
        if scss:
            self.output.scss_lines.extend(scss)
        if preamble:
            indented_lines = ["  " * level + x for x in preamble]
            self.output.preamble_lines.extend(indented_lines)
        if preamble_hooks:
            indented_lines = ["  " * level + x for x in preamble_hooks]
            self.output.preamble_hooks_lines.extend(indented_lines)

    def _add_div_open(self):
        self.add(
            lines=[
                get_div_open(
                    self.widget_spec.div,
                    widget_class_name=self.widget_spec.widget_class_name,
                )
            ]
        )

    def _add_child_widgets(self, child_widget_specs=None):
        add_child_widgets(
            self, child_widget_specs or self.widget_spec.child_widget_specs
        )

    def _add_div_close(self):
        self.add(lines=[get_div_close()])

    def build(self):
        pass

    def get_spec_extension(self, places):
        return None

    def update_widget_spec(self):
        pass

    def __repr__(self):
        return f"{self.__class__.__name__}({self.widget_spec})"


def _trim(lines):
    return [x if x == "\n" else x.removesuffix("\n") for x in lines]
