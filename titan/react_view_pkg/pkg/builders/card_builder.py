from titan.react_view_pkg.pkg.builder import Builder
from titan.react_view_pkg.pkg.div_attrs import update_div_attrs


class CardBuilder(Builder):
    def build(self, div_attrs):
        self._add_div_open(update_div_attrs(div_attrs, prefix_classes=["card"]))
        self._add_child_widgets()
        self._add_div_close()
