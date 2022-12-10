from titan.react_view_pkg.pkg.builder import Builder


class CardBuilder(Builder):
    def update_widget_spec(self):
        if "card" not in self.widget_spec.div_styles:
            self.widget_spec.div_styles = ["card"] + self.widget_spec.div_styles

    def build(self):
        self.add(imports_lines=["import { card } from 'src/frames/components';"])
        self._add_div_open()
        self._add_child_widgets()
        self._add_div_close()
