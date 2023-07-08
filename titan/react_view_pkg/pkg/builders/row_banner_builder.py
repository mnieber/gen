from titan.react_view_pkg.pkg.builder import Builder


class RowBannerBuilder(Builder):
    type = "RowBanner"

    def update_widget_spec(self):
        self.widget_spec.div.prepend_styles(["rowBanner"])

    def build(self):
        self.output.add(imports=["import { rowBanner } from '/src/frames/components';"])
