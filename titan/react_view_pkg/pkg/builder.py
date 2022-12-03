from titan.react_view_pkg.pkg.add_child_widgets import add_child_widgets
from titan.react_view_pkg.pkg.add_div import add_div_close, add_div_open
from titan.react_view_pkg.pkg.builder_items_mixin import BuilderItemsMixin
from titan.react_view_pkg.pkg.builder_output import BuilderOutput
from titan.react_view_pkg.pkg.builder_pipeline_mixin import BuilderPipelineMixin
from titan.react_view_pkg.pkg.create_widget_class_name import create_widget_class_name


class Builder(BuilderPipelineMixin, BuilderItemsMixin):
    def __init__(self, widget_spec, parent_builder, level):
        self.builder_type_lut = dict()
        self.widget_spec = widget_spec
        self.parent_builder = parent_builder
        self.level = level
        self.root_builder = get_root_builder(self)
        self.output = create_builder_output(self)

    def register_builder_type(self, widget_base_type, builder_type):
        self.builder_type_lut[widget_base_type] = builder_type

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

    def get_provided_prop_name(self, named_input):
        return None

    def build(self, div_attrs=None):
        pass

    def create_widget_class_name(self):
        return create_widget_class_name(self)

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


def create_builder_output(builder):
    output = BuilderOutput(widget_class_name=builder.create_widget_class_name())
    if builder.widget_spec.is_component and builder.level > 0:
        output.components.append(builder.widget_spec.component)
    return output
