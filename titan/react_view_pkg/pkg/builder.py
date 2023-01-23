from titan.react_view_pkg.pkg.add_child_widgets import add_child_widgets
from titan.react_view_pkg.pkg.add_div import get_div_close, get_div_open
from titan.react_view_pkg.pkg.builder_output import BuilderOutput
from titan.react_view_pkg.pkg.builders.item_helper import ItemHelper
from titan.react_view_pkg.pkg.builders.item_list_helper import ItemListHelper


class Builder:
    type = "None"

    def __init__(self, widget_spec):
        self.widget_spec = widget_spec
        self.output = BuilderOutput()
        self.ilh = ItemListHelper(widget_spec)
        self.ih = ItemHelper(widget_spec)
        self.__post_init__()

    def __post_init__(self):
        pass

    def _add_div_open(self, also_close=False):
        self.output.add(
            lines=[
                get_div_open(
                    self.widget_spec.div,
                    widget_class_name=self.widget_spec.widget_class_name,
                    also_close=also_close,
                )
            ]
        )

    def _add_child_widgets(self, child_widget_specs=None):
        add_child_widgets(
            self, child_widget_specs or self.widget_spec.child_widget_specs
        )

    def _add_div_close(self):
        self.output.add(lines=[get_div_close(self.widget_spec.div)])

    def build(self):
        pass

    def get_spec_extension(self, places):
        return None

    def update_widget_spec(self):
        pass

    def get_value(self, name, recurse=False):
        return self.widget_spec.get_value_by_name(name, recurse=recurse)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.widget_spec})"
