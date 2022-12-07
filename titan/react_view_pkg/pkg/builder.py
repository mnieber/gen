from titan.react_view_pkg.pkg.add_child_widgets import add_child_widgets
from titan.react_view_pkg.pkg.add_div import add_div_close, add_div_open
from titan.react_view_pkg.pkg.builder_items_mixin import BuilderItemsMixin
from titan.react_view_pkg.pkg.builder_output import BuilderOutput
from titan.react_view_pkg.pkg.builder_render_mixin import BuilderRenderMixin


class Builder(BuilderRenderMixin, BuilderItemsMixin):
    def __init__(self, widget_spec):
        self.widget_spec = widget_spec
        self.output = BuilderOutput()
        if "Children" in widget_spec.widget_base_types:
            self.output.has_children = True
        self.__post_init__()

    def __post_init__(self):
        pass

    def add_lines(self, lines):
        indented_lines = ["  " * self.widget_spec.level + x for x in lines]
        self.output.lines.extend(indented_lines)

    def add_import_lines(self, lines):
        indented_lines = ["  " * self.widget_spec.level + x for x in lines]
        self.output.import_lines.extend(indented_lines)

    def add_preamble_lines(self, lines):
        indented_lines = ["  " * self.widget_spec.level + x for x in lines]
        self.output.preamble_lines.extend(indented_lines)

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

    def update_widget_spec(self, child_widget_spec):
        pass

    def __repr__(self):
        return f"{self.__class__.__name__}({self.widget_spec})"

    @property
    def use_uikit(self):
        component = self.widget_spec.root.component
        return component and component.module.react_app.service.uikit
