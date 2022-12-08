from moonleap.utils.indent import indent
from titan.react_view_pkg.pkg.builder import Builder


class VerbatimBuilder(Builder):
    def __init__(self, widget_spec, parent_builder, level, div):
        super().__init__(widget_spec, parent_builder, level)
        self.div = indent(level)(div)

    def build(self):
        self.add(lines=[self.div])
