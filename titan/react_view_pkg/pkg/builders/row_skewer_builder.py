from titan.react_view_pkg.pkg.builder import Builder


class RowSkewerBuilder(Builder):
    def update_widget_spec(self):
        self.widget_spec.div.append_styles(["rowSkewer"])

    def build(self):
        self.output.add(imports=["import { rowSkewer } from 'src/frames/components';"])
