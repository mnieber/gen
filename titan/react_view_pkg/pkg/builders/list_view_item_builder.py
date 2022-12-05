from titan.react_view_pkg.pkg.builder import Builder


class ListViewItemBuilder(Builder):
    def build(self):
        styles = []
        props = []

        self.widget_spec.div_styles = styles + self.widget_spec.div_styles
        self.widget_spec.div_props = self.widget_spec.div_props + props

        inner_builder.build()
        self.output = inner_builder.output
