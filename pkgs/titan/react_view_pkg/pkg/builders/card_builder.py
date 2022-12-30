from titan.react_view_pkg.pkg.builder import Builder


class CardBuilder(Builder):
    def update_widget_spec(self):
        self.widget_spec.div.prepend_styles(["card"])

    def build(self):
        self.add(imports=["import { card } from 'src/frames/components';"])
        self._add_div_open()
        self._add_child_widgets()
        self._add_div_close()
