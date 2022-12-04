from titan.react_view_pkg.pkg.add_child_widgets import add_child_widgets
from titan.react_view_pkg.pkg.add_div import add_div_close, add_div_open
from titan.react_view_pkg.pkg.builder_items_mixin import BuilderItemsMixin
from titan.react_view_pkg.pkg.builder_output import BuilderOutput
from titan.react_view_pkg.pkg.builder_pipeline_mixin import BuilderPipelineMixin
from titan.widgets_pkg.pkg.create_widget_class_name import create_widget_class_name


class Builder(BuilderPipelineMixin, BuilderItemsMixin):
    def __init__(self, widget_spec, parent_builder, level):
        self.widget_spec = widget_spec
        self.parent_builder = parent_builder
        self.level = level
        self.root_builder = get_root_builder(self)

        self.output = BuilderOutput(widget_class_name=create_widget_class_name(self))
        if widget_spec.widget_base_type == "Children":
            self.output.has_children = True

        self.__post_init__()

    def __post_init__(self):
        pass

    def add_lines(self, lines):
        indented_lines = ["  " * self.level + x for x in lines]
        self.output.lines.extend(indented_lines)

    def add_preamble(self, lines):
        indented_lines = ["  " * self.level + x for x in lines]
        self.output.preamble_lines.extend(indented_lines)

    def _add_div_open(self, div_attrs=None):
        add_div_open(self, div_attrs)

    def _add_child_widgets(self, child_widget_specs=None):
        add_child_widgets(
            self, child_widget_specs or self.widget_spec.child_widget_specs
        )

    def _add_div_close(self):
        add_div_close(self)

    def build(self, div_attrs=None):
        pass

    def __repr__(self):
        return f"{self.__class__.__name__}({self.widget_spec})"

    @property
    def use_ui_kit(self):
        component = self.widget_spec.component
        return component and component.react_app.service.uikit


def get_root_builder(builder):
    b = builder

    while b.parent_builder:
        b = b.parent_builder

    return b
