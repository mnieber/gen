from titan.react_view_pkg.pkg.builder import Builder


class CardBuilder(Builder):
    def build(self):
        if "card" not in self.widget_spec.div_styles:
            self.widget_spec.div_styles = ["card"] + self.widget_spec.div_styles
        self._add_div_open()
        self._add_child_widgets()
        self._add_div_close()
