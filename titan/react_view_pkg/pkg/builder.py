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

    def build(self):
        pass

    def get_spec_extension(self, places):
        return None

    def update_widget_spec(self):
        pass

    def get_value(self, name, recurse=False):
        return self.widget_spec.get_value(name, recurse=recurse)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.widget_spec})"
