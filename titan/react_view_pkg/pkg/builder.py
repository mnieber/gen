from titan.react_view_pkg.pkg.add_child_widgets import add_child_widgets
from titan.react_view_pkg.pkg.add_div import add_div_close, add_div_open
from titan.react_view_pkg.pkg.builder_items_mixin import BuilderItemsMixin
from titan.react_view_pkg.pkg.builder_output import BuilderOutput


class Builder(BuilderItemsMixin):
    def __init__(self, widget_spec):
        self.widget_spec = widget_spec
        self.output = BuilderOutput()
        if "Children" in widget_spec.widget_base_types:
            self.output.has_children = True
        self.__post_init__()

    def __post_init__(self):
        pass

    def add(
        self,
        lines=None,
        props_lines=None,
        add_props_lines=None,
        imports_lines=None,
        scss_lines=None,
        preamble_lines=None,
        preamble_hooks_lines=None,
    ):
        level = self.widget_spec.level
        if lines:
            indented_lines = ["  " * level + x for x in lines]
            self.output.lines.extend(indented_lines)
        if props_lines:
            self.output.props_lines.extend(_trim(props_lines))
        if add_props_lines:
            self.output.add_props_lines.extend(_trim(add_props_lines))
        if imports_lines:
            self.output.imports_lines.extend(imports_lines)
        if scss_lines:
            self.output.scss_lines.extend(scss_lines)
        if preamble_lines:
            indented_lines = ["  " * level + x for x in preamble_lines]
            self.output.preamble_lines.extend(indented_lines)
        if preamble_hooks_lines:
            indented_lines = ["  " * level + x for x in preamble_hooks_lines]
            self.output.preamble_hooks_lines.extend(indented_lines)

    def _add_div_open(self):
        add_div_open(self)

    def _add_child_widgets(self, child_widget_specs=None):
        add_child_widgets(
            self, child_widget_specs or self.widget_spec.child_widget_specs
        )

    def _add_div_close(self):
        add_div_close(self)

    def build(self):
        pass

    def get_spec_extension(self, places):
        return None

    def update_widget_spec(self):
        pass

    def __repr__(self):
        return f"{self.__class__.__name__}({self.widget_spec})"

    @property
    def use_uikit(self):
        component = self.widget_spec.root.component
        return component and component.module.react_app.service.uikit


def _trim(lines):
    return [x if x == "\n" else x.removesuffix("\n") for x in lines]
