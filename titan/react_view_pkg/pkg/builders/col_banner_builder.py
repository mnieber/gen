from titan.react_view_pkg.pkg.builder import Builder


class ColBannerBuilder(Builder):
    type = "ColBanner"

    def update_widget_spec(self):
        self.widget_spec.div.prepend_styles(["colBanner"])

    def build(self):
        self.output.add(imports=["import { colBanner } from '/src/frames/components';"])
