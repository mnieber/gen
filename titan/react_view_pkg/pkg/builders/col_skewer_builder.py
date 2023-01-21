from titan.react_view_pkg.pkg.builder import Builder


class ColSkewerBuilder(Builder):
    type = "ColSkewer"

    def update_widget_spec(self):
        self.widget_spec.div.prepend_styles(["colSkewer"])

    def build(self):
        self.output.add(imports=["import { colSkewer } from 'src/frames/components';"])
