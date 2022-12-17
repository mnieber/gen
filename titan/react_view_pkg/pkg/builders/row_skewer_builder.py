from titan.react_view_pkg.pkg.builder import Builder


class RowSkewerBuilder(Builder):
    def update_widget_spec(self):
        self.widget_spec.div.styles += ["rowSkewer"]

    def build(self):
        self.add(imports=["import { rowSkewer } from 'src/frames/components';"])
